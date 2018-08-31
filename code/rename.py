import json
import os
import cv2
# import tools
import numpy as np
import base64

root_path = os.getcwd()

pic_path = os.path.join(root_path,'pic/')
if not os.path.exists(pic_path):
    os.mkdir(pic_path)
js_path = os.path.join(root_path,'json/')
if not os.path.exists(js_path):
    os.mkdir(js_path)

# for root,dirs,files in os.walk(root_path):
#     # if dir.startswith('for')
#         for dir in dirs:
#             # if dir.startswith('for'):
#             if dir.startswith('for'):
#                 dir_name = dir.split('_')[-1]
#                 for file in os.listdir(os.path.join(root_path,dir)):
#                     if file.endswith('.png'):
#                         file_name = file.split('.')[0]
#                         src = os.path.join(root_path, dir + '/'+file)
#                         dst = os.path.join(pic_path,dir_name+'_'+file_name+'.png')
#                         os.rename(src,dst)
#                     if file.endswith('.json'):
#                         file_name = file.split('.')[0]
#                         src = os.path.join(root_path, dir + '/' + file)
#                         dst = os.path.join(js_path, dir_name + '_' + file_name + '.json')
#                         os.rename(src,dst)

js_path = '/home/xxy/data_maskrcnn/0628_0625_0621/json'
for js_file in os.listdir(js_path):
    print (js_file+' is done')
    js_name = js_file.split('.')[0]
    origin = cv2.imread(pic_path+js_name+'.png')
    image = cv2.imencode('.png',origin )[1]
    base64_data = str(base64.b64encode(image))[2:-1]

    with open(js_path+'/'+js_file,'r') as f:
        js = json.load(f)
        js['imagePath'] =js_name+ '.png'
        js['imageData'] = str(base64_data).replace('b\'','').replace('\'','')
        fs = json.dumps(js, ensure_ascii=False)

    fo = open(os.path.join(root_path+'/json2/'+js_file),'w+', encoding='utf-8')
    fo.write(fs)
    fo.close()
    print(js_name+' is Done.')

# img_path = '/home/xxy/data_maskrcnn/0628_0625_0621/for_labelme_0629'
# def cvt(img_path):
#     for img in os.listdir(img_path):
#         if img.endswith('.png'):
#             image= cv2.imread(img_path+'/'+img,0)
#             name = img.split('.')[0]
#             cv2.imwrite('/home/xxy/data_maskrcnn/0628_0625_0621/0625/'+name+'.png',image)


#  /home/xxy/data_maskrcnn/0628_0625_0621/json2/0621_016.json
#
# cvt(img_path)

