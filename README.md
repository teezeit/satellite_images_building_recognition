# Using DetectNet within NVIDIA DIGITS to detect objects in satellite images

Theses python scripts are used to preprocess satellite image data to put into DetectNet


`python prepare_data.py`

Takes images from ./processed_labeled/images/*tif
Converts them to png’s
Imports featurefile ./AOI_1_Rio_polygons_solutions_3band.geojson, extracts features and converts polygons to boxes
Maps features to images
Write features in single feature .txt files matching each image

`python show_boxes_boxes.py ‘/processed_labeled’ 10`

This shows 10 random images in the folder specified with it’s according bounding boxes


`python statistics.py ‘./processed_labeled/labels/*txt’ ‘./statistics_all.png’`

This shows the statistics of the buildings in all the images

`python create_random_subsets.py ‘./processed_labeled’ ‘./sample_1000’ 1000 0.8`

Takes images and labels from ./processed_labeled/images/ ./processed_labeled/labels/
Copies a random subset of 1000 them and puts 0.8 of those 1000 images&labels into ./sample_1000/train/ and 0.2 into ./sample_1000/val/
This is to make the structure fit the KITTI format
Actually only takes images with more than 5 buildings

`python scale_images.py 1280 ‘.sample_1000/train/images/*png’ ‘./sample_1000/train/labels/*txt’ ‘./sample_1000/val/images/*png’ ‘./sample_1000/val/labels/*txt’`

Takes images and labels from the folder put into the python script and scales both images and labels up to 1280x1280 pixels
This is because the network is only/most sensitive to objects in the range of 40-500 px

