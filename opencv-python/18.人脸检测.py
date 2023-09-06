from cv2 import FONT_HERSHEY_COMPLEX, waitKey
import face_recognition
import cv2
import numpy as np

#加载图片
imgcxk = face_recognition.load_image_file("/home/devil/code-projects/opencvProject/faces/cxk.jpeg")  #输出的是rgb格式
imgcxk = cv2.cvtColor(imgcxk, cv2.COLOR_RGB2BGR)
#cv2.imshow("cxk", imgcxk)
imgtest = face_recognition.load_image_file("/home/devil/code-projects/opencvProject/faces/cxk2.jpeg")
imgtest = cv2.cvtColor(imgtest, cv2.COLOR_RGB2BGR)


faceloc = face_recognition.face_locations(imgcxk)[0] #函数定位所有图像中识别出的人脸位置信息，返回值是列表形式，列表中每一行是一张人脸的位置信息
                                                       # [top, right, bottom, left]
encodecxk = face_recognition.face_encodings(imgcxk)[0] #函数获取图像文件中所有面部编码
cv2.rectangle(imgcxk, (faceloc[3], faceloc[0]), (faceloc[1], faceloc[2]), (255, 0,255), 2)

faceloctest = face_recognition.face_locations(imgtest)[0]
encodetest = face_recognition.face_encodings(imgtest)[0]
cv2.rectangle(imgtest, (faceloctest[3], faceloctest[0]), (faceloctest[1], faceloctest[2]),(255, 0,255), 2)

#人脸对比
result = face_recognition.compare_faces([encodecxk], encodetest)
#第一个参数给出一个面部编码列表（很多张脸），第二个参数给出单个面部编码（一张脸），compare_faces方法会将第二个参数的编码与第一个参数中的编码依次匹配，返回值是一个布尔值列表，匹配成功的脸返回True，匹配失败的返回False，顺序与第一个参数中脸的顺序一致。
#第三个参数默认为0.6， 越低越严格
facedis = face_recognition.face_distance([encodecxk], encodetest) #返回相似度，越大越不像
#print(result , facedis)
cv2.putText(imgtest, f'{result} {round(facedis[0], 2)}', (50, 50), FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)

cv2.imshow("cxk mask", imgcxk)
cv2.imshow("cxk test", imgtest)
cv2.waitKey(0)