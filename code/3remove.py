# coding = utf-8

# remove js by pic and remove pic by js

import os
import shutil

root_dir = os.getcwd()

img_path = root_dir+'/pic/'
js_path = root_dir+'/json/'

def remove_pic_by_json(img_path,js_path):
    js = os.listdir(js_path)
    for pic in os.listdir(img_path):
        name,_ = os.path.splitext(pic)
        if name+".json"  not in js:
            os.remove(os.path.join(img_path,name+".png"))
            print ('remove ',name+".png")

def remove_js_by_pic(img_path,js_path):
    pic = os.listdir(img_path)
    for js in os.listdir(js_path):
        name,_ = os.path.splitext(js)
        if name+'.png' not in pic:
            os.remove(os.path.join(js_path,name+'.json'))
            print ('remove ',name+".json")

img_num = len(os.listdir(img_path))
js_num = len(os.listdir(js_path))


#pre delete, consider the equal num between js and pic
# pic = os.listdir(img_path)
# for js in os.listdir(js_path):
#     name, _ = os.path.splitext(js)
#     if name + '.png' not in pic:
#         os.remove(os.path.join(root_dir, name + '.json'))

# js_num = 0
# # def move(img_path,js_path):
# if not os.path.exists(os.path.join(root_dir,'/josn_file/')):
#     os.system('sudo mkdir ----')
#     # js_file = os.mkdirs(os.path.join(root_dir,'/josn_file/'))


# for file in os.listdir(js_path):
#     if file.endswith('_json'):
#         shutil.move(file,js_file)


if img_num > js_num:
     remove_pic_by_json(img_path,js_path)
if img_num < js_num:
    remove_js_by_pic(img_path,js_path)


#for js2 in os.listdir(js_path):
#    if js2.endswith('_json'):
#        js_name = js2.split('_')[0]
#        pic2 = os.listdir(img_path)
#        if js_name+'.png' not in pic2:
#            print (js_name,' has error')

