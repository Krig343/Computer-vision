import cv2 as cv
import sys
import numpy as np
import math

def translation (img, x, y):
    shape = np.shape(img)
    size = (shape[1],shape[0])
    V = np.float32([[1, 0, x], [0, 1, y]])
    return cv.warpAffine(img, V, size)

def rotationv1 (img, c, a):
    M = cv.getRotationMatrix2D(c, a, 1)
    shape = np.shape(img)
    size = (shape[1],shape[0])
    return cv.warpAffine(img, M, size)

def rotationv2 (img, c, a):
    shape = np.shape(img)
    size = (shape[0], shape[1])
    rotv2 = np.zeros(shape, np.uint8)
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            X = x * math.cos(a) - y * math.sin(a)
            Y = y * math.sin(a) + x * math.cos(a)
            if X > 0 and X < shape[0] and Y > 0 and Y < shape[1]:
                rotv2[round(X),round(Y)] = img[x,y]
    return rotv2

def update_rot(s):
    rotv1 = rotationv1(img, (float(sys.argv[4]),float(sys.argv[5])), s)
    cv.imshow("rotation 1",rotv1)

def update_cx(s):
    rotv1 = rotationv1(img, (s,float(sys.argv[5])), float(sys.argv[6]))
    cv.imshow("rotation 1",rotv1)

def update_cy(s):
    rotv1 = rotationv1(img, (float(sys.argv[4]),s), float(sys.argv[6]))
    cv.imshow("rotation 1",rotv1)

img = cv.imread(sys.argv[1])

tran = translation(img, float(sys.argv[2]), float(sys.argv[3]))
cv.imshow('trasnlation',tran)

cv.namedWindow('rotation 1')
cv.createTrackbar('angle','rotation 1',int(sys.argv[6]),360,update_rot)
cv.createTrackbar('cx','rotation 1',int(sys.argv[4]),1000,update_cx)
cv.createTrackbar('cy','rotation 1',int(sys.argv[5]),1000,update_cy)
rotv1 = rotationv1(img, (float(sys.argv[4]),float(sys.argv[5])), float(sys.argv[6]))
cv.imshow('rotation 1',rotv1)

rotv2 = rotationv2(img, (float(sys.argv[4]),float(sys.argv[5])), float(sys.argv[6]))
cv.imshow('rotation 2',rotv2)

cv.waitKey(0)
cv.destroyAllWindows()