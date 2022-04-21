# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 09:00:44 2021

@author: wes
"""



#!/usr/bin/env python3
# WES 
# this skript takes the filtered files per scene (where annotations for categories that should be excluded
# where deleted), and concatenates them to one big file. The files for each scene that are used here,
# results from the script filterScannetAnnotations.py.
# For concatenation, we do a json concat for the first elements, but for the huge element "annotations" 
# a simple string concat (adding block by block to the result file) is done. in this script NO 
# reductions for images or annotations are done


from os import listdir
import json
import os
import sys


DATABASE = "SCANNET"#"MSCOCO"


ANNOTATIONFILE_PREFIX = "train"
#ANNOTATIONFILE_PREFIX = "val"
#ANNOTATIONFILE_PREFIX = "test"

TOLERANCE = 5

def main():

    # category_string = '{"categories": [{"supercategory": "shape", "id": 1, "name": "garbage bin"}, \
    #     {"supercategory": "shape", "id": 2, "name": "pillow"}, \
    #     {"supercategory": "shape", "id": 3, "name": "ceiling"}, \
    #     {"supercategory": "shape", "id": 4, "name": "doorframe"}, \
    #     {"supercategory": "shape", "id": 5, "name": "lamp"}, \
    #     {"supercategory": "shape", "id": 6, "name": "mirror"}, \
    #     {"supercategory": "shape", "id": 7, "name": "whiteboard"}, \
    #     {"supercategory": "shape", "id": 8, "name": "radiator"}, \
    #     {"supercategory": "shape", "id": 9, "name": "night stand"}, \
    #     {"supercategory": "shape", "id": 10, "name": "stool"}, \
    #     {"supercategory": "shape", "id": 11, "name": "telephone"}, \
    #     {"supercategory": "shape", "id": 12, "name": "microwave"}, \
    #     {"supercategory": "shape", "id": 13, "name": "board"}, \
    #     {"supercategory": "shape", "id": 14, "name": "shower wall"} \
    #     ]}'
                                        

    category_string = '{"categories": [{"supercategory": "shape", "id": 1, "name": "wall"}, \
        {"supercategory": "shape", "id": 2, "name": "floor"}, \
        {"supercategory": "shape", "id": 3, "name": "cabinet"}, \
        {"supercategory": "shape", "id": 4, "name": "bed"}, \
        {"supercategory": "shape", "id": 5, "name": "chair"}, \
        {"supercategory": "shape", "id": 6, "name": "sofa"}, \
        {"supercategory": "shape", "id": 7, "name": "table"}, \
        {"supercategory": "shape", "id": 8, "name": "door"}, \
        {"supercategory": "shape", "id": 9, "name": "window"}, \
        {"supercategory": "shape", "id": 10, "name": "bookshelf"}, \
        {"supercategory": "shape", "id": 11, "name": "picture"}, \
        {"supercategory": "shape", "id": 12, "name": "counter"}, \
        {"supercategory": "shape", "id": 14, "name": "desk"}, \
        {"supercategory": "shape", "id": 16, "name": "curtain"}, \
        {"supercategory": "shape", "id": 24, "name": "refridgerator"}, \
        {"supercategory": "shape", "id": 28, "name": "shower curtain"}, \
        {"supercategory": "shape", "id": 33, "name": "toilet"}, \
        {"supercategory": "shape", "id": 34, "name": "sink"}, \
        {"supercategory": "shape", "id": 36, "name": "bathtub"}, \
        {"supercategory": "shape", "id": 39, "name": "otherfurniture"} \
        ]}'
                                        
    print(category_string)
    data_cat = json.loads(category_string)

    info_added = False
    
    OUTPUT_DIR = os.path.join("D:/Atlantis/ScannetSamples/annotations/tmpOutput/")
    INPUT_DIR = "D:\\Atlantis\\ScannetSamples\\tmpOutput\\scannetFilteredImages_filtered_trainFiles\\"

    
    json_file_concat = ANNOTATIONFILE_PREFIX + "-tol5-scannet-v2.json"
                        
    annotation_file_result_path = os.path.join(OUTPUT_DIR,json_file_concat)

    try:
        os.mkdir(OUTPUT_DIR)
    except:
        print("Directory <"+OUTPUT_DIR+"> already exist")
    
    

    processedSceneIndex = -1
    sceneList = listdir(INPUT_DIR)

    for filename in sceneList:
     
        if filename.find(ANNOTATIONFILE_PREFIX +"-tol5-") < 0:
            continue
        
        if filename.find("scannet-v2") >= 0:
            continue
        
        processedSceneIndex = processedSceneIndex + 1
        
        if (ANNOTATIONFILE_PREFIX == "train"):
            SCENE = filename[11:-5]  
        else:
            SCENE = filename[9:-5]

        if (ANNOTATIONFILE_PREFIX == "test"):
            SCENE = filename[10:-5]  
            
        print("scene: " + SCENE)
        
        

        ANNOTATION_FILE = ANNOTATIONFILE_PREFIX+"-tol"+str(TOLERANCE)+"-"+SCENE+".json" 

    
        json_file = ANNOTATION_FILE #"train-tol2-scene0191_00.json"        
        json_file_path = os.path.join(INPUT_DIR, json_file)
              
        
        with open(json_file_path) as json_file:
            # all data from the json file
            data = json.load(json_file)
            #print(data)
            
        element_images = data["images"]   
        
        if len(element_images) == 0:
            continue
        
        if not info_added:
            del data["images"]
            del data["annotations"]
            
            with open(annotation_file_result_path,"a") as ann_file:
                ann_file.writelines("{")
                ann_file.writelines("\"info\": ")
               
                json.dump(data["info"], ann_file)
                ann_file.writelines(",")
                ann_file.writelines("\"licenses\": ")
                #print(data["licenses"])
                ann_file.writelines(json.dumps(data["licenses"]))
                # json.dumps(data["licenses"], ann_file)
                ann_file.writelines(",")
                ann_file.writelines("\"categories\": ")
                #print(data["categories"])
                json.dump(data_cat["categories"], ann_file) 
                
                ann_file.writelines(",")
                ann_file.writelines("\"images\": ")
                ann_file.writelines("[")

            info_added = True            
           
       
        # add the images element
        with open(annotation_file_result_path,"a") as ann_file:
            
            #if it is not the first scene we need a "," here
            if not processedSceneIndex==0:
                ann_file.writelines(",")
                
            ann_file.writelines(json.dumps(element_images[0]))
            is_first = True
            for el in element_images:
                # print(el)
                if not is_first:
                    ann_file.writelines(",")
                    ann_file.writelines(json.dumps(el))
                else:
                    is_first = False  
                   
        with open(annotation_file_result_path,"a") as ann_file:
            ann_file.writelines("")
            ann_file.writelines("")
            ann_file.writelines("")
        print("adding images...scene "+ SCENE + " finished")
    
    
    with open(annotation_file_result_path,"a") as ann_file:
        ann_file.writelines("]")
    

    ### then all annotations:
    with open(annotation_file_result_path,"a") as ann_file:
       
        ann_file.writelines(",")
        ann_file.writelines("\"annotations\": ")
        ann_file.writelines("[")
   
    processedSceneIndex = -1
    
    for filename in sceneList:
        
        if filename.find(ANNOTATIONFILE_PREFIX + "-tol5-") < 0:
            continue
        
        if filename.find("scannet-v2") >= 0:
            continue
        
        processedSceneIndex = processedSceneIndex + 1
        
        if (ANNOTATIONFILE_PREFIX == "train"):
            SCENE = filename[11:-5]  
        else:
            SCENE = filename[9:-5]
            
        if (ANNOTATIONFILE_PREFIX == "test"):
            SCENE = filename[10:-5]
        print("scene: " + SCENE)


        ANNOTATION_FILE = ANNOTATIONFILE_PREFIX + "-tol"+str(TOLERANCE)+"-"+SCENE+".json" 
        

        json_file = ANNOTATION_FILE #"train-tol2-scene0191_00.json"        
        json_file_path = os.path.join(INPUT_DIR, json_file)
              
        
        with open(json_file_path) as json_file:
            # all data from the json file
            data = json.load(json_file)
            #print(data)
            
        element_annotations = data["annotations"]   
        
        print( " # annotations: " +str(len(element_annotations)))
        if len(element_annotations) == 0:
            continue
       
        # add the annotations element
        with open(annotation_file_result_path,"a") as ann_file:
            
            #if it is not the first scene we need a "," here
            if not processedSceneIndex==0:
                ann_file.writelines(",")
                
            ann_file.writelines(json.dumps(element_annotations[0]))
            
            is_first = True
            el_ind = 0
            for el in element_annotations:
                # print(el)
                if not is_first:                                    
        
                    ann_file.writelines(",")
                    ann_file.writelines(json.dumps(el))
                    el_ind = el_ind+1
                else:
                    is_first = False  
            print("written elements: "+str(el_ind))
                
        with open(annotation_file_result_path,"a") as ann_file:
            ann_file.writelines("")
            ann_file.writelines("")
            ann_file.writelines("")
        print("adding annotations...scene "+ SCENE + " finished")
       
    
    with open(annotation_file_result_path,"a") as ann_file:
        ann_file.writelines("]")      
        
      

    with open(annotation_file_result_path,"a") as ann_file:
        ann_file.writelines("}")
   
    
if __name__ == "__main__":
    main()
    sys.exit()
