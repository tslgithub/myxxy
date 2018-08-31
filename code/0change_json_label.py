import cv2
import os
import json

root_path = os.getcwd()
data_path = os.path.join(root_path,'json/')

for root,dirs,files in os.walk(data_path):
    files.sort()
    for file in files:
        if file.endswith('.json'):
            num = 1
            with open(os.path.join(data_path,file)) as f:
                js = json.load(f)
                for shape in js['shapes']:
                    shape['label'] = shape['label']+str(num)
                    # js['shapes'][num]['label'] = js['shapes'][num]['label']+str(num)
                    num+=1

            fo = open((os.path.join(data_path,file)), 'w+', encoding='utf-8')
            fs = json.dumps(js, ensure_ascii=False)
            fo.write(fs)
            fo.close()

for root,dirs,files in os.walk(data_path):
    files.sort()
    for file in files:
        if file.endswith('.json'):
            num = 1
            with open(os.path.join(data_path,file)) as f:
                js = json.load(f)
                for shape2 in js['shapes']:
                    print (file,'    ',shape2['label'])