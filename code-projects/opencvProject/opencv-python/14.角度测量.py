import cv2
import math

from cv2 import imread

path = "/home/devil/code-projects/opencvProject/angle.jpeg"

img = imread(path)
pointsList = [] #用来存储点的坐标

def mousepoints(event, x, y, flags, params):
    if event == cv2.EVENT_FLAG_LBUTTON:  #鼠标左键点击
        size = len(pointsList)
        if size != 0 and size % 3 != 0:
            cv2.line(img,tuple(pointsList[round((size-1)/3)*3]),(x,y),(0,0,255),2)  #round((size-1)/3)*3保证第二三个点与第一个点连线
        cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED)
        pointsList.append([x,y])
        

def gradient(pt1, pt2):  #计算梯度
    return (pt2[1]-pt1[1])/(pt2[0]-pt1[0])

def getAngle(pointslist):
    pt1, pt2, pt3 = pointsList[-3:]  #取最后三个点
    m1 = gradient(pt1,pt2)
    m2 = gradient(pt1,pt3)
    angR = math.atan((m1-m2)/(1+(m2*m1)))   #arctan角度计算公式
    
    angD = round(math.degrees(angR))   #round()四舍五入   degrees角度转换
    if  angR < 0:
        angD = 180 + angD
    cv2.putText(img,str(angD),(pt1[0]-40,pt1[1]-20),cv2.FONT_HERSHEY_COMPLEX,
                1.5,(0,0,255),2)

while True:
    if len(pointsList) % 3 == 0 and len(pointsList) !=0:
        getAngle(pointsList)

    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mousepoints)
    
    #清除图片上的点和点的数据
    if cv2.waitKey(1) & 0xFF == ord("q"):
        pointList = []
        img = cv2.imread(path)

