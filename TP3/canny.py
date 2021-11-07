import cv2 as cv
import sys
import numpy as np
import math
import queue
np.set_printoptions(threshold=sys.maxsize)

if len(sys.argv) < 5:
    print("Nombre d'argument invalide")
    sys.exit("Format attendu : " + sys.argv[0] + " <fichier image>" + " valeur de sigma" + " seuil haut" + " seuil bas")

if int(sys.argv[2]) <= 0:
    sys.exit("La valeur de sigma doit être posiitve")

if float(sys.argv[3]) < 0 or float(sys.argv[3]) > 1:
    sys.exit("alpha doit avoir une valeur comprise entre 0 et 1")

if float(sys.argv[4]) < 0 or float(sys.argv[4]) > 1:
    sys.exit("beta doit avoir une valeur comprise entre 0 et 1")

if float(sys.argv[3]) < float(sys.argv[4]):
    sys.exit("alpha doit être supérieur à beta")

img = cv.imread(sys.argv[1])
img_origin = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

def gaussianFiltering (img, sigma):
    n = math.floor(3*sigma)
    if n%2 == 0:
        n+=1
    return cv.GaussianBlur(img,(n,n),sigma)

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
    for x in range(0,xmax):
        for y in range(0,ymax):
            if grad_d[x][y] < -Pi/8:
                grad_d[x][y] += Pi
            elif grad_d[x][y] >= 7*Pi/8:
                grad_d[x][y] -= Pi
            if grad_d[x][y] >= -Pi/8 and grad_d[x][y] < Pi/8:
                if x-1 > 0 and grad_m[x-1][y] > grad_m[x][y]:
                    img[x][y] = 0
                elif x+1 < xmax and grad_m[x+1][y] > grad_m[x][y]:
                    img[x][y] = 0
                else:
                    img[x][y] = grad_m[x][y]
            elif grad_d[x][y] >= Pi/8 and grad_d[x][y] < 3*Pi/8:
                if (x-1 > 0 and y+1 < ymax) and grad_m[x-1][y+1] > grad_m[x][y]:
                    img[x][y] = 0
                elif (y-1 > 0 and x+1 < xmax) and grad_m[x+1][y-1] > grad_m[x][y]:
                    img[x][y] = 0
                else:
                    img[x][y] = grad_m[x][y]
            elif grad_d[x][y] >= 3*Pi/8 and grad_d[x][y] < 5*Pi/8:
                if y+1 < ymax and grad_m[x][y+1] > grad_m[x][y]:
                    img[x][y] = 0
                elif y-1 > 0 and grad_m[x][y-1] > grad_m[x][y]:
                    img[x][y] = 0
                else:
                    img[x][y] = grad_m[x][y]
            elif grad_d[x][y] >= 5*Pi/8 and grad_d[x][y] < 7*Pi/8:
                if (y-1 > 0 and x-1 > 0) and grad_m[x-1][y-1] > grad_m[x][y]:
                    img[x][y] = 0
                elif (y+1 < ymax and x+1 < xmax) and grad_m[x+1][y+1] > grad_m[x][y]:
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

def hysteresisThresholding(grad_maxima, tLow, tHigh):
    fifo = queue.Queue()
    size = np.shape(grad_maxima)
    xmax = size[0]
    ymax = size[1]
    canny = np.zeros(size)
    for x in range(0,xmax):
        for y in range(0,ymax):
            if grad_maxima[x][y] >= tHigh:
                fifo.put((x,y))
                canny[x][y] = 255
            else:
                canny[x][y] = 0
    while(not fifo.empty()):
        p = fifo.get()
        x = p[0]
        y = p[1]
        #voisin droite
        if x+1 < xmax and grad_maxima[x+1][y] >= tLow and canny[x+1][y]==0:
            canny[x+1][y] = 255
            fifo.put((x+1,y))
        #voisin haut droite
        if (x+1 < xmax and y+1 < ymax) and grad_maxima[x+1][y+1] >= tLow and canny[x+1][y+1]==0:
            canny[x+1][y+1] = 255
            fifo.put((x+1,y+1))
        #voisin haut
        if y+1 < ymax and grad_maxima[x][y+1] >= tLow and canny[x][y+1]==0:
            canny[x][y+1] = 255
            fifo.put((x,y+1))
        #voisin haut gauche
        if (x-1 > 0 and y+1 < ymax) and grad_maxima[x-1][y+1] >= tLow and canny[x-1][y+1]==0:
            canny[x-1][y+1] = 255
            fifo.put((x-1,y+1))
        #voisin gauche
        if x-1 > 0 and grad_maxima[x-1][y] >= tLow and canny[x-1][y]==0:
            canny[x-1][y] = 255
            fifo.put((x-1,y))
        #voisin bas gauche
        if (x-1 > 0 and y-1 > 0) and grad_maxima[x-1][y-1] >= tLow and canny[x-1][y-1]==0:
            canny[x-1][y-1] = 255
            fifo.put((x-1,y-1))
        #voisin bas
        if y-1 > 0 and grad_maxima[x][y-1] >= tLow and canny[x][y-1]==0:
            canny[x][y-1] = 255
            fifo.put((x,y-1))
        #voisin bas droite
        if (x+1 < xmax and y-1 > 0) and grad_maxima[x+1][y-1] >= tLow and canny[x+1][y-1]==0:
            canny[x+1][y-1] = 255
            fifo.put((x+1,y-1))
    return canny

blur = gaussianFiltering(img_origin, int(sys.argv[2]))
blurFile = open("Filtre gaussien.txt","w")
blurFile.write(str(blur))
blurFile.close()

Gx = computeGx(blur)
Gy = computeGy(blur)

mag = computeMagnitude(Gx,Gy)
magFile = open("Magnitude du gradient.txt","w")
magFile.write(str(mag))
magFile.close()

dir = computeDirection(Gx,Gy)

gmax = removeNonMaxima(mag,dir)

high, low = computeThresholds(gmax, float(sys.argv[3]), float(sys.argv[4]))

print("Seuil haut : " + str(high))
print("Seuil bas : " + str(low))

canny = hysteresisThresholding(gmax, low, high)
cannyFile = open("Filtre de conny.txt","w")
cannyFile.write(str(canny))
cannyFile.close()
cv.imshow("Filtre de canny",canny)

cv.waitKey(0)
cv.destroyAllWindows()