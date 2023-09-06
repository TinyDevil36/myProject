import cv2
import numpy as np
from pyzbar.pyzbar import decode
from utils24 import getContours,stackImages
cap = cv2.VideoCapture(0)

#134 179 0 255 213 255 red
#54 82 41 255 65 255 green
#108 132 65 230 106 255 blue
colors = [[134,179,0,255,213,255,"red"],[54,82,41,255,65,255,"green"],[108,132,65,230,106,255,'blue']] #颜色hsv阈值存储
color_orders = "2" #获取的颜色顺序
color_order = 0 #当前颜色选择
is_finish = False #抓取是否完成

while True:
    ret, img = cap.read()

    if is_finish:   #如果完成就换下个颜色
        color_order +=1
        is_finish = False

    #识别二维码
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData)
        color_order = myData
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
        pts2 = barcode.rect
        cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
    
    #将颜色锁定在一定阈值内
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 
    try:

        color_orders = [int(x) for x in color_orders]
        
        lower = np.array([colors[color_orders[color_order]][0],colors[color_orders[color_order]][2],colors[color_orders[color_order]][4]])
        upper = np.array([colors[color_orders[color_order]][1],colors[color_orders[color_order]][3],colors[color_orders[color_order]][5]])
        mask = cv2.inRange(imgHSV,lower,upper)

        imgResult = cv2.bitwise_and(img,img,mask=mask)
        imgResult, finalCountours = getContours(imgResult,imgResult,draw = True,minArea=300)#获得图像和识别的坐标
        for con in finalCountours:
            x, y, w, h = con[3]
            print(x,y,w,h)
        # imgStack = stackImages(0.6,([img,imgHSV],[mask,imgResult]))
        
    except:
        continue

    cv2.imshow("Stacked Images", imgResult) #展示
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break


