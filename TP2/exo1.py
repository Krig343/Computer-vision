import cv2 as cv
import sys
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread(sys.argv[1])

if img is None:
	sys.exit("Could not read the image.")

n = int(sys.argv[2])
kernel = np.ones((n,n),np.float32)/9
dst = cv.filter2D(img,-1,kernel)

cv.imshow("Original",img)
cv.imshow("Moyenneur",dst)

cv.waitKey(0)
cv.destroyAllWindows()