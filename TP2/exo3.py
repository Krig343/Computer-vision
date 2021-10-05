import cv2 as cv
import sys
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread(sys.argv[1])

if img is None:
	sys.exit("Could not read the image.")

s = float(sys.argv[2])
gauss = cv.GaussianBlur(img,(5,5),s)

m3 = np.matrix ([[0,-1,0],[-1,5,-1],[0,-1,0]])
m4 = np.matrix ([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
r1 = cv.filter2D(gauss,-1,m3)
r2 = cv.filter2D(gauss,-1,m4)

cv.imshow("Original",img)
cv.imshow("M3 rehaussement",r1)
cv.imshow("M4 rehaussement",r2)

cv.waitKey(0)
cv.detroyAllWindows()