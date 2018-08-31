import os
import shutil

root_path = os.getcwd()

data = os.path.join(root_path,'data/')
js_path = os.path.join(root_path,'json/')
pic_path = os.path.join(root_path,'pic/')

# json2 = os.path.join(root_path,'josn2')
# if os.path.exists(json2):
#     os.mkdir(json2)

# start = (input('imput your start path: '))
# for start in range(0,10):
#     start = str(start)
#     ans_path = os.path.join(root_path,'mnist'+'/'+start+'/')

for img in os.listdir(data):
    if img.endswith('.png'):
        shutil.move(data+img,pic_path)
    if img.endswith('.json'):
        shutil.move(data+img,js_path)

        # pass
        # name = os.path.splitext(img)[0]
        # # name = start
        # src = os.path.join(ans_path,name+'.png')
        # dst = os.path.join(ans_path,start+"_"+name+'.png')
        # os.rename(src,dst)
    # start+=1