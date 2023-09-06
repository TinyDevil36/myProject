
import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab
import time



img = cv2.imread('/home/devil/code-projects/opencvProject/paper3.jpeg')
img = cv2.resize(img, (640, 360))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#############################################
#### Detecting Characters  ######
#############################################
hImg, wImg,_ = img.shape
print(pytesseract.image_to_string(img)) #输出扫描的文本
boxes = pytesseract.image_to_boxes(img)  #获取识别出的文本的边界框, 若想识别中文需要加lang = 'chi_sim'
for b in boxes.splitlines():
    #print(b)
    b = b.split(' ')
    #print(b)
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 50, 255), 2)
    #cv2.putText(img,b[0],(x,hImg- y+25),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2) #此函数不能写中文


cv2.imshow('img', img)
cv2.waitKey(0)