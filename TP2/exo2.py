import cv2 as cv
import sys
import numpy as np
from matplotlib import pyplot as plt

def frame_update(s):
    blur = cv.GaussianBlur(img,(5,5),s)
    cv.imshow("Gaussienne",blur)

img = cv.imread(sys.argv[1])

if img is None:
	sys.exit("Could not read the image.")

cv.namedWindow('controls')
cv.createTrackbar('sigma','controls',0,1,frame_update)

blur = img
cv.imshow("Original",img)
cv.imshow("Gaussienne",blur)

cv.waitKey(0)
cv.destroyAllWindows()