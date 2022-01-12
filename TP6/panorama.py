import numpy as np
import cv2 as cv
import sys

from numpy.core.numeric import zeros_like
np.set_printoptions(threshold=sys.maxsize)


def computeHarris(img, n, threshold):
    n = int(n)
    threshold = float(threshold)
    size = np.shape(img)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv.cornerHarris(gray, n, n, 0.04)
    dst = cv.dilate(dst, None)
    img[dst > threshold*dst.max()] = [0, 255, 0]
    return img


def getDescriptor(img, v):
    desc = zeros_like(img)
    w_size = np.floor(v/2)

    xmin = x-w_size
    xmax = x+w_size+1
    ymin = y-w_size
    ymax = x+w_size+1
    w = np.array[xmin:xmax, ymin:ymax]
    desc[x, y] = w.flatten()

    return desc


def pointAppariment(descA, descB):
    pass  # normL2 au carré(descA-descB)


imgA = cv.imread(sys.argv[1])
imgB = cv.imread(sys.argv[2])
imgA = cv.resize(imgA, (500, 500))
imgB = cv.resize(imgB, (500, 500))

imgA = computeHarris(imgA, sys.argv[3], sys.argv[4])
imgB = computeHarris(imgB, sys.argv[3], sys.argv[4])

res = np.concatenate((imgA, imgB), axis=1)
cv.imshow('panorama', res)

cv.waitKey(0)
cv.destroyAllWindows()
