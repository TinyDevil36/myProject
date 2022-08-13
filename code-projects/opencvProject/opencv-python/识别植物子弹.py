
import cv2
import numpy as np
import math

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>500:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(approx)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            r1 = peri/2/math.pi
            r2 = math.sqrt(area/math.pi)
            ratio = r1/r2

            
            if objCor == 4 :
                aspRatio = w/float(h)
                if aspRatio >0.78 and aspRatio <1.33: objectType= "Square"
                else:objectType="Rectangle"
                cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            elif objCor>4 and 1.3>ratio>0.7 : 
                if i == 1:
                    objectType = "fire bean"
                
                if i == 2:
                    objectType = "ice bean"
                
            elif i == 4:
                cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            else: None



                
            #cv2.putText(imgContour,objectType,
                        #(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        #(0,0,0),2)


myColors = [[0,46,83,138,117,237],  #火焰子弹
            [78,98,0,255,55,255], #冰子弹
            [0,38,47,122,224,255],  #黄油子弹
            [20,33,152,255,176,255]]  #玉米炸弹

path = '/home/devil/code-projects/opencvProject/shapes.png'
videopath = "PlantsVsZombies.mp4"
cap = cv2.VideoCapture(videopath)
while True:

    ret, img = cap.read()
    imgContour = img.copy()
    kernel = np.ones((5,5),np.uint8)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
    imgCanny = cv2.Canny(imgBlur,50,50)
    imgDil = cv2.dilate(imgCanny, kernel,iterations=1)
    imgEroded = cv2.erode(imgDil,kernel,iterations=1)
    i = 1
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        imgResult = cv2.bitwise_and(imgEroded,imgEroded,mask=mask)
    
        
        getContours(imgResult)
        i+=1
    """ getContours(imgCanny)

    imgBlank = np.zeros_like(img)
    imgStack = stackImages(0.5,([img,imgGray,imgBlur],
                                [imgCanny,imgContour,imgBlank]))

    cv2.imshow("Stack", imgStack) """
    cv2.imshow("result", imgContour)
    cv2.waitKey(10)
