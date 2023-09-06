import cv2
from cv2 import VideoCapture

cap = cv2.VideoCapture(0)

faceCascade= cv2.CascadeClassifier("/home/devil/code-projects/opencvProject/haarcascade_frontalface_default.xml")
while True:
    ret, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(imgGray,1.1,4)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)


    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break