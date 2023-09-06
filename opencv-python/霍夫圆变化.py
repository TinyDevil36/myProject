import numpy as np
import cv2 as cv

img = cv.imread("shapes.png", 0)
img = cv.medianBlur(img,5)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,param1=50,param2=50,minRadius=0,maxRadius=0)
'''
第一个参数为原图像（灰度图）,第二个参数是检测方法,
第三个参数为检测内侧圆心的累加器图像的分辨率于输入图像之比的倒数,如dp=1,累加器和输入图像具有相同的分辨率,如果dp=2,累计器便有输入图像一半那么大的宽度和高度,
第四个参数表示两个圆之间圆心的最小距离

param1与param2有默认值100,它们是method设置的检测方法的对应的参数,对当前唯一的方法霍夫梯度法cv2.HOUGH_GRADIENT,
param1表示传递给canny边缘检测算子的高阈值,而低阈值为高阈值的一半,
param2表示在检测阶段圆心的累加器阈值,它越小,就越可以检测到更多根本不存在的圆,而它越大的话,能通过检测的圆就更加接近完美的圆形了
'''
circles = np.uint16(np.around(circles))
for i in circles[0, :]:
    # 绘制外圆
    cv.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # 绘制圆心
    cv.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
cv.imshow('detected circles', cimg)
cv.waitKey(0)