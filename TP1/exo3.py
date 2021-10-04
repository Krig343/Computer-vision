# Utiliser avec newimg.png et lion.png

import cv2 as cv
import sys
import matplotlib.pyplot as plt

img = cv.imread(sys.argv[1])

if img is None:
	sys.exit("Could not read the image.")

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
histo = cv.calcHist([img_gray], [0], None, [256], [0,256])

cv.imshow("Image",img_gray)
plt.plot(histo)
plt.show()
cv.waitKey(0)

img_eq = cv.equalizeHist(img_gray)

histo_eq = cv.calcHist([img_eq], [0], None, [256], [0,256])

cv.imshow("Image equalized",img_eq)
plt.plot(histo_eq)
plt.show()
cv.waitKey(0)

cv.destroyAllWindows()