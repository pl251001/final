import cv2
import numpy as np
import math


vid = cv2.VideoCapture('/Users/local/Downloads/3686.mp4')
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH )
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT )
fps =  vid.get(cv2.CAP_PROP_FPS)
while vid.isOpened():
    ret, img = vid.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img = cv2.Canny(img, 7000, 7000, apertureSize=7)
        btml = (300, 1080)
        btmr = (1200, 1080)
        topl = (300, 680)
        topr = (1200, 680)
        cimg=img[topl[1]:btmr[1], topl[0]:btmr[0]]
        cimg1 = cv2.Canny(cimg, 7000, 7000, apertureSize=7)
        cv2.circle(img, btml, 5, (0, 0, 255), 10)
        cv2.circle(img, btmr, 5, (0, 0, 255), 10)
        cv2.circle(img, topl, 5, (0, 0, 255), 10)
        cv2.circle(img, topr, 5, (0, 0, 255), 10)

        cv2.imshow('image', img)
        cv2.imshow('image', cimg1)
        cv2.imshow('image1', cimg)
        if cv2.waitKey(1) == ord('q'):
            break
print(width,height,fps)
vid.release()
cv2.destroyAllWindows()
