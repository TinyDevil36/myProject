import cv2
import numpy as np

img = cv2.imread("lambo.png")

#二维卷积（图像滤波）
kernel = np.ones((5, 5), np.float32)/25  #/5*5
#操作如下：将该内核中心与一个像素对齐，然后将该内核下面的所有 25 个像素相加，取其平均值，并用新的平均值替换这个25x25窗口的中心像素。
# 它继续对图像中的所有像素执行此操作。：
dst = cv2.filter2D(img, -1, kernel)

#图像模糊(图像平滑)
#1.均值模糊  它只需取内核区域下所有像素的平均值并替换中心元素
blur = cv2.blur(img, (5, 5))

#2.高斯模糊
gsblur = cv2.GaussianBlur(img, (5, 5), 0)

#3.中值滤波   取内核区域下所有像素的中值，将中央元素替换为该中值
median = cv2.medianBlur(img, 5)

#4.双边滤波
blfblur = cv2.bilateralFilter(img, 9, 75, 75)

cv2.imshow("image", img)
cv2.imshow("after", dst)
cv2.imshow("blur", blur)
cv2.imshow("gsblur", gsblur)
cv2.imshow("median", median)
cv2.imshow("blfblur", blfblur)

cv2.waitKey(0)

