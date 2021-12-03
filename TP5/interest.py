import cv2 as cv
import numpy as np
import sys
from scipy.ndimage.interpolation import shift

def scale (img, t):
    shape = np.shape(img)
    size = (shape[0],shape[1])
    M = np.float32([[t, 0, 1], [0, t, 1]])
    return cv.warpAffine(img, M, size)

def rotation (img, a):
    height = img.shape[0]
    width = img.shape[1]
    center = (height/2, width/2)
    M = cv.getRotationMatrix2D(center, a, 1)
    size = (height,width)
    return cv.warpAffine(img, M, size)

def perspective (img, p, q, k, l):
    size = np.shape(img)
    pts1 = np.float32([p,q,k,l])
    pts2 = np.float32([[0,0],[size[0],0],[0,size[1]],[size[0],size[1]]])
    M = cv.getPerspectiveTransform(pts1,pts2)
    return cv.warpPerspective(img, M, (size[0],size[1]))

def computeHarris (img):
    img = scale (img, taille)
    img = rotation (img, angle)
    if persp:
        img = perspective (img, p1, p2, p3, p4)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    gray = addNoise(gray, noise)
    gray = np.uint8(gray)
    harrised = cv.cornerHarris(gray,3,3,0.04)
    harrised = cv.dilate(harrised,None)
    img[harrised>0.01*harrised.max()]=[0,0,255]
    cv.imshow('Harris cv',img)

def computeMyHarris (img):
    img = scale (img, taille)
    img = rotation (img, angle)
    if persp:
        img = perspective (img, p1, p2, p3, p4)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    gray = addNoise(gray, noise)
    gray = np.uint8(gray)
    harrised = computeR(gray)
    dilated = cv.dilate(harrised,None)
    img[harrised != dilated]=0
    img[dilated>0.01*dilated.max()]=[0,0,255]
    cv.imshow('Harris cv',img)

def computeShiTomasi (img):
    img = scale(img, taille)
    img = rotation (img, angle)
    if persp:
        img = perspective (img, p1, p2, p3, p4)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    gray = addNoise(gray, noise)
    gray = np.uint8(gray)
    corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
    corners = np.int0(corners)
    for i in corners:
        x,y = i.ravel()
        cv.circle(img,(x,y),3,255,-1)
    cv.imshow('Harris cv', img)

def computeSIFT (img):
    img = scale(img, taille)
    img = rotation (img, angle)
    if persp:
        img = perspective (img, p1, p2, p3, p4)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    gray = addNoise(gray, noise)
    gray = np.uint8(gray)
    sift = cv.xfeatures2d.SIFT_create()
    kp = sift.detect(gray,None)
    img=cv.drawKeypoints(gray,kp,img)
    cv.imshow('Harris cv',img)

def computeORB (img):
    img = scale(img, taille)
    img = rotation (img, angle)
    if persp:
        img = perspective (img, p1, p2, p3, p4)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    gray = addNoise(gray, noise)
    gray = np.uint8(gray)
    orb = cv.ORB_create()
    kp = orb.detect(img,None)
    kp, des = orb.compute(img, kp)
    img2 = cv.drawKeypoints(img,kp, des, color=(0,255,0), flags=0)
    cv.imshow('Harris cv', img2)


def computeIx(img):
    return cv.Sobel(img, -1, 1, 0, 3)

def computeIy(img):
    return cv.Sobel(img, -1, 0, 1, 3)

def computeSommeI (Ix, Iy):
    sommeI = np.zeros_like(Ix)
    sommeI += Ix * Iy
    sommeI += shift(Ix, 1.0) * shift(Iy, 1.0)
    sommeI += shift(Ix, -1.0) * shift(Iy, -1.0)
    sommeI += shift(Ix, [1.0,0.0]) * shift(Iy, [1.0,0.0])
    sommeI += shift(Ix, [-1.0,0.0]) * shift(Iy, [-1.0,0.0])
    sommeI += shift(Ix, [0.0,1.0]) * shift(Iy, [0.0,1.0])
    sommeI += shift(Ix, [0.0,-1.0]) * shift(Iy, [0.0,-1.0])
    sommeI += shift(Ix, [1.0,-1.0]) * shift(Iy, [1.0,-1.0])
    sommeI += shift(Ix, [-1.0,1.0]) * shift(Iy, [-1.0,1.0])
    return sommeI

def computeR (img):
    Ix = computeIx(img)
    Iy = computeIx(img)
    Ix2 = computeSommeI (Ix, Ix)
    Iy2 = computeSommeI (Iy, Iy)
    Ixy = computeSommeI (Ix, Iy)
    M = np.array([[Ix2, Ixy],[Ixy, Iy2]])
    detM = M[0,0] * M[1,1] - M[0,1] * M[1,0]
    traceM = M[0,0] + M[1,1]
    R = detM - 0.04 * traceM
    return np.float32(R)

def addNoise (img, n):
    size = np.shape(img)
    M = np.random.normal((255/2), n, size)
    img = np.add(img, M)
    for x in range(size[0]):
        for y in range(size[1]):
            if img[x,y] < 0:
                img[x,y] = 0
            if img[x,y] > 255:
                img[x,y] = 255
    return img

def refresh (img):
    if version == 0:
        computeHarris (img)
    elif version == 1:
        computeMyHarris (img)
    elif version == 2:
        computeShiTomasi (img)
    elif version == 3:
        computeSIFT (img)
    elif version == 4:
        computeORB (img)

def update_angle (a):
    global angle
    angle = a
    refresh (img)

def update_scale (s):
    global taille
    taille = float(s+50)/100
    refresh (img)

def update_version (v):
    global version
    version = v
    refresh (img)

def update_noise (n):
    global noise
    noise = n
    refresh (img)

def update_perspective (p):
    global persp, p1, p2, p3, p4
    if persp == 0:
        p1x = input("Entrez les coordonées x du premier point : ")
        p1y = input("Entrez les coordonées y du premier point : ")
        p1 = (int(p1x), int(p1y))
        p2x = input("Entrez les coordonées x du deuxième point : ")
        p2y = input("Entrez les coordonées y du deuxième point : ")
        p2 = (int(p2x), int(p2y))
        p3x = input("Entrez les coordonées x du troisième point : ")
        p3y = input("Entrez les coordonées y du troisième point : ")
        p3 = (int(p3x), int(p3y))
        p4x = input("Entrez les coordonées x du quatrième point : ")
        p4y = input("Entrez les coordonées y du quatrième point : ")
        p4 = (int(p4x), int(p4y))
    persp = p
    refresh (img)

taille = 1
angle = 0
version = 0
noise = 0
persp = 0
img_source = cv.imread(sys.argv[1])
img = cv.resize(img_source, (500,500))
height = img.shape[0]
width = img.shape[1]
p1 = (0,0)
p2 = (width,0)
p3 = (0,height)
p4 = (width,height)

cv.namedWindow('Harris cv')
cv.createTrackbar('angle', 'Harris cv',0,360, update_angle)
cv.createTrackbar('scale', 'Harris cv',50,100, update_scale)
cv.createTrackbar('version', 'Harris cv',0,4, update_version)
cv.createTrackbar('bruit', 'Harris cv',0,100, update_noise)
cv.createTrackbar('perspective', 'Harris cv',0,1, update_perspective)

refresh(img)

cv.waitKey(0)
cv.destroyAllWindows()