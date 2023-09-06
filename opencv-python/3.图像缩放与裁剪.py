import cv2
import numpy as np
from MyQR import myqr
img = cv2.imread("/home/devil/code-projects/opencvProject/cards.jpg")

# text = ''
# for row in img:
#     print(row.shape)
#     cv2.waitKey(0)
#     for e in row:
#         print(e.shape)
#         cv2.waitKey(0)
#         text += '({}, {}, {}) '.format(e[0], e[1], e[2])
#     text += '\
# '
# print(text)
# img = img.reshape((3,-1))
# print(img_qe.shape)
img_R = img[:,:,0]
img_G = img[:,:,1]
img_B = img[:,:,2]
print(str(img_R))
save_name = 'R.gif'
myqr.run(
    words=np.array(img_R),#扫描二维码后跳转的链接
    version=6, # 容错率
    level='H', # 纠错水平，范围是L、M、Q、H，从左到右依次升高
    colorized=True, # False为黑白
    contrast=1.0, # 用以调节图片的对比度，1.0 表示原始图片。
    brightness=1.0, # 用来调节图片的亮度。
    save_name=save_name, # 存储的文件名
    # 背景图片我这里给的是一张gif动态图！
    picture="R_test.gif"
    )
img_new = cv2.merge([img_R,img_G,img_B])
print(img.shape)

imgResize = cv2.resize(img,(1000,500))
print(imgResize.shape)

imgCropped = img[46:119,352:495]

# cv2.imshow("Image",img)
# cv2.imshow("Image Resize",imgResize)
# cv2.imshow("Image Cropped",imgCropped)
# cv2.imshow("ImageR",img_R)
# cv2.imshow("ImageG",img_G)
# cv2.imshow("ImageB",img_B)
# cv2.imshow("new",img_new)
cv2.waitKey(0)