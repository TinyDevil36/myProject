'''
最开始就想起以前跟着视频写过类似小项目,然后就去寻找,找到了knn算法和SVM算法
但是开始觉得有点麻烦，然后就去找了看有没有其他办法，网上大部分都是用训练好的模型，直接排除
然后就是那些用pytorch或者tensorflow之类来训练模型的,哎，可惜没学
最后只能回归用knn算法来, 可惜知识储备不够，写出来的程序精度太感人

大体思路就是和官方给的步骤来，把图片统一处理为一种格式方便训练
然后对视频中的数字进行识别轮廓，然后把数字截出来，然后放到训练好的模型中检测，

最开始识别出的数字都是空。。。 后来进行了一些处理，但是精度还是感人，哎，学长还是强。
'''



import cv2
import numpy as np

def getContours(img):
    #获得轮廓
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours: #遍历每个轮廓

        area = cv2.contourArea(cnt) #求面积
        #print(area)
        if area>60: #筛选
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)  #求精度
            #print(peri)

            #获取轮廓坐标
            approx = cv2.approxPolyDP(cnt,0.02*peri,True) 
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            #将轮廓截出
            imgt = img[y:y+h, x:x+w]
            #cv2.imshow("img1", imgt)
            imgt = cv2.resize(imgt, (25, 36))  #将其处理为统一格式
            img_tests.append(np.array(imgt).reshape(-1, 25*36).astype(np.float32)) #存储

            #将获取的结果标记在图像中
            imgt = np.array(imgt).reshape(-1, 25*36).astype(np.float32)
            ret,result,neighbours,dist = knn.findNearest(imgt,k=5) # 获取预测结果
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2) #画框
            cv2.putText(imgContour,str(int(result[0][0])),  #写文字
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (255,255,255),2)
            cv2.imshow("img", imgContour) #展示




#读取训练图片
dataPath = "算法附件/numbers/"
data = []
labels = []
for i in range(10):
    img = cv2.imread(dataPath+str(i)+".jpg")

    #对图片进行统一处理
    img = cv2.resize(img, (25, 36))  #因为图片大小不齐，于是设了一个接近值
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
    imgCanny = cv2.Canny(imgBlur,36,60)
    kernel = np.ones((3,3),np.uint8)
    imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)
    imgEroded = cv2.erode(imgDialation,kernel,iterations=2)
    data.append(np.array(imgEroded).reshape(-1, 25*36).astype(np.float32)) #存储
 

#待测图片
cap = cv2.VideoCapture("算法附件/num.mp4")
img_tests = []

#将训练图片列表格式规整
data = np.array(data).reshape(-1, 25*36).astype(np.float32)
data = np.repeat(data, 100, axis=0) #重复 多训练

#训练的label
k = np.arange(10)
train_labels = np.repeat(k,100)[:,np.newaxis] #重复
test_labels = train_labels.copy()

#创建一个K-Nearest Neighbour分类器，然后测试
knn = cv2.ml.KNearest_create()
knn.train(data,cv2.ml.ROW_SAMPLE,train_labels)

#获取待测图集
success = True
while success:
    try:  #因为到视频结尾会报错，于是用try except语句解决
        ret, img_test = cap.read()  #读取视频
        img_test = cv2.resize(img_test, (0, 0), fx=0.2,fy=0.2) #视频太大，缩小一下
        imgContour = img_test.copy()

        #预处理
        imgGray = cv2.cvtColor(img_test,cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
        imgCanny = cv2.Canny(imgBlur,36,60)
        kernel = np.ones((3,3),np.uint8)
        imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)
        imgEroded = cv2.erode(imgDialation,kernel,iterations=2)
        
        #识别轮廓， 并在图片上标记结果
        getContours(imgDialation)

        cv2.waitKey(10)#设定等待时间
    except:
        success = False

#待测数据格式规整
img_tests = np.array(img_tests).reshape(-1, 25*36).astype(np.float32)
ret,result,neighbours,dist = knn.findNearest(img_tests,k=5) # 获取整体预测结果
print(result)