### scannet_utils
Utilties for preparing the Scannet dataset for training and validation instance segmentation

In order to convert the original ScanNet data follow these steps:

(1) use _convert-scannet-to-coco.bat_ for generate train files for each scene sererately in COCO file for the 40 nyu40 classes.
	batch runs scannet_to_coco.py and generates an entry for each image and several annotation entries for each instance annotation.
	for other classes adaptations are needed.
	since train/test/val sets are predefined, adapt the filepaths correctly and run it for each subset seperately.
	
(2) the dataset might be too huge to use it for any training, a reduction of the data is done by using _filter_scannet_annotations.py_:
configurations: First, update the 'lookuptable': set 'reduceCategories' to True and if the categories should be reduced, define all categories that should be kept in the category_lookuptable. In the resulting json file, all annotations will be updated, but all will keep their categoryID, they won't be updated to be incremental.
Second, set keep_in_percent: set "reduceImagesByXPercent" to True and if 'keep_in_percent' is set to 10, approximately 10 % of all image entries will be taken, approximately 90 % wont be taken, this is decided by using a random number; all belonging annotation entries are deleted as well.
					
(3) concatenation of scene annotations:
	finally, all json files have to be concatenated, seperately for train, val, test by using the script: _concat_json_files.py_
	
### Acknowledgement
Created 2021-2022 by JOANNEUM RESEARCH as part of the [ATLANTIS H2020 project](https://atlantis-ar.eu). This work is part of a project that has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 951900, and from the _Bridge_ program by the Austrian Federal Ministry of Climate Action, Environment, Energy, Mobility, Innovation and Technology (BMK) under the project _TRIP_.

