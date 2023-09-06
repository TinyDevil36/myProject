import cv2
import numpy as np

img = cv2.imread("/home/devil/code-projects/opencvProject/cards2.jpg")

#仿射变换
rows, cols ,c= img.shape
pts1 = np.float32([[50,50],[200,50],[50,200]]) 
pts2 = np.float32([[10,100],[200,50],[100,250]])
M = cv2.getAffineTransform(pts1, pts2)  #输入2X3矩阵
dst = cv2.warpAffine(img, M, (cols, rows))

#透视变换
width,height = 250,350
pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
#print(matrix)
imgOutput = cv2.warpPerspective(img,matrix,(width,height))

#平移变化
M2 = np.float32([[1, 0, 100], [0, 1, 50]])  #M = [[1 0 tx]
                                            #     [0 1 ty] ]
dst2 = cv2.warpAffine(img, M2, (cols, rows))

cv2.imshow("Image",img)
cv2.imshow("Output",imgOutput)
cv2.imshow("ImageWarp",dst)
cv2.imshow("ImageWarp2",dst2)

cv2.waitKey(0)