# coding: utf-8
# 8bit to 16 bit

import cv2
import os

# 16bit to 8bit

root_path = os.getcwd()
js_path = os.path.join(root_path,'json/')
aa_path = os.path.join(root_path,'aa/')

if not os.path.exists(aa_path):
    os.mkdir(aa_path)

i=0
for root,dirs,files in os.walk(js_path):
    # dirs = sorted(dirs,key=lambda b:b.replace('_json',''))
    for dir in dirs:
        i+=1
        name = dir.split('_json')[0]
        # print (name)
        # if name != 103:
        #     continue
        img16 = cv2.imread(js_path + dir+"/label.png", -1)
        # print (img16.dtype)
        img8 = (img16/256).astype('uint8')
        # print (img8.dtype)
        if str(img8.dtype) != 'uint8':
            print (name ,' is not uint8')
        # print ('------------'+str(i)+'----------------'+name)
        cv2.imwrite(os.path.join(aa_path,name+'.png'), img8)

        # for file in dir:
        #     if file.endswith('.png'):



#
# img8 = (img/256).astype('uint8')
#
# cv2.imwrite("./output/8bit.png",img8)
