import cv2 as cv
import sys

img_bgr = cv.imread(sys.argv[1])

if img_bgr is None:
	sys.exit("Could not read the image.")