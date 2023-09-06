import cv2
import numpy as np
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>60:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            #print(approx)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor ==3: objectType ="Tri"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio >0.98 and aspRatio <1.03: objectType= "Square"
                else:objectType="Rectangle"
            elif objCor>4: objectType= "Circles"
            else:objectType="None"



            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour,objectType,
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,0,0),2)
def empty(a):
    pass
cap = cv2.VideoCapture("算法附件/Robomaster.mp4")
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("t Min","TrackBars",0,255,empty)
cv2.createTrackbar("t Max","TrackBars",50,255,empty)


while True:
    #ret, img = cap.read()
    img = cv2.imread("/home/devil/code-projects/opencvProject/圈.png")
    #img = cv2.resize(img, (0, 0), fx = 0.45, fy = 0.45)
    imgContour = img.copy()
    t_min = cv2.getTrackbarPos("t Min","TrackBars")
    t_max = cv2.getTrackbarPos("t Max", "TrackBars")
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
    imgcanny = cv2.Canny(imgBlur, t_min, t_max)
    kernel = np.ones((3,3),np.uint8)
    imgDialation = cv2.dilate(imgcanny,kernel,iterations=1)
    imgEroded = cv2.erode(imgDialation,kernel,iterations=1)
    getContours(imgEroded)
    cv2.imshow("TrackBars", imgContour)

    cv2.waitKey(100)