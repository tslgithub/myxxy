#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Date:    2018.04
# Copyright © 2018 Xuexiyou Company. All rights reserved.
######################################################################
import sys
# reload(sys)


import sys
import cv2
import os
import re
import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import inspect

#
# from aip import AipOcr
# """ 你的 APPID AK SK """
# APP_ID = '10539468'
# API_KEY = 'M7drAlWh6juKaunIvGRN346Z'
# SECRET_KEY = '8R64fekCM6MtSdKfGw3jw8m7EzRbLxyl'
#
# aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#
PARENTHESES_WIDTH = 33
PARENTHESES_LEFT = "xxy/parentheses_left.jpg"
PARENTHESES_RIGHT = "xxy/parentheses_right.jpg"
def sh(data):
    plt.imshow(data)
    plt.show()


def sh2(data):
    dpi = 80.0
    xpixels, ypixels = data.shape[::-1]
    margin = 0.05
    figsize = (1 + margin) * ypixels / dpi, (1 + margin) * xpixels / dpi
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])
    ax.imshow(data, interpolation='none')
    plt.show()

def sh3(data,s):
    data = cv2.resize(data,(0,0),None,s,s)
    cv2.imshow("img",data)
    cv2.waitKey()


def box(width, height):
    return np.ones((height, width), dtype=np.uint8)


def debug_pic(name,data):
    cv2.imwrite("output/"+name+".png", data)


def sort_contours(cnts, method="top-to-bottom"):
    if len(cnts)==0:
        return (cnts, [])
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


def contact_vertical_lines(lines):
    v_lines = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            angle = math.atan2(abs(y1 - y2), abs(x1 - x2))
            if abs(angle-math.pi/2)<0.05:
                v_lines.append([x1,min(y1,y2),x2,max(y1,y2)])
    sort_lines = sorted(v_lines, key=lambda loc: loc[0])
    contact_lines = []
    last_x = 0
    for x1,y1,x2,y2 in sort_lines:
        if len(contact_lines)==0:
            contact_lines.append([x1,y1,x2,y2])
        else:
            xx1, yy1, xx2, yy2 = contact_lines[-1]
            if x1-last_x<20 and ((yy1-20>y1 and yy1-20<y2) or (yy2+20>y1 and yy2+20<y2) or abs(yy1-y1)<20 or abs(yy1-y2)<20):
                contact_lines[-1][1] = min(yy1, yy2, y1, y2)
                contact_lines[-1][3] = max(yy1, yy2, y1, y2)
            else:
                contact_lines.append([x1, y1, x2, y2])
        last_x = x1
    return sorted(contact_lines, key=lambda loc: abs(loc[1] - loc[3]))[::-1]


def contact_contours(contours,offset_height=20):
    if len(contours)==0:
        return list([])
    (cnts, boundingBoxes) = sort_contours(contours)
    lines = list([])
    last_y = -999
    for contour in boundingBoxes:
        x, y, w, h = contour
        last_contour = contour
        if abs(y - last_y) > offset_height:
            lines.append([x, y, w, h])
        else:
            min_x = min(lines[-1][0], x)
            max_x = max(lines[-1][0] + lines[-1][2], x + w)
            lines[-1][0] = min_x
            lines[-1][2] = max_x - min_x
            lines[-1][3] = y+h -lines[-1][1]
        last_y = y

    last_contour = None
    i = 0
    new_lines = list([])
    for contour in lines:
        x, y, w, h = contour
        change = False
        if last_contour is not None:
            change=check_contours_include(last_contour, contour)
        if change:
            min_x = min(new_lines[-1][0], x)
            max_x = max(new_lines[-1][0] + new_lines[-1][2], x + w)
            new_lines[-1][0] = min_x
            new_lines[-1][2] = max_x - min_x
        else:
            new_lines.append([x, y, w, h])
        last_contour = contour
        i+=1
    return new_lines


def check_contours_include(contour_a, contour_b):
    if check_contour_a_include_B(contour_a, contour_b):
        return True
    return check_contour_a_include_B(contour_b, contour_a)

def check_contour_a_include_B(contour_a, contour_b):
    x1, y1, w1, h1 = contour_a
    x2, y2, w2, h2 = contour_b
    if x2>(x1+w1) or (x2+w2)<x1:
        return False
    if y2>(y1+h1) or (y2+h2)<y1:
        return False
    if x2<x1:
        w = x2+w2-x1
    else:
        w = x1+w1-x2
    if y2<y1:
        h = y2+h2-y1
    else:
        h = y1+h1-y2
    if w*h>w2*h2/2:
        return True
    return False


def ocr(mat):
    if mat is None or len(mat)==0:
        return ""
    mat_copy = remove_little_rect(mat)
    cv2.imwrite("output/_ocr_h.png", mat_copy)
    im = Image.open("output/_ocr_h.png")
    im.save("output/_ocr_h_3.png", dpi=(300, 300))
    os.system("tesseract" + " " + "output/_ocr_h_3.png" + " output/ocr  -l chi_sim --psm 7")
    fs = open("output/ocr.txt", 'r', encoding='utf-8')
    string = fs.read()
    string = re.sub(r'\n', "", string).replace('〈','(').replace('〉',')').replace('_、',\
                '一.').replace('L.','1.').replace('l.','1.').replace('_`','一.').replace('\`','.')
    print("ocr: " + string)
    return string

def ocroem0(mat):
    if mat is None or len(mat)==0:
        return ""
    mat_copy = remove_little_rect(mat)
    cv2.imwrite("output/_ocr_h.png", mat_copy)
    im = Image.open("output/_ocr_h.png")
    im.save("output/_ocr_h_3.png", dpi=(300, 300))
    os.system("tesseract" + " " + "output/_ocr_h_3.png" + " output/ocr  -l chi_sim --oem 0")
    fs = open("output/ocr.txt", 'r', encoding='utf-8')
    string = fs.read()
    string = re.sub(r'\n', "", string).replace('〈','(').replace('〉',\
                    ')').replace('_、','一.').replace('L.','1.').replace('l.','1.').replace('_\`','一.').replace('\`','.')
    print("ocr: " + string)
    return string


def ocr_number(mat):

    cv2.imwrite("output/_ocr_h.png", mat)
    im = Image.open("output/_ocr_h.png")
    im.save("output/_ocr_h_3.png", dpi=(300, 300))
    os.system("tesseract" + " " + "output/_ocr_h_3.png" + " output/ocr --oem 0 --psm 7 test_c")
    fs = open("output/ocr.txt", 'r', encoding='utf-8')
    string = fs.read()
    string = string.strip().replace('〈','(').replace('〉',')').replace('_、',\
                                          '一.').replace('L.','1.').replace('l.','1.').replace('_\`','一.').replace('\`','.')
    # string = re.sub(r'\D', "", string)
    print("ocr: " + string)
    return string


def ocr_eng(mat):
    cv2.imwrite("output/_ocr_h.png", mat)
    im = Image.open("output/_ocr_h.png")
    im.save("output/_ocr_h_3.png", dpi=(300, 300))
    os.system("tesseract" + " " + "output/_ocr_h_3.png" + " output/ocr -l eng --oem 0 --psm 7")
    fs = open("output/ocr.txt", 'r', encoding='utf-8')
    string = fs.read()
    string = string.strip().replace('〈',\
                    '(').replace('〉',')').replace('_、','一.').replace('L.','1.').replace('l.','1.').replace('_\`','一.').replace('\`','.')
    # string = re.sub(r'\D', "", string)
    print("ocr: " + string)
    return string

def ocr_baidu(mat):
    cv2.imwrite("output/_baidu.png",mat)
    file=open("output/_baidu.png",'rb')
    img = file.read()

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "false"
    options["detect_language"] = "false"
    options["probability"] = "false"
    options["log_id"] = "false"

    """ 调用通用文字识别, 图片参数为本地图片 """
    result = aipOcr.basicGeneral(img, options)
    """table api"""
    # tabel = aipOcr.form(image)
    fpath = open("dir.txt", "a")
    # print(result)
    words = ''
    for item in result['words_result']:
        # print (item['words'])
        # fpath.write(item['words'] + "\n")
        words =words + item['words']+" "
    file.close()
    # print(words)

    return words


def find_next_page(ck_y,contours_with_page):
    for contour in contours_with_page:
        x, y, w, h, page = contour
        if(ck_y > (y+20) ):
            continue
        return page
    return contours_with_page[-1][-1]


def use_max_location(x, y, v, locations, check_x=20, check_y=20):
    if (len(locations)==0):
        locations.append([x, y, v])
        return

    i = 0
    for loc in locations:
        ck_x, ck_y, ck_v = loc
        if( abs(ck_x-x)<check_x and abs(ck_y-y)<check_y):
            if(ck_v<v):
                locations[i]=[x,y,v]
            return
        i+=1
    locations.append([x, y, v])


def get_pic_height_and_offset_y(mat):
    locs = np.where(mat > 200)[0]
    return locs.max() - locs.min() + 1, locs.min()


def get_mat_width_height(mat):
    ya, xa = np.where(mat > 180)
    return xa.max() - xa.min() + 1, ya.max() - ya.min() + 1


def get_pic_height(mat):
    locs = np.where(mat > 200)[0]
    return locs.max() - locs.min() + 1

    mask = cv2.dilate(mat, box(10, 1))
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    max_height = 0
    for contour in contours:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        max_height = max(max_height, h)
    return max_height


def change_height_with_template(mat,tf):
    mat_height = get_pic_height(mat)
    tf_height = get_pic_height(tf)
    if(mat_height==0):
        return 1, mat
    w, h = mat.shape[::-1]
    tw, th = tf.shape[::-1]
    power_y = tf_height/mat_height
    if int(round(h*power_y))<th:
        return 1, mat
    change_mat = cv2.resize(mat, (int(round(w*power_y)), int(round(h*power_y))), interpolation=cv2.INTER_CUBIC)
    return power_y, change_mat


def find_with_template(mat,tf2):
    tw, th = tf2.shape[::-1]
    w, h = mat.shape[::-1]
    if w<tw or h<th:
        return [],1
    threshold = 0.7
    # need change height to the same
    power_y, change_mat = 1, mat
    # power_y, change_mat = change_height_with_template(mat,tf2)
    res1 = cv2.matchTemplate(change_mat, tf2, cv2.TM_CCORR_NORMED)
    # minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res1)
    loc = np.where(res1 >= threshold)
    fix_loc = []
    for pt in zip(*loc[::-1]):
        use_max_location(pt[0], pt[1], res1[pt[1]][pt[0]], fix_loc)
    # need revert x,y location
    revert_loc = []
    while len(fix_loc)>0:
        v = fix_loc.pop()
        v[0] = int(round(v[0] / power_y))
        v[1] = int(round(v[1] / power_y))
        # need check is long line
        change_mat = cv2.dilate(change_mat,box(3,3))
        check_roi = remove_little_rect(change_mat[slice(v[1] + 2, v[1] + th - 6), slice(v[0] + 2, v[0] + tw + 2)])
        # check_roi = remove_little_rect(change_mat[slice(v[1]+2, v[1]+th-4),slice(v[0]+2,v[0]+tw-4)])

        cw, ch = get_mat_width_height(check_roi)
        tcw, tch = get_mat_width_height(tf2)
        if abs(cw-tcw)<tcw/2 and abs(ch-tch)<tch/5:
            revert_loc.insert(0,v)
    return revert_loc,power_y


def check_contour_in_locations(contour, locations, power_y, tf):
    x, y, w, h = contour
    ck_w, ck_h = round(tf.shape[::-1][0]/power_y), round(tf.shape[::-1][1]/power_y)
    for loc in locations:
        ck_x, ck_y, _ = loc
        if x>=ck_x and y>=ck_y and (x+w)<(ck_x+ck_w) and (y+h)<(ck_y+ck_h):
            return  loc


def sort_location_y_x(locations):
    y_min = -15
    sorts = []
    while y_min < 9999:
        y_min = get_sort_y_min(locations, y_min)
        if y_min >= 9999:
            break
        sort_line = []
        for loc in locations:
            if loc[0][1] <= y_min + 15 and loc[0][1]>=y_min:
                sort_line.append(loc)
        line_sorts = sorted(sort_line, key=lambda loc: loc[0][0])
        for loc in line_sorts:
            sorts.append(loc)
    return sorts

def get_sort_y_min(locations, y_min):
    ck_min = 9999
    for loc in locations:
        if loc[0][1]>y_min+15:
            ck_min = min(ck_min, loc[0][1])
    return ck_min

def check_parentheses(mat):
    left_tf = cv2.imread(PARENTHESES_LEFT)
    left_tf = cv2.cvtColor(left_tf, cv2.COLOR_RGB2GRAY)
    left_loc, power_left_y = find_with_template(mat, left_tf)
    right_tf = cv2.imread(PARENTHESES_RIGHT)
    right_tf = cv2.cvtColor(right_tf, cv2.COLOR_RGB2GRAY)
    right_loc, power_right_y = find_with_template(mat, right_tf)
    locations = []
    if len(left_loc) > 0:
        for loc in left_loc:
            locations.append([loc, "0"])
    if len(right_loc) > 0:
        for loc in right_loc:
            locations.append([loc, "1"])
    # just use loc to sort sorted(left_loc, key=lambda location:location[2])
    # order_sorts = sorted(locations, key=lambda location: location[0][0])
    order_sorts = sort_location_y_x(locations)
    # check left has content
    last_has = False
    w, h = mat.shape[::-1]
    if len(order_sorts)>0:
        check_content_roi = mat[slice(0, h), slice(0, order_sorts[0][0][0])]
        last_has = check_roi_has_content(check_content_roi)
    sorts = []
    for loc in order_sorts:
        if loc[1] == "0":
            sorts.append([last_has, loc[0], False, "left"])
            last_has = False
        elif loc[1] == "1":
            sorts.append([last_has, loc[0], False, "right"])
            last_has = False
        else:
            last_has = True
            if len(sorts) > 0:
                sorts[-1][2] = last_has
    # check has content in ( )
    i = 1
    for i in range(1,len(sorts),1):
        if sorts[i-1][3] == "left" and sorts[i][3] == "right":
            x1, y1, x2, y2 = sorts[i-1][1][0], sorts[i-1][1][1], sorts[i][1][0], sorts[i][1][1]
            if abs(y1-y2)>30:
                ck_left_roi = mat[slice(y1,y1+60),slice(x1+28,w)]
                if check_roi_has_content(ck_left_roi):
                    sorts[i - 1][2] = True
                    sorts[i][0] = True
                    continue
                ck_right_roi = mat[slice(y2, y2 + 60), slice(0, x2)]
                if check_roi_has_content(ck_right_roi):
                    sorts[i - 1][2] = True
                    sorts[i][0] = True
                continue
            check_content_roi = mat[slice(sorts[i-1][1][1], sorts[i-1][1][1]+60), slice(sorts[i-1][1][0]+28, sorts[i][1][0])]
            if check_roi_has_content(check_content_roi):
                sorts[i - 1][2] = True
                sorts[i][0] = True
    return sorts, power_left_y, power_right_y

def check_roi_has_content(roi):
    _, contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        if h>20 and w>10:
            return  True
    return  False


def check_is_topic_number(text):
    # //0,字符串，1，阿拉伯数字，2，中文数字，3小括号套阿拉伯数字
    if "一二三四五六七八九十".find(text[0]) >= 0:
        return 2
    elif "0123456789".find(text[0]) >= 0:
        return 1
    return 0


def check_is_first_topic_number(text):
    return "一" == text or "1" == text


def remove_little_rect(mat):
    mat_copy = np.copy(mat)
    mask = cv2.dilate(mat_copy, box(25, 5))
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        if need_remove_little_rect(rect,mat_copy):
            mat_copy[slice(y, y + h), slice(x, x + w)] = 0
    return mat_copy


def need_remove_little_rect(rect, mat):
    x, y, w, h = rect
    roi = mat[slice(y,y+h),slice(x,x+w)]
    ya, xa = np.where(roi > 200)
    if (xa.max() - xa.min()) < 10 and (ya.max() - ya.min()) < 10:
        return True
    return False


def get_first_text_rect(rects, method="top"):
    if method=="top":
        for rect in rects:
            x, y, w, h = rect
            if (h < 20):
                continue
            return rect
    elif method=="left":
        for rect in rects:
            x, y, w, h = rect
            if (w < 10):
                continue
            return rect
    return [0,0,0,0]

def get_first_text_rect2(rects):
    pass


def check_is_dot(index, mat, otext):
    text = re.sub(r'\s', "", otext)
    if(len(text)>index):
        if(text[index]=="." or text[index]=="、"):
            return True
    mat_copy = remove_little_rect(mat)
    img_h, offset_y = get_pic_height_and_offset_y(mat_copy)
    mask = cv2.dilate(mat_copy, box(1, int(round(img_h/2))))
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    (cnts, boundingBoxes) = sort_contours(contours, "left-to-right")
    if(len(boundingBoxes)<=index):
        return False
    x, y, w, h = boundingBoxes[index]
    dot_image = mat[slice(0,y+h), slice(x,x+w)]
    ya, xa = np.where(dot_image > 200)
    if (xa.max()-xa.min()) < img_h / 2 and (ya.max()-ya.min()) < min(20,img_h / 2) and (ya.min() - offset_y) > img_h / 3:
        #if w<img_h/2 and h<img_h/2 and (y-offset_y)>img_h/2:
        return True
    return False


def get_topic_text(hash):
    #  //0,字符串，1，阿拉伯数字，2，中文数字，3小括号套阿拉伯数字
    #  {"text": "", "type": 99, "positionX": loc[0], "positionY": loc[1]}
    v2t = "一二三四五六七八九十"
    if hash["type"] == 0:
        return hash["text"]
    elif hash["type"] == 1:
        return hash["text"]
    elif hash["type"] == 2:
        if len(hash["text"]) == 1:
            if v2t.find(hash["text"])>=0:
                return str(v2t.index(hash["text"])+1)
        else:
            if v2t.find(hash["text"][1]) >= 0:
                return str(v2t.index(hash["text"][1])+11)
    return hash["text"]


def text_to_number(text,type):
    return get_topic_text({"type":type,"text":text})


def check_is_topic(text,mat,first_text,max_length=999):
    #//0,字符串，1，阿拉伯数字，2，中文数字，3小括号套阿拉伯数字, 4小括号套中文数字
    # is_topic, topic_number, number_type, has_dot
    r = [ False, "", 0, False ]
    text = text.strip()
    if len(text)==0:
        return r
    if len(text)>max_length:
        return r
    # 1 -> [ True, "1", 1, False]
    # 1. -> [ True, "1", 1, True]
    # (1)-> [ True, "1", 3, False]
    # 1A -> [ True, "1", 1, False]
    # 12 -> [ True, "12", 1, False]
    # 12. -> [ True, "12", 1, True]
    first_ck = check_is_topic_number(text[0])
    if first_text == "(X)":
        first_ck = first_ck+2  # (1)
    if first_ck>0:
        first_dot = check_is_dot(1, mat, text)
        if len(text) == 1:
            return [True, text[0], first_ck, first_dot]  # 1
        if first_dot:
            return [True, text[0], first_ck, first_dot]  # 1.
        else:
            second_ck = check_is_topic_number(text[1])
            if second_ck>0:
                second_dot = check_is_dot(2, mat, text)
                return [True, text[0:2], first_ck, second_dot]  # 12.
            else:
                return [True, text[0], first_ck, False]  # 1A
    else:
        return  r  # A


def convert_px2percent(px, total):
    if total == 0:
        return px
    return int(px*10000/total)


def convert_3channels(mat, front_color, background_color):
    ms = []
    for i in range(0,5,2):
        fc = int(front_color[i:i+2],16)
        bc = int(background_color[i:i+2],16)
        r = np.copy(mat)
        r[np.where(mat>200)]=fc
        r[np.where(mat<=200)]=bc
        ms.append(r)
    return cv2.merge(ms[::-1])


def add_padding_roi(roi, left=0, right=0, top=0, bottom=0, fill=0):
    w, h = roi.shape[::-1]
    n = np.zeros((h+top+bottom, w+left+right), dtype=np.uint8)
    if fill!=0:
        n=fill
    n[slice(top, top+h),slice(left,left+w)]=roi
    return n


def merge_two_mat(mat1, mat2):
    w1,h1 = mat1.shape[::-1]
    w2,h2 = mat2.shape[::-1]
    n = np.zeros((h1+h2,max(w1,w2)), dtype=np.uint8)
    n[slice(0,h1+h2),slice(0,max(w1,w2))] = 255
    n[slice(0,h1),slice(0,w1)]=mat1
    n[slice(h1,h1+h2),slice(0,w2)]=mat2
    return n


def get_most_min_x(data):
    hash = {"0":0}
    v = sorted(data)
    x_min = -15
    sorts = []
    while x_min < 9999:
        x_min = get_sort_x_min(v, x_min)
        if x_min >= 9999:
            break
        sort = []
        for loc in v:
            if loc <= x_min + 15 and loc>= x_min:
                sort.append(loc)
        sort_list = sorted(sort)
        sorts.append([sort_list[0],len(sort_list)])
    return sorted(sorts, key=lambda loc: loc[1])[-1]

def get_sort_x_min(data, x_min):
    ck_min = 9999
    for loc in data:
        if loc>=x_min+15:
            ck_min = min(ck_min, loc)
    return ck_min


def check_is_html_code(mat):
    # (40    left parenthesis
    #  )    41    right    parenthesis
    # < 60    less - than
    # =    61    equals - to
    # > 62    greater - than
    # ✔	10004	2714
    # ✕	10005	2715
    for root, dirs, files in os.walk("xxy/html_code"):
        for file in files:
            name, _ = os.path.splitext(file)
            img = cv2.imread(os.path.join(root, file))
            tf = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            loc, _ = find_with_template(mat, tf)
            if len(loc)>0:
                return name
    return None

def check_most_left(img):
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 101, 25)
    iw, ih = img.shape[::-1]
    roi = img[slice(0, ih), slice(0, int(iw / 10))]
    roi = cv2.dilate(roi, box(25, 15))
    _, contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours = sort_contours(contours, "top-to-bottom")
    left = []
    for contour in contours:
        x, y, w, h = contour
        if h > 30 and h < 110 and w > 45 and w < 300:
            left.append([x])
            continue
        # else:
        #     left.append([0])
        roi[slice(y, y + h), slice(x, x + w)] = 0

    if len(left)==0:
        most_left = 30
    else:
        most_left = sorted(left)[0][0]
    #     return most_left
    # most_left = sorted(left)[0][0]
    return most_left

def w(mat,name):
    cv2.imwrite('tmp/'+str(name)+'.jpg',mat)

class DD():
    def __init__(self, n="__"):
        # _p 最后一次的Mat值， n 图片主名 f 处理方法名 l1 第一层 l2 第二层
        self._p, self.n, self.f, self.l1, self.l2, self.skip, self.increase = None, n, "_", 0, 0, False, 1

    @property
    def p1(self):
        return self._p

    @p1.setter
    def p1(self, p):
        self._p = p
        self.l1 += 1
        if self.l2 > 0:
            self.f = ""
        self.l2 = 0
        self.write()

    @p1.deleter
    def p1(self):
        del self._p

    @property
    def p2(self):
        return self._p

    @p2.setter
    def p2(self, p):
        self._p = p
        self.l2 += 1
        self.write()

    @p2.deleter
    def p2(self):
        del self._p

    def write(self):
        if self.skip:
            pass
        else:
            #cv2.imwrite("output/tmp/%s.z.%s.%s.%s.png" % (self.n, str(self.l1).zfill(2), str(self.l2).zfill(2), self.f), self._p)
            cv2.imwrite("tmp/%s.z.%s.%s.%s.png" % (self.n, str(self.l1).zfill(2), str(self.l2).zfill(2), self.f),self._p)

    def write_auto(self,mat,path,rpath):
        self.increase += 1
        file_name = self.n+"_"+str(self.increase).zfill(4)+".png"
        mw,mh = mat.shape[::-1]
        clear = remove_little_rect(mat)
        mask = cv2.dilate(clear, box(25, 25))
        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        x1,y1,x2,y2=9999,9999,0,0
        for contour in contours:
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect
            x1 = min(x1,x)
            x2 = max(x2,x+w)
            y1 = min(y1,y)
            y2 = max(y2,y+h)
        write=mat
        if x1==9999 or y1==9999:
            pass
        else:
            write=clear[slice(y1,y2),slice(max(0,x1-10),min(mw,x2+10))]
        c3 = convert_3channels(write, "0e3655", "f8f9fe")
        cv2.imwrite(path+rpath+file_name, c3)
        w,h = write.shape[::-1]
        return file_name,w,h