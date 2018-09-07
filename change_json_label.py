import cv2
import os
import json
import encodings
import io

# root_path = os.getcwd()

# data_path = os.path.join(root_path,'pre_data_train/')

def change_file_name(root_path):
    i = 0
    for root,dirs,files in os.walk(root_path):
        files.sort()
        for file in files:
            if file.endswith('_.json'):
                i+=1
                file_name = file.split('_.json')[0]
                tmp = file_name.split('_')[:3]
                file_time = tmp[0]+'_'+tmp[1]+'_'+tmp[2]
                src = os.path.join(root_path,file)
                dst = os.path.join(root_path,file_time+'_'+str(i)+'.json')
                os.rename(src,dst)
                src_png = os.path.join(root_path,file.replace('_.json','_.png'))
                dst_png = os.path.join(root_path,file_time+'_'+str(i)+'.png')
                os.rename(src_png,dst_png)

def change_json_imagePath(root_path):
    Files = []
    for root,dirs,files in os.walk(root_path):
        for file in files:
            if file.endswith('.json'):
                Files.append(file)

        files = sorted(Files, key=lambda b: (int(b.split('_')[-1].split('.')[0])))
        # print(files)

        # continue
        for file in files:
            if file.endswith('.json'):
                name = file.replace('.json','.png')
                print('name = ',name)
                # if int(name.split('_')[-1].replace('.png','')) != 75:
                #     continue
                with open(os.path.join(root,file)) as f:
                    js = json.load(f)
                    js['imagePath'] = name
                print('name = ',name)
                fo = open(os.path.join(root,file),'w+',encoding='utf-8')
                fs = json.dumps(js,ensure_ascii=False)
                fo.write(fs)
                fo.close()

def remove_little_rec(root_path):
    flag = False
    for root,dirs,files in os.walk(root_path):
        for file in files:
            if file.endswith('.json'):
                # if file != '2018_7_28_92.json':
                #     continue
                i = 0
                with open(os.path.join(root_path,file)) as f:
                    js=json.load(f)
                    for shapes in js['shapes']:
                        # if flag != True:
                        if len(shapes['points'])<5:
                            js['shapes'].pop(i)
                        i+=1

                fo = open(os.path.join(root_path,file),'w+',encoding='utf-8')
                fs = json.dumps(js,ensure_ascii=False)
                fo.write(fs)
                fo.close()

root_path = './train_label_0906/'
# change_file_name(root_path)
# change_json_imagePath(root_path)
remove_little_rec(root_path)


            # if file.endswith('_.json'):
#             with open(os.path.join(root_path,file)) as f:
#                 js = json.load(f)
#
#                 if 'fault'  in js['label']:
#                     js['label'] = 'fault'
#                 if 'right' in js['label']:
#                     js['label'] = 'right'
#             # print((os.path.join(data_path,file)))
#             fo = io.open((os.path.join(root_path,file)), 'w+', encoding='utf-8')
#
#             fs = json.dumps(js, ensure_ascii=False)
#             fo.write(fs)
#             fo.close()
# #







# for root,dirs,files in os.walk(data_path):
#     files.sort()
#     for file in files:
#         if file.endswith('.json'):
#             # num = 1
#             with open(os.path.join(data_path,file)) as f:
#                 js = json.load(f)
#                 print( js['imagePath'])
