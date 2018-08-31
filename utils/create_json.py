import os
import cv2
import base64
import json
import io

#python2 env
def create_json(target,image_name,image_root_dir):
    root_path = os.getcwd()
    img = cv2.imread(image_name)
    
    #target example,first '2' means label
    #[[2, [[[588, 486]], [[572, 485]] ,[[598, 436]], [[555, 185]] ]]]

    # ada = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 101, 25)
    image = cv2.imencode('.png', img)[1]

    with open(image_name,'rb') as f:
        base64_data = base64.b64encode(f.read())
    # print('target = ',target)

    imagePath = image_name.split('/')[-1]
    imagePath = ''.join(imagePath)
    # print('imagePath = ',imagePath)
    json_name = imagePath.replace('png','json')

    shapes=[]

    for item in target:

        label_number=item[0]

        if label_number==1:
            label = 'fault'
        else:
            label = 'right'

        points,_ = [],[]
        
        for item1 in item[1]:
            points.append(item1[0])

        shapes.append(
            {
            "line_color":None, 
            "fill_color": None,
            "points":points,
            "label":label
        }
        )
      
    js = {"imagePath":imagePath,
        # "imageData":'',
        "imageData":base64_data,
        "shapes":shapes,
        "fillColor": [255, 0, 0, 128],
        "lineColor": [0, 255, 0, 128],
        "flags":{}
    }

    fo = open(image_root_dir + json_name, "w")

    fs = json.dumps(js, ensure_ascii=False)
    fo.write(fs)
    fo.close()