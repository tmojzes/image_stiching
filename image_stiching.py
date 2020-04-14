# import the necessary packages
import numpy as np
from imutils import paths
import argparse
import cv2
import os
import math
import re

#Enable gpu accerelation
# cv2.ocl.setUseOpenCL(True)

#Round up numbers
# def round_up(n, decimals=0):
#     multiplier = 10 ** decimals
#     return math.ceil(n * multiplier) / multiplier

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,
	help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,
	help="path to the output image")
args = vars(ap.parse_args())

#Alphanumeric sorting implementation:
def sorted_nicely(image_list):
    """ Sorts the given iterable in the way that is expected. 
    Required arguments: 
    l -- The iterable to be sorted. 
    """  
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]  
    return sorted(image_list, key = alphanum_key)

# grab the paths to the input images and initialize our images list
print("[INFO] loading images...")
imagePaths = list(paths.list_images(args["images"]))
imagePaths = sorted_nicely(imagePaths)
print(imagePaths)
images = []
# loop over the image paths, load each one, and add them to our
# images to stitch list
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

# initialize OpenCV's image stitcher object and then perform the image
# stitching
print("[INFO] stitching images...")
stitcher = cv2.Stitcher_create(mode=1)
start =0
diff = 333
finish = start + diff

# (status, stitched) = stitcher.stitch(images)
# print(status)
# cv2.imwrite(args["output"], stitched)

for j in range(0, math.ceil(len(images)/diff)):
    (status, stitched) = stitcher.stitch(images[:finish])
    

    # if the status is '0', then OpenCV successfully performed image
    # stitching
    if status == 0:
        # write the output stitched image to disk
        cv2.imwrite(f"{finish}"+args["output"], stitched)
        # os.system(f"mv output.png output/output{finish}.png")
        # display the output stitched image to our screen
        # cv2.imshow("Stitched", stitched)
        # otherwise the stitching failed, likely due to not enough keypoints)
        # being detected
        start+=math.ceil(diff*0.7)
        finish+=diff
    else:
        print("[INFO] image stitching failed ({})".format(status))
        break

# last_start = (math.ceil(len(images)/diff)-1)*diff
# print(last_start)
# (status, stitched) = stitcher.stitch(images[last_start:])
# if status == 0:
#     cv2.imwrite(args["output"], stitched)
#     os.system(f"mv output.png output/output{len(images)}.png")
# else:
#     print("[INFO] image stitching failed ({})".format(status))

    # cv2.waitKey(0)