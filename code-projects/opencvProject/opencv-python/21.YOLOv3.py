from pydoc import classname
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
wht = 320 #图片长宽
classesFile = "coco.names2"
classNames = []

#读取coco.names
with open(classesFile ,"rt") as f:
    classNames = f.read().rstrip('\n').split('\n') 
#print(classNames)
#print(len(classNames))


modelConfiguration = 'yolov3-320.cfg'  #设定配置
modelWeight = 'yolov3-320.weights'     #设定权重
confThreshold = 0.5  #设定置信度阈值
nmsThreshold = 0.3   #设定非极大抑制阈值（越小越严）

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeight)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV) #设置后端
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)    #设定目标计算设备

def findObject(outputs, img):
    ht, wt, ct = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]     #获取每个物品对应的概率
            classId = np.argmax(scores)  #找到最匹配的值的下标
            confidence = scores[classId] #获取置信度
            if confidence > confThreshold:
                w, h = int(det[2]*wt), int(det[3]*ht) #
                x, y = int(det[0]*wt - w/2), int(det[1]*ht - h/2) #获取左上角坐标
                classIds.append(classId)
                bbox.append([x,y,w,h])
                confs.append(float(confidence))
    indices = cv.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)  #执行非极大抑制（抑制不是极大值的元素，搜索局部的极大值）抑制一些没用的边框
                #第一个参数是输入的预测框的尺寸，是左上角和右下角的尺寸， 第二个是置信度(float类型的list) ，第三第四是置信度阈值和nms阈值
    for i in indices:

        box = bbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        cv.rectangle(img, (x,y), (x+w, y+h), (255, 0, 255), 2)
        cv.putText(img,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                  (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
while True:
    success, img = cap.read()

    blob = cv.dnn.blobFromImage(img, 1/255, (wht, wht), [0, 0, 0], 1, crop = False) #对图像进行预处理，包括减均值，比例缩放，裁剪，交换通道等
    #第一个参数是图片， 第二个是缩放比例， 第三个为输出空间尺寸size， 第四个是用于各通道减去的值，降低光照影响， 1代表交换RB通道， crop裁剪如果为True就先缩放，再从中心裁剪为size尺寸
    net.setInput(blob)
    
    #获取输出层
    layerNames = net.getLayerNames()  #获取每一层的名称，返回一个列表
    outputnames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]  #后面的函数以列表的形式返回输出层在整个网络中的索引位置
    #print(outputnames)
    output = net.forward(outputnames)  #YOLOv4网络的输出为矩形框，每个矩形框由一个向量表示，所有矩形框组成一个向量组。每个向量的长度为类别数 + 5个参数，这五个参数的前四个分别是矩形框在图像上的位置center_x, center_y, width, height（均为比例，范围在0-1之间），第五个参数是该矩形框包含一个物体的置信度。
    #print(output[0].shape, output[1].shape, output[2].shape ,output[0][0])
    findObject(output, img)
    cv.imshow("image", img)
    if cv.waitKey(1) & 0xff == ord("q"):
        break