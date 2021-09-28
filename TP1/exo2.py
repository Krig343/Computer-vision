import cv2 as cv
import sys
import matplotlib.pyplot as plt

img_bgr = cv.imread(sys.argv[1])

if img_bgr is None:
	sys.exit("Could not read the image.")

b_histo = cv.calcHist([img_bgr], [0], None, [256], [0,255])
g_histo = cv.calcHist([img_bgr], [1], None, [256], [0,255])
r_histo = cv.calcHist([img_bgr], [2], None, [256], [0,255])

cv.imshow("Image",img_bgr)
cv.waitKey(0)

plt.plot(b_histo)
plt.plot(g_histo)
plt.plot(r_histo)
plt.show()

cv.destroyAllWindows()