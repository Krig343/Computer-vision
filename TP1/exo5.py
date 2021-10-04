import cv2 as cv
import sys
import matplotlib.pyplot as plt

vid = cv.VideoCapture(0)

while(vid.isOpened()):
      
    ret, frame = vid.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
      
    histo = cv.calcHist([gray], [0], None, [256], [0,256])

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv.destroyAllWindows()