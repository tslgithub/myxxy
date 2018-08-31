import json
import os
import base64

# imageData = base64.b64encode(imageData)
root_path = os.getcwd()
js_path = os.path.join(root_path,'json/')
pic_path = os.path.join(root_path,'pic/')

json2 = os.path.join(root_path,'josn2')
if os.path.exists(json2):
    os.mkdir(json2)

# for js in os.listdir(js_path):
for root,dirs,files in os.walk(js_path):
    files.sort()
    for js in files:
        js_name = os.path.splitext(js)[0]
        # for pic in os.listdir(pic_path):
        for pic in sorted(os.listdir(pic_path),key=lambda b:int(b.split('.')[0])):
        # for root2,dirs2,files2 in os.w
        #     pic_name = os.path.splitext(os.path.join(pic_path,pic))[0]
            pic_name = os.path.splitext(pic)[0]
            if js_name == pic_name:
                # pass
                with open(os.path.join(pic_path,pic),'rb') as img:
                    imageData = base64.b64encode(img.read())
                with open(os.path.join(js_path,js),'r') as f:
                    js_data = json.load(f)
                js_data['imageData'] = imageData
                fo = open((json2+'/'+js),'w+', encoding='utf-8')
                fs = json.dumps(js_data,ensure_ascii=False)
                fo.write(fs)
                fo.close()


                # with open(os.path.join(js_path, js), 'w') as j:
                #     json.dumps(j,js_data)

    # with open(os.path.join(js_path,js_file)) as f:
    #     js = json.loads(f)

