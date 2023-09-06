import pytesseract
import cv2
from utils24 import *

path = "highlight_3.jpeg"
hsv = [0, 65, 59, 255, 0, 255] #限定hsv的最大最小值 yellow

img = cv2.imread(path)

#提取高亮文本区域图
imgResult = detectColor(img, hsv) 

#提取相应轮廓
imgContours, contours = getContours(imgResult, img, showCanny=True,
                                    minArea=1000, filter=4,
                                    cThr=[100, 150], draw=True)
cv2.imshow("imgContours",imgContours) #画出轮廓

#提取对应轮廓的图片
roiList = getRoi(img, contours)
# cv2.imshow("TestCrop",roiList[2])
roiDisplay(roiList)

#获取文本
highlightedText = []
for roi in roiList:
    print(pytesseract.image_to_string(roi))
    highlightedText.append(pytesseract.image_to_string(roi))

#saveText(highlightedText)

#堆叠图像
imgStack = stackImages(0.7, ([img, imgResult, imgContours]))
cv2.imshow("Stacked Images", imgStack)

cv2.waitKey(0)