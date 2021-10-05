import cv2 as cv
import sys
import matplotlib.pyplot as plt

vid = cv.VideoCapture(0)
plt.ion()
while(vid.isOpened()):
      
    ret, frame = vid.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
      
    histo = cv.calcHist([gray], [0], None, [256], [0,256])
    plt.plot(histo)
    plt.show()
    plt.pause(0.01)
    plt.clf()

    b_histo = cv.calcHist([vid], [0], None, [256], [0,256])
    g_histo = cv.calcHist([vid], [1], None, [256], [0,256])
    r_histo = cv.calcHist([vid], [2], None, [256], [0,256])

    cv.imshow("RGB", vid)

    plt.plot(b_histo,'b')
    plt.plot(g_histo,'g')
    plt.plot(r_histo,'r')
    plt.show()
    plt.pause(0.01)
    plt.clf()

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()