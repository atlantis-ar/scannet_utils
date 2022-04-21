#!/usr/bin/env python3
# FTT create a coco compatible json file for your dataset
# Works in windows with PyCharm and python 3.8 now
# (You have to add PYTHONPATH=d:\program files\python38\lib\site-packages
# as start config environment)

import datetime
import json
import os
import re
import fnmatch
import numpy as np
from  pycococreatortools import pycococreatortools
from PIL import Image
import csv
import sys, argparse


#sys.path.append(os.getcwd()) better set PYTHONPATH to contain module directories
# params
parser = argparse.ArgumentParser()
# data paths
# path to directory containing the .sens file and <scene>_2d-instance-filt.zip
parser.add_argument('--scannet_scene_dir', required=True, help='input path to scene (with color, depth and instance_filt) to convert', default="\\\\avm-media\\Storage\\Datasets\\ScanNet\\solov2\\train\\")
parser.add_argument('--export_color_images', dest='export_color_images', action='store_true', default=False)
parser.add_argument('--coco_annotation_dir', required=True, help='output root for annotations', default="\\\\avm-media\\Storage\\Datasets\\ScanNet\\solov2\\train\\")
parser.add_argument('--coco_annotation_file', required=True, help='filename for annotation json', default="\\\\avm-media\\Storage\\Datasets\\ScanNet\\solov2\\train\\")
parser.add_argument('--tolerance', type=int, default=2, help='mask smoothing, higher is smoother')

opt = parser.parse_args()
opt.export_color_images = True
#print(opt)


#parsing parameters 
ROOT_DIR = '\\\\avm-media\\Storage\\Datasets\\ScanNet\\solov2\\'
SCENE_DIR = opt.scannet_scene_dir # 'train'
MAPPING_DIR = os.path.join(ROOT_DIR, "mapping") #opt.coco_mapping_dir # os.path.join(ROOT_DIR, "mapping")
ANNOTATION_DIR = opt.coco_annotation_dir # os.path.join(ROOT_DIR, "annotations")
ANNOTATION_FILE = opt.coco_annotation_file
TOLERANCE = opt.tolerance
export_color_images = opt.export_color_images



SCENE = os.path.basename(SCENE_DIR.rstrip('/'))
OUTPUT = os.path.join(ANNOTATION_DIR, ANNOTATION_FILE)


## for the 14 additional classes
# mapping = {56 : 1, #"garbage bin" },
#            13 : 2, #"pillow"
#            41 : 3, # "ceiling"
#            161 : 4, #"doorframe"
#            28 : 5, #"lamp"
#            71 : 6, #"mirror"
#            52 : 7, #"whiteboard"
#            96 : 8, #"radiator"
#            34 : 9, #"night stand"
#            38 : 10, #"stool"
#            101 : 11, #"telephone" 
#            59 : 12, #"microwave" 
#            69 : 13, #"board"
#            128 : 14, #"shower wall"
#            97 : 1, #recycling bin
#            67 : 10} #ottoman

INFO = {
    "description": "ScanNet v2 nyu40id dataset",
    "url": "https://www.scan-net.org",
    "version": "1.0",
    "year": int(datetime.datetime.utcnow().year),
    "contributor": "Converted by JOANNEUM RESEARCH",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]


# nyu40id copied from ScanNet site
CATEGORIES = [
{"supercategory": "shape", "id": 1, "name": "wall" },
{"supercategory": "shape", "id": 2, "name": "floor" },
{"supercategory": "shape", "id": 3, "name": "cabinet" },
{"supercategory": "shape", "id": 4, "name": "bed" },
{"supercategory": "shape", "id": 5, "name": "chair" },
{"supercategory": "shape", "id": 6, "name": "sofa" },
{"supercategory": "shape", "id": 7, "name": "table" },
{"supercategory": "shape", "id": 8, "name": "door" },
{"supercategory": "shape", "id": 9, "name": "window" },
{"supercategory": "shape", "id": 10, "name": "bookshelf" },
{"supercategory": "shape", "id": 11, "name": "picture" },
{"supercategory": "shape", "id": 12, "name": "counter" },
{"supercategory": "shape", "id": 13, "name": "blinds" },
{"supercategory": "shape", "id": 14, "name": "desk" },
{"supercategory": "shape", "id": 15, "name": "shelves" },
{"supercategory": "shape", "id": 16, "name": "curtain" },
{"supercategory": "shape", "id": 17, "name": "dresser" },
{"supercategory": "shape", "id": 18, "name": "pillow" },
{"supercategory": "shape", "id": 19, "name": "mirror" },
{"supercategory": "shape", "id": 20, "name": "floor mat" },
{"supercategory": "shape", "id": 21, "name": "clothes" },
{"supercategory": "shape", "id": 22, "name": "ceiling" },
{"supercategory": "shape", "id": 23, "name": "books" },
{"supercategory": "shape", "id": 24, "name": "refridgerator" },
{"supercategory": "shape", "id": 25, "name": "television" },
{"supercategory": "shape", "id": 26, "name": "paper" },
{"supercategory": "shape", "id": 27, "name": "towel" },
{"supercategory": "shape", "id": 28, "name": "shower curtain" },
{"supercategory": "shape", "id": 29, "name": "box" },
{"supercategory": "shape", "id": 30, "name": "whiteboard" },
{"supercategory": "shape", "id": 31, "name": "person" },
{"supercategory": "shape", "id": 32, "name": "nightstand" },
{"supercategory": "shape", "id": 33, "name": "toilet" },
{"supercategory": "shape", "id": 34, "name": "sink" },
{"supercategory": "shape", "id": 35, "name": "lamp" },
{"supercategory": "shape", "id": 36, "name": "bathtub" },
{"supercategory": "shape", "id": 37, "name": "bag" },
{"supercategory": "shape", "id": 38, "name": "otherstructure" },
{"supercategory": "shape", "id": 39, "name": "otherfurniture" },
{"supercategory": "shape", "id": 40, "name": "otherprop" }
]

# CATEGORIES = [
# {"supercategory": "shape", "id": 1, "name": "garbage bin" },
# {"supercategory": "shape", "id": 2, "name": "pillow" },
# {"supercategory": "shape", "id": 3, "name": "ceiling" },
# {"supercategory": "shape", "id": 4, "name": "doorframe" },
# {"supercategory": "shape", "id": 5, "name": "lamp" },
# {"supercategory": "shape", "id": 6, "name": "mirror" },
# {"supercategory": "shape", "id": 7, "name": "whiteboard" },
# {"supercategory": "shape", "id": 8, "name": "radiator" },
# {"supercategory": "shape", "id": 9, "name": "night stand" },
# {"supercategory": "shape", "id": 10, "name": "stool" },
# {"supercategory": "shape", "id": 11, "name": "telephone" },
# {"supercategory": "shape", "id": 12, "name": "microwave" },
# {"supercategory": "shape", "id": 13, "name": "board" },
# {"supercategory": "shape", "id": 14, "name": "shower wall" }
# ]

MAX_CATEGORIES = len(CATEGORIES)

def get_mapping(mapping_file):
    
    mapping = {}
    
    with open(mapping_file, "r") as f:
        lines = csv.reader(f, delimiter='\t')
        for l in lines:
            if l[0].startswith('id'):
                continue;
            
            # nyu40 ids are <= 40
            if int(l[4]) <= 40:
               
                # used if we only want the scannet nyu40 ids
                key = l[0]
                mapping[key] =l[4]

    return mapping
    

def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    
    return files

def filter_for_instances(root, files, image_filename):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    basename_no_extension = os.path.splitext(os.path.basename(image_filename))[0]
    file_name_prefix = basename_no_extension + '.*'
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]

    return files

# Pattern is 1xxxxyyiiii
# 1 is for color images, xxxx encodes the scene part 1, yy encodes the scene part2 followed by the 0-padded current image index (0000..n)
def generate_color_image_id(scene, file):
    i = os.path.basename(file).rsplit('.') [0]
    if len(scene) == 12:
        return int('1'+ scene[5:9] + scene[10:12] + str(i).zfill(4))
    return 0

# Pattern is 2xxxxyyiiii
# 2 is for depth images, xxxx encodes the scene part 1, yy encodes the scene part2 followed by the 0-padded current image index (0000..n)
def generate_depth_image_id(scene, file):
    i = os.path.basename(file).rsplit('.') [0]
    if len(scene) == 12:
        return int('2' + scene[5:9] + scene[10:12] + str(i).zfill(4))
    return 0

# Pattern is 7xxxxyyiiiij
# 7 is for annotations, xxxx encodes the scene part 1, yy encodes the scene part2 followed by the current image index (0000..n), jjj the segmentation counter
def generate_annotation_id(scene, file, counter):
    i = os.path.basename(file).rsplit('.') [0]
    if len(scene) == 12:
        return int('7' + scene[5:9] + scene[10:12] + str(i).zfill(4) + str(counter))
    return 0

def generate_color_filename(scene, file):
    target1 = '/color/'
    target2 = '\\color\\'
    if len(scene) == 12 and (target2 in file or target1 in file):
        return scene + target1 + os.path.basename(file)
    return os.path.basename(file)

def generate_depth_filename(scene, file):
    target1 = '/depth/'
    target2 = '\\depth\\'
    if len(scene) == 12 and (target2 in file or target1 in file):
        return scene + target1 + os.path.basename(file)
    return os.path.basename(file)


def main():

    mapping = get_mapping(os.path.join(MAPPING_DIR, 'scannetv2-labels.combined.tsv'))
  
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1 
    segmentation_id = 1 # counter

    # Filter for color jpeg images
    if export_color_images:

        cc = os.path.join(SCENE_DIR, 'color')
        for root, _, files in os.walk(cc):
            
            image_files = filter_for_jpeg(root, files)
            counter = 0
                            
            # Go through each color image
            for image_filename in image_files:
                # only add every second image since we have a lot of img             
                if (counter % 2) == 0:                    
                    counter = counter + 1
                    continue
                print(image_filename)
                image = Image.open(image_filename)
                counter = counter + 1
               
                image_id = generate_color_image_id(SCENE, image_filename) # FTT
                file_name = generate_color_filename(SCENE, image_filename) # FTT
                #filenum = os.path.basename(image_filename).rsplit('.')[0]

                labelImg_filename = image_filename.replace('color', 'label-filt').replace('.jpg', '.png')
             
                img = Image.open(labelImg_filename)
                pixel = np.array(img)
                # Go through each colour, as instances are encoded as colour values
                pixelcolors = [x[1] for x in img.getcolors()]  # [0] = pixelcount, [1] = colour
                num_labels_added = 0
                for label_id in pixelcolors:
                    #key = SCENE + '_' + str(filenum) + '_' + str(label_id)
                    #val = mapping.get(key, {'raw': 0, 'nyu40': 0})  # val contains raw and nyu40 label (=category)
                    #category_id = val.get('nyu40', 0)
                    category_id = 0
                    try:
                        category_id = int(mapping[str(label_id)])
                    except:
                        #print("label_id not converted: "+str(label_id))
                        category_id = 0
                            
                    if category_id == 0:  # 0 is background
                        continue
                    if category_id < 1 or category_id > MAX_CATEGORIES:  # Just make sure, we are safe
                        print('Ignore category ' + str(category_id))
                        continue

               
                    # if this counter is zero in the end, no info for the current image is added
                    num_labels_added = num_labels_added + 1
                    # Labels are nyu40id and coded as pixel colours (1 .. 40 decimal)
                    category_info = {'id': category_id, 'is_crowd': 'crowd' in image_filename}
                    binary_mask = pixel[:, :] == label_id  # Create a binary mask for each of the labels
                    # For debug:                
                    # Image.fromarray((binary_mask * 255).astype(np.uint8)).save(maskfile)

                    # FTT, unique id to allow merging of all scenes
                    annotation_id = generate_annotation_id(SCENE, image_filename, label_id)

                    annotation_info = pycococreatortools.create_annotation_info(
                        annotation_id, image_id, category_info, binary_mask,
                        image.size, tolerance=TOLERANCE)  # 2)

                    if annotation_info is not None:
                        coco_output["annotations"].append(annotation_info)
                    segmentation_id = segmentation_id + 1

                if num_labels_added > 0:
                    image_info = pycococreatortools.create_image_info(
                    image_id, file_name, image.size) #image.size)
                   
                    coco_output["images"].append(image_info)
                    

    with open(OUTPUT, 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    main()
    sys.exit()
