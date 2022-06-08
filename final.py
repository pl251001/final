import cv2
import numpy as np
import math
import random

def count(queue):
    gnum = 0
    ynum = 0
    for x in queue:
        if x == "G":
            gnum = gnum + 1
        else:
            ynum = ynum + 1
    return gnum,ynum

def crop(img,btml,btmr,topr,topl):
    cimg = img.copy()
    roi_coord = [btml, btmr, topr, topl]
    roi = np.array([roi_coord], dtype=np.int64)
    blank = np.zeros_like(cimg)
    region = cv2.fillPoly(blank, roi, 255)
    cimg = cv2.bitwise_and(cimg, region)
    return cimg


vid = cv2.VideoCapture('C:/Users/Lucas/Downloads/3686.mp4')
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH )
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT )
fps =  vid.get(cv2.CAP_PROP_FPS)
status = False
queue = []
left = 1.4
right = 1.4
number=0
total=0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter('pwpfinal.mp4', fourcc, fps, (1920, 1080))
while vid.isOpened():
    ret, img = vid.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    else:
        #Height = 1080
        #Width = 1920
        btml = (200, 1080)
        btmr = (450, 1080)
        topl = (350, 700)
        topr = (600, 700)
        btml1 = (1000, 1080)
        btmr1 = (1250, 1080)
        topl1 = (850, 700)
        topr1 = (1100, 700)
        cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cimg = cv2.GaussianBlur(cimg, (7, 7), 0)
        cimg = cv2.Canny(cimg, 50, 30, None, 3)
        limg = crop(cimg,btml,btmr,topr,topl)
        rimg = crop(cimg,btml1,btmr1,topr1,topl1)

        linesl = cv2.HoughLinesP(
            limg,  # Input edge image
            1,  # Distance resolution in pixels
            np.pi / 180,  # Angle resolution in radians
            threshold=50,  # Min number of votes for valid line
            minLineLength=150,  # Min allowed length of line
            maxLineGap=25  # Max allowed gap between line for joining them
        )
        linesr = cv2.HoughLinesP(
            rimg,  # Input edge image
            1,  # Distance resolution in pixels
            np.pi / 180,  # Angle resolution in radians
            threshold=50,  # Min number of votes for valid line
            minLineLength=150,  # Min allowed length of line
            maxLineGap=25  # Max allowed gap between line for joining them
        )

        if linesl is not None:
            for pt in linesl:
                x1, y1, x2, y2 = pt[0]
                slope = abs((y2 - y1) / (x2 - x1))
                if slope < 0.3:
                    pass
                else:
                    if 1.35 < slope < 1.45:
                        status = False
                    else:
                        status = True
                    cv2.line(limg, (x1, y1), (x2, y2), (255, 100, 100), 10)
                    left = slope
                    break
        if linesr is not None:
            for pt in linesr:
                x1, y1, x2, y2 = pt[0]
                slope = abs((y2 - y1) / (x2 - x1))
                if slope < 0.3:
                    pass
                else:
                    cv2.line(rimg,(x1,y1),(x2,y2),(255,255,255),10)
                    right = slope
                    break
        if right<0.7:
            status = True
        else:
            if 1<=right<=1.08:
                status = False
            else:
                if 1.35 < left < 1.45:
                    status = False
                else:
                    status = True
        if len(queue) >= 10:
            queue.pop(0)

        if status == False:
            queue.append("G")
        if status == True:
            queue.append("Y")
        gnum, ynum = count(queue)
        if gnum > ynum:
            cv2.circle(img, (1700, 200), 5, (0, 255, 0), 100)
        else:
            cv2.circle(img, (1700, 200), 5, (0, 255, 255), 100)
            number=number+1
        total = total+1
        txt = f'Frames with Derailment Risk: {number}/{total} '
        cv2.putText(img=img, text=txt, org=(0, 150), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2.5, color=(0, 255, 0),
                   thickness=3)


        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.imshow('image', img)
        output.write(img)
        if cv2.waitKey(1) == ord('q'):
            break
print(width,height,fps)
print(number,total)
vid.release()
output.release()
cv2.destroyAllWindows()
