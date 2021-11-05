import cv2 as cv
import sys
import numpy as np
import math

if len(sys.argv) < 5:
    sys.exit("Format attendu : " + sys.argv[0] + " <fichier image>" + " valeur de sigma" + " alpha" + " beta")

img = cv.imread(sys.argv[1])
img_origin = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

cv.imshow("Image originele",img_origin)

def gaussianFiltering (img, sigma):
    return cv.GaussianBlur(img,(5,5),sigma)

def computeGx(img):
    m = np.matrix ([[-1,0,1],[-2,0,2],[-1,0,1]])
    return cv.filter2D(img,-1,m)

def computeGy(img):
    m = np.matrix ([[-1,-2,-1],[0,0,0],[1,2,1]])
    return cv.filter2D(img,-1,m)

def computeMagnitude(Gx,Gy):
    size = np.shape(Gx)
    M = np.zeros(size)
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            M[x,y] = math.sqrt(Gx[x,y]^2+Gy[x,y]^2)
    return M

def computeDirection(Gx,Gy):
    size = np.shape(Gx)
    Teta = np.zeros(size)
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            Teta[x,y] = math.atan2(Gy[x,y],Gx[x,y])
    return Teta

def removeNonMaxima(grad_m, grad_d):
    Pi = math.pi
    size = np.shape(grad_m)
    xmax = size[0]
    ymax = size[1]
    img = np.zeros(size)
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            if grad_d[x][y] < -Pi/8:
                grad_d[x][y] += Pi
            elif grad_d[x][y] >= 7*Pi/8:
                grad_d[x][y] -= Pi
            if grad_d[x][y] >= -Pi/8 and grad_d[x][y] < Pi/8:
                if x-1 > 0 and grad_m[x-1][y] > grad_m[x][y]:
                        img[x][y] = 0
                else:
                    if x+1 < xmax and grad_m[x+1][y] > grad_m[x][y]:
                        img[x][y] = 0
                    else:
                        img[x][y] = grad_m[x][y]
            elif grad_d[x][y] >= Pi/8 and grad_d[x][y] < 3*Pi/8:
                if (x-1 > 0 and y+1 < ymax) and grad_m[x-1][y+1] > grad_m[x][y]:
                        img[x][y] = 0
                else:
                    if (y-1 > 0 and x+1 < xmax) and grad_m[x+1][y-1] > grad_m[x][y]:
                        img[x][y] = 0
                    else:
                        img[x][y] = grad_m[x][y]
            elif grad_d[x][y] >= 3*Pi/8 and grad_d[x][y] < 5*Pi/8:
                if y+1 < ymax and grad_m[x][y+1] > grad_m[x][y]:
                        img[x][y] = 0
                else:
                    if y-1 > 0 and grad_m[x][y-1] > grad_m[x][y]:
                        img[x][y] = 0
                    else:
                        img[x][y] = grad_m[x][y]
            elif grad_d[x][y] >= 5*Pi/8 and grad_d[x][y] < 7*Pi/8:
                if (y-1 > 0 and x-1 > 0) and grad_m[x-1][y-1] > grad_m[x][y]:
                        img[x][y] = 0
                else:
                    if (y+1 < ymax and x+1 < xmax) and grad_m[x+1][y+1] > grad_m[x][y]:
                        img[x][y] = 0
                    else:
                        img[x][y] = grad_m[x][y]
    return img

def computeThresholds(grad_maxima,  alpha,  beta):
    temp = grad_maxima.flatten()
    t = sorted(temp)
    thigh = t[round(alpha * len(t))]
    tlow = beta * thigh
    return thigh, tlow

def hysteresisThresholding(grad_maxima, tLow,tHigh):

blur = gaussianFiltering(img_origin, int(sys.argv[2]))
cv.imshow("Image blur",img_origin)

mag = computeMagnitude(computeGx(blur),computeGy(blur))
cv.imshow("Image gradient magnitude",mag)

dir = computeDirection(computeGx(blur),computeGy(blur))
cv.imshow("Image gradient direction",dir)

gmax = removeNonMaxima(mag,dir)
cv.imshow("Image sans les maximas",gmax)

high, low = computeThresholds(gmax, float(sys.argv[3]), float(sys.argv[4]))

cv.waitKey(0)
cv.destroyAllWindows()