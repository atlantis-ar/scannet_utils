# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 10:59:49 2021

@author: wes
"""


#!/usr/bin/env python3
# WES 
# scannet annotation file is too big for training with SOLO/SOLOv2: 
# all annotations have to be reduced, and if desired, the categories can be reduces as well. In this sample the new #
# of categories is 20.    
# This is done for each scene file seperately, and later the files are concatenated. 


import datetime
from os import listdir
import json
import os
import sys

import time
import numpy as np
from random import randrange
import argparse


DATABASE = "SCANNET"
TOLERANCE = 5
ANNOTATIONFILE_PREFIX = "train"
#ANNOTATIONFILE_PREFIX = "val"
identifier = "filtered"
debug_level =  4 #int(opt.debug_level)
# only one digit after comma is allowed!
keep_in_percent = 10#18#10 #0.5 
randValue = 100 #1000
randomValHigherThan = (100 - keep_in_percent)*(randValue/100.0)
reduceImagesByXPercent = True
reduceCategories = True

variantFaster = True



parser = argparse.ArgumentParser()

#define input and output dir
parser.add_argument('--scannet_scene_dir', required=True, help='input path to json files that should be filtered')
parser.add_argument('--output_file_dir', required=True, help='output file path for the filtered scene files')

opt = parser.parse_args()
opt.export_color_images = True


INPUT_DIR = opt.scannet_scene_dir # 'train'
OUTPUT_DIR = opt.output_file_dir 

 
def main():

    # # for keeping 40 classes
    # category_string = '{"categories": [{"supercategory": "shape", "id": 1, "name": "wall"}, \
    #     {"supercategory": "shape", "id": 2, "name": "floor"}, \
    #     {"supercategory": "shape", "id": 3, "name": "cabinet"}, \
    #     {"supercategory": "shape", "id": 4, "name": "bed"}, \
    #     {"supercategory": "shape", "id": 5, "name": "chair"}, \
    #     {"supercategory": "shape", "id": 6, "name": "sofa"}, \
    #     {"supercategory": "shape", "id": 7, "name": "table"}, \
    #     {"supercategory": "shape", "id": 8, "name": "door"}, \
    #     {"supercategory": "shape", "id": 9, "name": "window"}, \
    #     {"supercategory": "shape", "id": 10, "name": "bookshelf"}, \
    #     {"supercategory": "shape", "id": 11, "name": "picture"},\
    #     {"supercategory": "shape", "id": 12, "name": "counter"},\
    #     {"supercategory": "shape", "id": 13, "name": "blinds"}, \
    #     {"supercategory": "shape", "id": 14, "name": "desk"}, \
    #     {"supercategory": "shape", "id": 15, "name": "shelves"}, \
    #     {"supercategory": "shape", "id": 16, "name": "curtain"}, \
    #     {"supercategory": "shape", "id": 17, "name": "dresser"}, \
    #     {"supercategory": "shape", "id": 18, "name": "pillow"}, \
    #     {"supercategory": "shape", "id": 19, "name": "mirror"}, \
    #     {"supercategory": "shape", "id": 20, "name": "floor mat"}, \
    #     {"supercategory": "shape", "id": 21, "name": "clothes"}, \
    #     {"supercategory": "shape", "id": 22, "name": "ceiling"}, \
    #     {"supercategory": "shape", "id": 23, "name": "books"}, \
    #     {"supercategory": "shape", "id": 24, "name": "refridgerator"}, \
    #     {"supercategory": "shape", "id": 25, "name": "television"}, \
    #     {"supercategory": "shape", "id": 26, "name": "paper"},\
    #     {"supercategory": "shape", "id": 27, "name": "towel"},\
    #     {"supercategory": "shape", "id": 28, "name": "shower curtain"},\
    #     {"supercategory": "shape", "id": 29, "name": "box"},\
    #     {"supercategory": "shape", "id": 30, "name": "whiteboard"},\
    #     {"supercategory": "shape", "id": 31, "name": "person"}, \
    #     {"supercategory": "shape", "id": 32, "name": "nightstand"},\
    #     {"supercategory": "shape", "id": 33, "name": "toilet"},\
    #     {"supercategory": "shape", "id": 34, "name": "sink"}, \
    #     {"supercategory": "shape", "id": 35, "name": "lamp"}, \
    #     {"supercategory": "shape", "id": 36, "name": "bathtub"},\
    #     {"supercategory": "shape", "id": 37, "name": "bag"}, \
    #     {"supercategory": "shape", "id": 38, "name": "otherstructure"}, \
    #     {"supercategory": "shape", "id": 39, "name": "otherfurniture"}, \
    #     {"supercategory": "shape", "id": 40, "name": "otherprop"}\
    #     ]}'
    
    # for keeping 20 classes
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
    

    data_cat = json.loads(category_string)
    
    dataId_NameMapping = dict()
    cat_occurrenceMap = np.zeros((41,), dtype=int)
    cat_exclusionMap = np.zeros((41,), dtype=int)

    for cat in data_cat["categories"]:
        dataId_NameMapping[cat["id"]] = cat["name"]
 
    # some checks
    # check if DIR for output images (where the polygons are visualized) 
    # already exists
    try:
        os.mkdir(OUTPUT_DIR)
    except:
        if debug_level > 5:
            print("Directory <"+OUTPUT_DIR+"> already exist")
    

    processedSceneIndex = -1
    sceneList = listdir(INPUT_DIR)
    #["scene0000_00", "scene0000_01", "scene0000_02"]
    #SCENE = "scene0425_01" #"scene0444_00" 
    SCENE = "scannet-v2" #"scene0444_00" 
    skipScenes = [0,0]#422#0#582 #processed bis 320_01
    for filename in sceneList:
         
        t = time.time()
        

        
        if filename.find(ANNOTATIONFILE_PREFIX + "-tol5-") < 0:
            continue
        
        if filename.find("scannet-v2") >= 0:
            continue
        
        
        processedSceneIndex = processedSceneIndex + 1
        
        if (ANNOTATIONFILE_PREFIX == "train"):
            SCENE = filename[11:-5]  
        else:
            SCENE = filename[9:-5]
        print("scene: " + SCENE)
        
        
        if skipScenes[0] > processedSceneIndex:
            continue
        
        if  processedSceneIndex > skipScenes[1]:
            continue
        

        
        json_file = ANNOTATIONFILE_PREFIX+"-tol"+str(TOLERANCE)+"-"+SCENE+".json"  #"train-tol2-scene0191_00.json"
        json_file_path = os.path.join(INPUT_DIR, json_file)
              
        
        with open(json_file_path) as json_file:
            # all data from the json file
            data = json.load(json_file)
            #print(data)
            
        # adapting info of this annotation file
        element = data['info']
        element["description"] = "ScanNet v2 nyu40id dataset - filtered out categories (numClasses=20), filtered out annotations of instances not enough visible and reduced by "+str(keep_in_percent)+" percent."
        element["year"] = 2021
        element["contributor"] = "Converted by JOANNEUM RESEARCH (WES)"
        element["date_created"] = datetime.datetime.utcnow().isoformat(' ')
    
        if reduceCategories:
            data["categories"] = data_cat["categories"]
            
            # create lookup table of keeping ids (categories I want to keep in the annotation file), 
            # for every entry i can check if the id is present, if not, the entry is deleted.
            category_lookuptable = [1,2,3,4,5,6,7,8,9,10,11,12,14,16,24,28,33,34,36,39]
    
            
        #image_map = dict()    
        #num_image_entries = 0
        
        element_images = data["images"]   
        element_annotations = data["annotations"]   
        
        if variantFaster==True:
            del data["annotations"]
        
        # list of image ids used for the annotations
        image_id_list_from_annotations = []
        for annotation in element_annotations:
            image_id_list_from_annotations.append(annotation["image_id"])
            
            
        # # all entries concerning the images, containing e.g. filepath of the images    
        # for image_entry in data['images']:
        #     # if debug_level>2:
        #     #     print(image_entry)
            
        #     #read all info to the images into a map: 
        #     # |image_id| => |image_filename|width|hight|
        #     image_map[image_entry['id']] = [image_entry['file_name'],image_entry['width'],image_entry['height']]
        #     num_image_entries = num_image_entries + 1
        
        
        
        
        # go through all images in the image-list from the end to the beginning
        # delete image entry if the random number is not in the desired range or if the num_occurences in the annotations is not at least
        # 1/or 2.
        ###################################
        if reduceImagesByXPercent:
            takenCounter=0
            notTakenCounter=0
            # go through image entries and check # of annotation entries
            ind = len(element_images)-1
            print("# image entries: " + str(ind))
            while ind >= 0 :
                
                randNum = randrange(randValue)
                #print(randNum)
                if randNum >= randomValHigherThan:
                    currentImgId = element_images[ind]["id"]
                    # count entries in the list image_id_list_from_annotation            
                    num_occurences = image_id_list_from_annotations.count(currentImgId)
                   
                    shouldBeKept = num_occurences >= 1#2
                    if not shouldBeKept:
                        #print("image entry with id "+str( data["images"][ind]["id"])+ " has not enough annotations - deleted!")           
                        del data["images"][ind]
                        notTakenCounter = notTakenCounter+1
                    else:
                        takenCounter = takenCounter+1
                        
                        
                else:
                    notTakenCounter = notTakenCounter+1
                    del data["images"][ind]
                    
                
                ind = ind - 1
                ## for printing progress
                # if (ind % 1000) == 0:
                #     print("image elements left: "+str(ind))
                    
            print("image entries: taken: "+str(takenCounter) +", not taken: "+str(notTakenCounter)+", thats a ratio of "+str(notTakenCounter/takenCounter))
               

        # list of all image ids from the image list in data
        ################################################
        image_id_list_from_images = []
        for image_el in element_images:
            image_id_list_from_images.append(image_el["id"])


        ind = len(element_annotations)-1
        print("num annotations (before reducing): " + str(ind))
        # now go through all annotations: this is one instance within an image, can contain several polygons
        # e.g. if the object is occluded and therefor consists of several parts. 
        # Here the bounding box (rectangle) is saved as well.
        
        takenCounter=0
        notTakenCounter=0
        annotationsNew = []#{"annotations":""}#json.loads("")
        while ind >= 0 :                     
    
            firstEntryCatId = element_annotations[ind]["category_id"]
            
            if firstEntryCatId == 1:
                randNum = randrange(2)
                #print(randNum)
                if randNum != 1.0:
                    cat_exclusionMap[firstEntryCatId]=cat_exclusionMap[firstEntryCatId]+1  
                
                    if variantFaster == False:
                        del data["annotations"][ind]
                    notTakenCounter = notTakenCounter+1                                    
                    ind = ind - 1                    
                    continue
                
           #box_coord = element_annotations[ind]["bbox"]
            #area = element_annotations[ind]["area"]
            #segmentation = element_annotations[ind]["segmentation"]
            curr_img_id = element_annotations[ind]["image_id"]
            
            isCrowd = element_annotations[ind]["iscrowd"]
            if isCrowd==1:
                print(element_annotations[ind])
                
            
            shouldBeKept = True
            
            # check if category is in the category lookup table and if there is an entry of this image_id in the image list.
            if reduceCategories:
                shouldBeKept = firstEntryCatId in category_lookuptable and curr_img_id in image_id_list_from_images
            else:                                
                shouldBeKept = curr_img_id in image_id_list_from_images
                
                

            # after annotations that do not have a category listed in the lookuptable, we additionally check if the mask of the 
            # current instance does not ly mainly on one of the image borders.                
                         
            if not shouldBeKept:

                cat_exclusionMap[firstEntryCatId]=cat_exclusionMap[firstEntryCatId]+1  
                
                if variantFaster==False:
                    del data["annotations"][ind]
                    
                notTakenCounter = notTakenCounter+1                
            else: 
                takenCounter = takenCounter+1
                cat_occurrenceMap[firstEntryCatId]=cat_occurrenceMap[firstEntryCatId]+1
                if variantFaster==True:
                    annotationsNew.append(element_annotations[ind])            
        
            ind = ind - 1
            ## for printing progress
            # if (ind % 1000) == 0:
            #     print("annotations elements left: "+str(ind))
                    
        print("annotation entries: taken: "+str(takenCounter) +", not taken: "+str(notTakenCounter)+", thats a ratio of "+str(notTakenCounter/takenCounter))
               
        i=0
        
  
        if variantFaster==True:
            ann_entry = {"annotations": [annotationsNew[0]]}
            isFirst = True
            for ann in annotationsNew:
                if isFirst == True:
                    isFirst=False
                    continue
                ann_entry["annotations"].append(ann)
                i = i + 1
                
            data["annotations"] = ann_entry["annotations"]
        
        
        ## for statistics
        # print(str(cat_exclusionMap))
        # print(str(cat_occurrenceMap))
        
        json_output_file_name = ANNOTATIONFILE_PREFIX+"-tol"+str(TOLERANCE)+"-"+SCENE+"_Refined_10_Test.json" 
    
        with open(os.path.join(OUTPUT_DIR+json_output_file_name), 'w') as outfile:
            json.dump(data, outfile)
    
        elapsed = time.time() - t
        
        print("num annotations (after reducing): "+str(len(data["annotations"])))
        print("scene "+ SCENE + " finished")

        print("*****")
        print("elapsed time: "+ str(elapsed))
        print("*****")
        
        
     
if __name__ == "__main__":
    main()
    sys.exit()
