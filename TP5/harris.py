import cv2 as cv
import numpy as np
import sys

def scale (img, x, y):
    shape = np.shape(img)
    size = (shape[1],shape[0])
    size = (round(size[0] * (x/100)), round(size[1]* y /100))
    return cv.resize(img, size)

def rotation (img, c, a):
    M = cv.getRotationMatrix2D(c, a, 1)
    shape = np.shape(img)
    size = (shape[1],shape[0])
    return cv.warpAffine(img, M, size)

def computeHarris (img, gray):
    harrised = cv.cornerHarris(gray,3,3,0.04)
    harrised = cv.dilate(harrised,None)
    img[harrised>0.01*harrised.max()]=[0,0,255]
    cv.imshow('Harris cv',img)

def update_rot (a):
    global img
    global gray
    gray = rotation (gray, (0,0), a)
    img = rotation (img, (0,0), a)
    computeHarris(img, gray)

def update_scale (s):
    global img
    global gray
    gray = scale (gray, s, s)
    img = scale (img, s, s)
    computeHarris(img, gray)

img = cv.imread(sys.argv[1])
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(gray)

cv.namedWindow('Harris cv')
cv.createTrackbar('angle', 'Harris cv',0,360, update_rot)
cv.createTrackbar('scale', 'Harris cv',0,100, update_scale)

harrised = cv.cornerHarris(gray,3,3,0.04)
harrised = cv.dilate(harrised,None)

img[harrised>0.01*harrised.max()]=[0,0,255]
cv.imshow('Harris cv',img)

cv.waitKey(0)
cv.destroyAllWindows()

# I == Idil après avoir dilaté I, séléctionne les indices des maximas locaux car
# seul eux ont la même valeur quand dilaté ou non