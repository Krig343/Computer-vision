import cv2 as cv
import sys
import matplotlib.pyplot as plt

img_bgr = cv.imread(sys.argv[1])

if img_bgr is None:
	sys.exit("Could not read the image.")

histo = cv.calcHist([img_bgr], [0,1,2], None, [256,256,256], [0,256, 0,256, 0,256])

cv.imshow("Image originelle",img_bgr)
plt.plot(histo)
plt.show()
cv.waitKey(0)

img_eq = img_bgr

for c in range(0, 2):
    img_eq[:,:,c] = cv.equalizeHist(img_bgr[:,:,c])

histo_eq = cv.calcHist([img_eq], [0,1,2], None, [256,256,256], [0,256, 0,256, 0,256])

cv.imshow("Image equalized",img_eq)
plt.plot(histo_eq)
plt.show()
cv.waitKey(0)

img_hsv = cv.cvtColor(img_bgr,cv.COLOR_BGR2HSV)
img_hsv_eq = cv.equalizeHist(img_hsv[:,:,2])

#histo_eq_hsv = cv.calcHist([img_hsv_eq], [0,1,2], None, [], [,])

cv.imshow("Image HSV equalized",img_hsv_eq)
plt.plot(histo_eq_hsv)
plt.show()
cv.waitKey(0)

cv.destroyAllWindows()