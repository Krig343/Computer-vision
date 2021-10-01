# openCV couleur en bgr et pas en rgb

import cv2 as cv
import sys

img_bgr = cv.imread(sys.argv[1])

if img_bgr is None:
	sys.exit("Could not read the image.")

h, w, c = img_bgr.shape 

print('width:  ', w, type(w))
print('height: ', h, type(h))
print('channel:', c, " ", type(c))

b, g, r = cv.split(img_bgr)
img_gray = cv.cvtColor(img_bgr,cv.COLOR_BGR2GRAY)
img_hsv = cv.cvtColor(img_bgr,cv.COLOR_BGR2HSV)
t, s, v = cv.split(img_hsv)

cv.imshow("Color",img_bgr)
cv.waitKey(0)

cv.imshow("R",r)
cv.imshow("G",g)
cv.imshow("B",b)
cv.imshow("Gray",img_gray)
cv.waitKey(0)

cv.imshow("T",t)
cv.imshow("S",s)
cv.imshow("V",v)
cv.imshow("HSV",img_hsv)
cv.waitKey(0)

cv.imwrite("newimg.png", v)

cv.imshow("new",cv.imread("newimg.png"))
cv.waitKey(0)
cv.destroyAllWindows()