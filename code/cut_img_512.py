import cv2
import os
import tools

root_path = os.getcwd()

part_img_path = os.path.join(os.getcwd(),'part_img/')

if  not os.path.exists(part_img_path):
    os.mkdir(part_img_path)

NUM = 0
cut_sizt = 512

path = os.path.join(os.getcwd(),'20180625/')#gai

for root,dirs,files in os.walk(path):
    for file in files:
        gray = cv2.imread(os.path.join(root,file), 0)
        ada = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 101, 25)
        # img = cv2.imread(path,0)

        W,H = ada.shape[::-1]
        print (W,H,int(2048/W*H))
        # print (int(2048/W*H))
        img = cv2.resize(ada, (2048, int(2048/W*H) ))
        W,H = img.shape[::-1]
        central = [int(W/2),int(H/2)]
        ww,hh= int(W/2),int(H/2)
        # nw,nh = img.shape[::-1]
        hc = int(H/512)
        wc = int(W/512)

        for h in range(hc):
            for w in range(wc):
                flag = 1

                if ww - 512*(w+1)>0 and hh -512*(h+1) >0:
                    part = img[slice(hh - 512*(h+1), hh - 512*h ) ,slice(ww-512*(w+1),ww-w*512)]
                    NUM+=1
                    cv2.imwrite(part_img_path+str(NUM) + ".png", part)

                if ww + 512*(w+1)<W and hh - 512*(h+1) >0:
                    part = img[slice(hh - 512*(h+1), hh - 512*h ) ,slice( ww+512*(w),ww+(w+1)*512)]
                    NUM += 1
                    cv2.imwrite(part_img_path+str(NUM) + ".png", part)


                if ww - 512*(w+1)>0 and hh + 512*(h+1) < H:
                    part = img[slice(hh + 512*(h), hh + 512*(h+1) ) ,slice(ww-512*(w+1),ww-w*512)]
                    NUM += 1
                    cv2.imwrite(part_img_path+str(NUM) + ".png", part)

                if ww + 512*(w+1)<W and hh + 512*(h+1) < H:
                    part = img[slice(hh + 512*(h), hh + 512*(h+1) ) ,slice( ww+512*(w),ww+(w+1)*512)]
                    NUM += 1
                    cv2.imwrite(part_img_path +str(NUM)+ ".png", part)
