import cv2
import numpy as np
import utils22

webcam = False
path = "cards.jpg"
cap = cv2.VideoCapture(0)
cap.set(10, 160)
cap.set(3, 1920)
cap.set(4, 1080)
scale = 3
wP = 210
hP = 297

while True:
    if webcam:success,img = cap.read()
    else: img = cv2.imread(path)
 
    imgContours , conts = utils22.getContours(img,minarea=5000,filter=4)
    if len(conts) != 0:
        biggest = conts[0][2]
        #print(biggest)
        imgWarp = utils22.warpImg(img, biggest, wP*3,hP*3)
        imgContours2, conts2 = utils22.getContours(imgWarp,
                                                 minarea=2000, filter=4,
                                                 cThr=[50,50],draw = False)
        if len(conts) != 0:
            for obj in conts2:
                cv2.polylines(imgContours2,[obj[2]],True,(0,255,0),2)
                nPoints = utils22.reorder(obj[2])
                nW = round((utils22.findDis(nPoints[0][0]//scale,nPoints[1][0]//scale)/10),1)
                nH = round((utils22.findDis(nPoints[0][0]//scale,nPoints[2][0]//scale)/10),1)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
        cv2.imshow('A4', imgContours2)
 
    
    cv2.imshow('Original',img)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break