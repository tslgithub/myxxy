import base64
import os
import skimage.io
import json
import cv2
# import tools
import shutil
# import base64

ROOT_DIR = os.getcwd()
json2_path = os.path.join(ROOT_DIR,'json2/')
if not os.path.exists(json2_path):
    os.mkdir(json2_path)

for root,dirs,files in os.walk(os.path.join(ROOT_DIR,'json/')):
    files.sort()

    for file in files:
        name,_ = os.path.splitext(file)
        if file.endswith('.'
                         'json'):
            img = cv2.imread(os.path.join(ROOT_DIR,'pic/'+name+'.jpg'),0)
            # ada = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,101,25)
            image = cv2.imencode('.jpg', img)[1]
            base64_data = str(base64.b64encode(image))[2:-1]

            # with open(base64_data,'rb') as f:
            #     base64_data = base64.b64encode(f.read())
                # cv2.ad
            with open(os.path.join(ROOT_DIR,'json/'+name+'.json'),'r') as f:
                js=json.load(f)
                js['imageData'] = str(base64_data).replace('b\'','').replace('\'','')
                # print(js)
                fs = json.dumps(js, ensure_ascii=False)

            fo = open(os.path.join(ROOT_DIR, 'json2/' + name + '.json'), 'w+', encoding='utf-8')
            fo.write(fs)
            fo.close()

# shutil.move(os.path.join(ROOT_DIR,'json2/*.json'),os.path.join(ROOT_DIR,'json/'))