import cv2
import numpy as np

img = cv2.imread("paper.jpg", 0)
img = cv2.resize(img,(0, 0), fx=0.6, fy=0.6)

img = cv2.medianBlur(img, 5)
#简单阈值法
ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  

#自适应阈值   记住要是灰度图
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
""" Adaptive Method-它决定如何计算阈值。

    cv.ADAPTIVE_THRESH_MEAN_C 阈值是指邻近地区的平均值。
    cv.ADAPTIVE_THRESH_GAUSSIAN_C 阈值是权重为高斯窗的邻域值的加权和。

Block Size-它决定了计算阈值的窗口区域的大小。 

C-它只是一个常数，会从平均值或加权平均值中减去该值。

下面的代码比较了具有不同照明的图像的全局阈值和自适应阈值"""
titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]
for i in range(4):
    cv2.imshow(titles[i], images[i])


cv2.waitKey(0)