# import pylab as py
# import time
# from pylab import *
# from matplotlib.font_manager import FontProperties
# import matplotlib.pyplot as plt
#
# font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
#
# def readdata(ls):
#     l = ls.split(',')
#     if len(l)>2:
#         return [l[0],l[1]]
#     else:
#         return None
#
# if "__main__"==__name__:
#     print(9)
#     file_obj=open('fanmaker.txt')#target point data file
#     k=0
#     line=file_obj.readline()
#     polygon =[]
#     while line:
#             k+=1
#             px=[]
#             py=[]
#             while line:
#                 row = readdata(line)
#                 print (line)
#                 px.append(row[0])
#                 py.append(row[1])
#                 line=file_obj.readline()
#                 if line=='\n':
#                     ps=[]
#                     px.append(px[0])
#                     py.append(py[0])
#                     ps.append(px)
#                     ps.append(py)
#                     polygon.append(ps)
#                     line=file_obj.readline()
#                     break
#     x=np.array(polygon[0][0])
#     y=np.array(polygon[0][1])
# ##    plt.fill(x,y,'b')
#     plt.plot(x,y,'b-', linewidth=2)
#     for i in range(len(polygon)-1):
#         x=np.array(polygon[i+1][0])
#         y=np.array(polygon[i+1][1])
# ##        plt.fill(x,y,'b')
#         plt.plot(x,y,'r-', linewidth=2)
#         plt.hold(True)
# ##    plt.show()
#
#     x1=[-0.5 ,1.5]
#     x2=[-0.5,-0.5]
#     x3=[1.5 ,-0.5]
#     x4=[1.5,1.5]
#     plt.plot(x1,x2,'-')
#     plt.plot(x2,x3,'-')
#     plt.plot(x3,x4,'-')
#     plt.plot(x4,x1,'-')
#     plt.axis([-0.5,1.5 ,-0.5,1.5])
#     plt.show()
#     #     plt.axis('tight')
#     file_obj.close()

import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import json
import tools

right_path = os.path.join(os.getcwd(),'right')
fault_path = os.path.join(os.getcwd(),'fault')
if not os.path.exists(right_path):
    os.mkdir(right_path)
if not os.path.exists(fault_path):
    os.mkdir(fault_path)

for root,dirs,files in os.walk('./train_label_0906/'):

    Files = []
    for root, dirs, files in os.walk('./train_label_0906/'):
        for file in files:
            if file.endswith('.json'):
                Files.append(file)

        files = sorted(Files, key=lambda b: (int(b.split('_')[-1].split('.')[0])))


    for file in files:
        i=0


        if file.endswith('.json'):
            name = os.path.splitext(file)[0]
            # if name != '2018_7_27_78':
            #     continue
            print('name = ',name)
            tmp = int(name.split('_')[-1])
            if tmp<= 76:

                continue
            # if name != '2018_7_27_75':
            #     continue
            with open(os.path.join(root,file)) as f:
                js  = json.load(f)
                # print(js['shapes'])
                # x,y = [],[]
                for shapes in js['shapes']:
                    i+=1
                    # print(shapes['points'])
                    if len(shapes['points']) == 0:
                        continue
                    # print(shapes['label'])

                    if shapes['label'] == 'right':
                        save_file = right_path
                    if shapes['label'] == 'fault':            
                        save_file = fault_path
                    target_point = np.array([shapes['points']], dtype = np.int32)

                    target_label = shapes['label']
                    x = np.array(shapes['points'], dtype = np.int32)[:,0]
                    y = np.array(shapes['points'], dtype = np.int32)[:,1]


                    rx2,rx1,ry2,ry1 = target_point[0][:,0].max(),target_point[0][:,0].min(),\
                                      target_point[0][:,1].max(),target_point[0][:,1].min()

                    if (rx2 - rx1) <=0 or (ry2 - ry1) <=0:
                        print('name has error :',name)
                        continue
                    # print(name)
                    img = cv2.imread(os.path.join('./train_label_0906/',js['imagePath']))
                    roi = img[slice(ry1,ry2),slice(rx1,rx2)]#,dtype=np.uint32
                    # mask = np.asarray(mask,dtype=np.uint16)
                    target_point = np.array([list((zip(
                        target_point[0][:, 0] / ((target_point[0][:, 0]).max()) * x.max() - x.min(),
                        target_point[0][:, 1] / (target_point[0][:, 1].max()) * y.max() - y.min())))])
                    background = np.zeros_like(roi,dtype = np.int32)
                    # w,h,_ = background.shape()
                    mask = cv2.fillPoly(background, target_point.astype(int) + 1, (255, 0, 0))
                    cv2.imwrite(os.path.join(save_file, name + '_' + 'x=' + str(x[0]) + '_y=' + str(y[0]) + '_.png'),
                                mask*0.5+roi*0.5)



# a = np.array([[[10,10], [100,10], [100,100], [10,100]]], dtype = np.int32)
# b = np.array([[[100,100], [200,230], [150,200], [100,220]]], dtype = np.int32)
# print(a.shape)
# im = np.zeros([240, 320], dtype = np.uint8)
# cv2.polylines(im, a, 1, 255)
# cv2.fillPoly(im, b, 255)
# plt.imshow(im)
# plt.show()