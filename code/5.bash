#!/bin/bash
i=1
for i in /home/xxy/data_maskrcnn/0628_0625_0621/json/*.json
do 
	labelme_json_to_dataset $i
#	i=i+1
done

