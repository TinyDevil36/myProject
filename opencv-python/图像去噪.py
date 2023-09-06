import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

#------------彩色图片降噪-----------
img = cv.imread("zaodian1.jpeg")
dst = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)  #适用于彩色图像
""" h:参数决定滤波器强度。较高的 h 值可以更好地消除噪声，但也会删除图像的细节。 (10 个没问题）
hForColorComponents:与 h 相同，但仅适用于彩色图像。 （通常与 h 相同） """
plt.subplot(121), plt.imshow(img)
plt.subplot(122),plt.imshow(dst)
plt.show()

#灰色的就换成cv.fastNlMeansDenoising（）注意有个参数是彩色才能用

#------------灰色视频降噪------------

cap = cv.VideoCapture("vtest.avi")

# create a list of first 5 frames
img = [cap.read()[1] for i in range(5)]

# convert all to grayscale
gray = [cv.cvtColor(i, cv.COLOR_BGR2GRAY) for i in img]

# convert all to float64
gray = [np.float64(i) for i in gray]

# create a noise of variance 25
noise = np.random.randn(*gray[1].shape)*10

# Add this noise to images
noisy = [i+noise for i in gray]

# Convert back to uint8
noisy = [np.uint8(np.clip(i,0,255)) for i in noisy]

# Denoise 3rd frame considering all the 5 frames
dst = cv.fastNlMeansDenoisingMulti(noisy, 2, 5, None, 4, 7,35)

plt.subplot(131),plt.imshow(gray[2],'gray')
plt.subplot(132),plt.imshow(noisy[2],'gray')
plt.subplot(133),plt.imshow(dst,'gray')
plt.show()

#彩色就换成cv.fastNlMeansDenoisingColoredMulti（） 