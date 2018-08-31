import json
import os
import shutil

root_dir = os.getcwd()
js_path = os.path.join(root_dir,'json/')
pic_path = os.path.join(root_dir,'pic/')

if not os.path.exists(js_path):
    os.mkdir(js_path)
if not os.path.exists(pic_path):
    os.mkdir(pic_path)

# file_name = 0
# 移动.json文件到json文件夹, 移动.jpg文件到pic文件夹



# for file_name in range(0,10):
#     for root,dirs,files in os.walk('mnist/'+(str(file_name))+'/'):
#         print ('mnist/'+(str(file_name))+'/')
#         for file in files:
#             if file.endswith('.json'):
#                 name = int(file.split('.')[0])
#
#                 # os.rename()
#                 shutil.move(os.path.join(root_dir,root+file),js_path)
#             if file.endswith('.png'):
#                 shutil.move(os.path.join(root_dir,root+file),pic_path)


#删除json文件中shapes为空的文件
js_file = os.listdir(js_path)
for js in js_file:
    if js.endswith('.json'):
        with open(os.path.join(js_path,js)) as f:
            j = json.load(f)
            if len(j['shapes']) ==0:
                os.remove(os.path.join(js_path,js))
                print('-------------')
    # if j['shape']


# os.path.getsize('/home/xxy/data_maskrcnn/data20180626/json/321_json')