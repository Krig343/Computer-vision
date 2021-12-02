import cv2 as cv
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

def scale (img, t):
    shape = np.shape(img)
    size = (shape[0],shape[1]) #peut-être inverser
    V = np.float32([[t, 0, 1], [0, t, 1]])
    return cv.warpAffine(img, V, size)

def rotation (img, a):
    height = img.shape[0]
    width = img.shape[1]
    center = (height/2, width/2)
    M = cv.getRotationMatrix2D(center, a, 1)
    shape = np.shape(img)
    size = (shape[1],shape[0])
    return cv.warpAffine(img, M, size)

def computeHarris (img, angle, taille, noise):
    img = scale (img, taille)
    img = rotation (img, angle)
    img = addNoise (img, noise)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    harrised = cv.cornerHarris(gray,3,3,0.04)
    harrised = cv.dilate(harrised,None)
    img[harrised>0.01*harrised.max()]=[0,0,255]
    cv.imshow('Harris cv',img)

def computeIx(image):
    return cv.Sobel(image, -1, 1, 0, 3)

def computeIy(img):
    return cv.Sobel(img, -1, 0, 1, 3)

def computeSommeI (image):
    Ix = computeIx(image)
    Iy = computeIy(image)
    #A finir

def computeR (mat):
    pass#A finir

def addNoise (image, n):
    size = np.shape(image)
    return np.random.normal(0.0, n, size)

def refresh (img, angle, taille, version, noise):
    if version == 0:
        computeHarris (img, angle, taille, noise)
    elif version == 1:
        pass #mon harris
    elif version == 2:
        pass #computeShiTomasi()
    elif version == 3:
        pass #SIRF

def update_angle (a):
    global angle
    angle = a
    refresh (img, angle, taille, version, noise)

def update_scale (s):
    global taille
    taille = float(s+50)/100
    refresh (img, angle, taille, version, noise)

def update_version (v):
    global version
    version = v
    refresh (img, angle, taille, version, noise)

def update_noise (n):
    global noise
    noise = n
    refresh (img, angle, taille, version, noise)

taille = 1
angle = 0
version = 0
noise = 0
img_source = cv.imread(sys.argv[1])
img = cv.resize(img_source, (500,500))

cv.namedWindow('Harris cv')
cv.createTrackbar('angle', 'Harris cv',0,360, update_angle)
cv.createTrackbar('scale', 'Harris cv',50,100, update_scale)
cv.createTrackbar('version', 'Harris cv',0,3, update_version)
cv.createTrackbar('bruit', 'Harris cv',0,100, update_noise)

refresh(img, angle, taille, version, noise)

cv.waitKey(0)
cv.destroyAllWindows()

# # I == Idil après avoir dilaté I, séléctionne les indices des maximas locaux car
# # seul eux ont la même valeur quand dilaté ou non