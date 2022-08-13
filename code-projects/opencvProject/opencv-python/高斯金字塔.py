import cv2
import numpy as np
#高斯金字塔是通过高斯平滑和亚采样获得的一系列 采样 图像

""" 
向下采样方法：① 对图像进行高斯内核卷积；② 将所有偶数行和列去除。 pyrDown()
向上采样方法：① 将图像在每个方向上扩大为原来的两倍，新增的行和列以 0 填充；  pyrUp()
            ② 使用原先同样的内核（乘以 4)与放大后的图像卷积，获得”新增像素“的近似值。在缩放过程中已经丢失了一些信息，如果想在缩放过程中减少信息的丢失，就需要用到拉普拉斯金字塔 """
#注意：pyrUp 和 pyrDown 不是互逆的

img = cv2.imread("peien.jpeg")
imgup = []
imgdown = []
a = img.copy()
b = img.copy()
rows,cols,_ = img.shape 
for i in range(3):
    a = cv2.pyrUp(a,(cols*2, rows*2) ) 
    cv2.imshow(f"1{i}", a)
for i in range(3):
    b = cv2.pyrDown(b, (cols/2 ,rows/2))
    cv2.imshow(f"2{i}", b)

cv2.imshow("hai", img)


cv2.waitKey(0)