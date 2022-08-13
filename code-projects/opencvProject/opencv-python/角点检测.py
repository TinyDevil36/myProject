import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

path = "/home/devil/code-projects/opencvProject/shapes.png"
path2 = "/home/devil/code-projects/opencvProject/bricks.jpeg"
img = cv.imread(path)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv.cornerHarris(gray, 2, 3, 0.04)
'''
第一个参数**- img -是输入源图像,应为灰度图且是float32类型;
第二个参数- blockSize -是拐角检测考虑的邻域大小;
第三参数- ksize -是使用的Sobel导数的光圈参数;
第四个参数- k -**是等式中的哈里斯检测器自由参数
'''
dst = cv.dilate(dst, None)
# 最佳值的阈值，它可能因图像而异。
img[dst > 0.0001 * dst.max()] = [0, 0, 255]
cv.imshow('dst', img)

#---------------------SubPixel精度的转角--------------
img = cv.imread(path2)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 寻找哈里斯角
gray = np.float32(gray)
dst = cv.cornerHarris(gray, 2, 3, 0.04)
dst = cv.dilate(dst, None)
ret, dst = cv.threshold(dst, 0.01 * dst.max(), 255, 0)
dst = np.uint8(dst)
# 寻找质心
ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
# 定义停止和完善拐角的条件
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
# 绘制
res = np.hstack((centroids, corners))
res = np.int0(res)
img[res[:, 1], res[:, 0]] = [0, 0, 255]
img[res[:, 3], res[:, 2]] = [0, 255, 0]
cv.imshow('cornerSubPix', img)
cv.waitKey(0)


#--------------------Shi-Tomas拐角检测------------------
img = cv.imread(path2)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
corners = cv.goodFeaturesToTrack(gray,66,0.01,10)
'''
    Image: 输入灰度图像
    maxCorners : 获取角点数的数目。
    qualityLevel:该参数指出最低可接受的角点质量水平,在0-1之间。
    minDistance:角点之间最小的欧式距离，避免得到相邻特征点。
'''
corners = np.int0(corners)
for i in corners:
    x,y = i.ravel()
    cv.circle(img,(x,y),3,255,-1)
plt.figure(figsize=(10,8),dpi=100)
plt.imshow(img[:,:,::-1]),plt.title('shi-tomasi角点检测')
plt.xticks([]), plt.yticks([])
plt.show()
