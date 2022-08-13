import cv2
import numpy as np

#1 腐蚀 只有当内核下的所有像素都为 1 时，原始图像中的像素（1 或 0）才会被视为 1，否则会被侵蚀（变为零）
img = cv2.imread("lambo.png")
imgerode = cv2.erode(img, (5, 5), iterations=1)

#2 膨胀 它与腐蚀正好相反。这里，如果内核下至少有一个像素为“1”，则像素元素为“1”。所以它会增加图像中的白色区域，或者增加前景对象的大小
imgdil = cv2.dilate(img, (5, 5), iterations=1)

#3 开运算  开只是腐蚀的另一个名称，随后是膨胀。正如我们上面所解释的，它对消除噪音很有用。在这里，我们使用 
imgopen = cv2.morphologyEx(img, cv2.MORPH_OPEN, (5, 5))

#4 闭运算  关闭与打开相反，膨胀后腐蚀。它在填充前景对象内的小孔或对象上的小黑点时很有用。
imgclose = cv2.morphologyEx(img, cv2.MORPH_CLOSE, (5, 5))

#5 形态梯度  它是图像的膨胀和腐蚀之间的差值。
imggradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, (5, 5))

#6 顶帽  它是原图像和原图像开运算结果的差值
imgtophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, (5, 5))

#7 黑帽  它是原图像和原图像的闭的差值
imgblackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, (5, 5))



cv2.imshow("image", img)
cv2.imshow("imgerode", imgerode)
cv2.imshow("imgdil", imgdil)
cv2.imshow("imgopen", imgopen)
cv2.imshow("imgclose", imgclose)
cv2.imshow("imggradient", imggradient)
cv2.imshow("imgtophat", imgtophat)
cv2.imshow("imgblackhat", imgblackhat)
cv2.waitKey(0)