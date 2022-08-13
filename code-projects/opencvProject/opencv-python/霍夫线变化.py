import cv2
import numpy as np

img = cv2.imread("/home/devil/code-projects/opencvProject/angle.jpeg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
"""
cv.HoughLines() 函数了。它简单的返回了一个:math:(rho, theta)`值得数组。
\rho 的单位是像素，\theta的单位是弧度。
第一个参数，输入图像应该是个二元图像，所以在应用霍夫线性变换之前先来个阈值法或者坎尼边缘检测。
第二、第三参数分别是 \rho 和 \theta 的精度。第四个参数则是一个阈值，它代表了一个(\rho,\theta)单元被认为是一条直线需要获得的最低票数。
要记住的是，得票数其实取决于这条直线穿过了多少个点。所以它也代表了应被检测出的线条最少有多长。
"""
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
cv2.imshow('image',img)


#---------------------概率 Hough 变换-------------
'''
使用的函数是 cv.HoughLinesP() 。它比之前介绍的函数多出来两个参数：

    minLineLength - 最小线长。比这个值小的线条会被丢弃。
    maxLineGap - 允许线段之间的最大间隙，以便将(在同一条直线上的)线段视为同一条。

最好的是，它直接返回直线的两个端点。在前面的例子中，你只得到直线的参数，你必须找到所有的点
'''
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imshow('imag2',img)

cv2.waitKey(0)