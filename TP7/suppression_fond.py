import cv2 as cv
import numpy as np
import sys

img = cv.imread(sys.argv[1])

res = np.concatenate((img, res), axis=1)
cv.imshow('strech', res)

if cv.waitKey(0)

cv.destroyAllWindows()
