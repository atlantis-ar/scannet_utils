scannet_utils
Utilties for preparing the Scannet dataset for training and validation instance segmentation
to convert the original ScanNet data follow these steps:

(1) use convert-scannet-to-coco.bat for generate train files for each scene sererately in COCO file for the 40 nyu40 classes.
	batch runs scannet_to_coco.py and generates an entry for each image and several annotation entries for each instance annotation.
	for other classes adaptations are needed.
	since train/test/val sets are predefined, adapt the filepaths correctly and run it for each subset seperately.
	
(2) the dataset might be too huge to use it for any training, a reduction of the data is done by using filter_scannet_annotations.py:
	configure: (1) lookuptable 
					set "reduceCategories" to True
					if the categories should be reduced, define all categories that should be kept in the category_lookuptable.
					in the resulting json file, all annotations will be updated, but all will keep their categoryID, they won't be updated to be incremental.
			   (2) keep_in_percent
				    set "reduceImagesByXPercent" to True
					if NUM_ANNOT_TO_KEEP_IN_PERCENT is set to 10, approximately 10 % of all image entries will be taken, approximately 90 % wont be taken, this is decided by using a 
					random number.
					all belonging annotation entries are deleted as well.
					
(3) concatenation of scene annotations:
	finally, all json files have to be concatenated, seperately for train, val, test by using the script: concat_json_files.py
	
Acknowledgement
Created 2021-2022 by JOANNEUM RESEARCH as part of the ATLANTIS H2020 project. This work is part of a project that has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 951900.

