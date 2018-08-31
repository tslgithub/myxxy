import os
import shutil


root_dir = os.getcwd()
js_path = os.path.join(root_dir,'json/')
pic_path = os.path.join(root_dir,'pic/')
aa_path = os.path.join(root_dir,'aa/')


for root,dirs,files in os.walk(js_path):
    for dir in dirs:
        length = os.listdir(os.path.join(js_path,dir))
        if len(length) ==0:
            name = dir.split('_')[0]
            # os.remove(os.path.join(js_path,dir))
            os.remove(os.path.join(js_path,name+'.json'))
            os.remove(os.path.join(pic_path,name+'.png'))
            os.remove(os.path.join(aa_path,name+'.png'))
            print (name ,'removed')

        # if 改改改改改改改改改改改改改改改改改改改改改改改改改



# class remove(self,img_path,js_path):
#     def remove_pic_by_json(img_path, js_path):
#         js = os.listdir(js_path)
#         for pic in os.listdir(img_path):
#             name, _ = os.path.splitext(pic)
#             if name + ".json" not in js:
#                 os.remove(os.path.join(img_path, name + ".png"))
#
#     def remove_js_by_pic(img_path, js_path):
#         pic = os.listdir(img_path)
#         for js in os.listdir(js_path):
#             name, _ = os.path.splitext(js)
#             if name + '.png' not in pic:
#                 os.remove(os.path.join(js_path, name + '.json'))
#
#     img_num = len(os.listdir(img_path))
#     js_num = len(os.listdir(js_path))

# length = os.listdir('/home/xxy/data_maskrcnn/data20180626/json/321_json')
# if len(length) ==0:
#     print ('skdjfa')