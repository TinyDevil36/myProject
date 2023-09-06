import cv2
import numpy as np
from utils24 import stackImages

cap = cv2.VideoCapture(0)
imgTarget = cv2.imread("water.png")
myvid = cv2.VideoCapture("LightHeaded（蜡烛人）.mp4")

detection = False
frameCounter = 0

success, imgVid = myvid.read()
hT, wT, cT = imgTarget.shape
imgVid = cv2.resize(imgVid, (wT, hT)) #设置相同大小

orb = cv2.ORB_create(nfeatures=1000) #创建关键点
kp1, des1 = orb.detectAndCompute(imgTarget, None) #提取描述点

#imgTarget = cv2.drawKeypoints(imgTarget,kp1,None) #描绘描述点

while True:
    success, imgWebcam = cap.read()
    imgAug = imgWebcam.copy()
    kp2, des2 = orb.detectAndCompute(imgWebcam, None)  #从视频中获取关键点

    if detection == False:
        myvid.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 0
    else:
        if frameCounter == myvid.get(cv2.CAP_PROP_FRAME_COUNT):
            myvid.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter = 0
        success, imgVid = myvid.read()
        imgVid = cv2.resize(imgVid, (wT, hT))

#对比匹配
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []

    for m, n in matches:
        if m.distance < 0.75 *n.distance:
            good.append(m)
    print(len(good))

    imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2) #两幅图连线

    if len(good) > 20:
        detection = True
        srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2) #reshape二维升三维
        dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(srcPts,dstPts,cv2.RANSAC,5)
        print(matrix)
 
        pts = np.float32([[0,0],[0,hT],[wT,hT],[wT,0]]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,matrix)
        img2 = cv2.polylines(imgWebcam,[np.int32(dst)],True,(255,0,255),3)
 
        imgWarp = cv2.warpPerspective(imgVid,matrix, (imgWebcam.shape[1],imgWebcam.shape[0]))
 
        maskNew = np.zeros((imgWebcam.shape[0],imgWebcam.shape[1]),np.uint8) #建立遮罩
        cv2.fillPoly(maskNew,[np.int32(dst)],(255,255,255)) #先按照目标图像的形状填充白色
        maskInv = cv2.bitwise_not(maskNew) #翻转成黑色
        imgAug = cv2.bitwise_and(imgAug,imgAug,mask = maskInv) #使用遮罩把黑色图形放到摄像头中
        imgAug = cv2.bitwise_or(imgWarp,imgAug) #图形相加，投影到摄像头视频中
 
        #imgStacked = stackImages(([imgWebcam,imgVid,imgTarget],[imgFeatures,imgWarp,imgAug]),0.5)
 
        cv2.imshow('imgWarp', imgWarp)
        cv2.imshow('img2', img2)
    cv2.imshow('maskNew', imgAug)
        
    cv2.imshow('ImgTarget',imgTarget)
    cv2.imshow('myVid',imgVid)
    cv2.imshow('Webcam', imgWebcam)
    #cv2.imshow('imgStacked', imgStacked)
    cv2.imshow('imgFeatures', imgFeatures)
    cv2.waitKey(1)
    frameCounter +=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break