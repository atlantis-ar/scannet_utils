@echo off

set scenename=%1
echo %scenename%
python scannet_to_coco.py --scannet_scene_dir \\avm-media\Storage\Datasets\ScanNet\solov2\train\%scenename% --export_color_images --coco_annotation_dir \\avm-media\Storage\Datasets\ScanNet\solov2\annotations --coco_annotation_file train-tol5-%scenename%.json --tolerance 5 
REM python scannet_to_coco.py --scannet_scene_dir \\avm-media\Storage\Datasets\ScanNet\solov2\val\%scenename% --export_color_images --coco_annotation_dir \\avm-media\Storage\Datasets\ScanNet\solov2\annotations --coco_annotation_file val-tol5-%scenename%.json --tolerance 5 
 