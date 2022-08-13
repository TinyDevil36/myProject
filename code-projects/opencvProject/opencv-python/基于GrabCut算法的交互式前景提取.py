import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


img = cv.imread("/home/devil/code-projects/opencvProject/deer.jpeg")
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = (140,98,280,350)
cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
'''
第一个参数**- img -即源图像,第二个参数- mask -是掩码图像,在其中我们会指定哪些区域为背景,第三个参数- rect -是它的矩形坐标,格式为(x, y, w, h),其中包括前景对象,
第四第五个参数 - bdgModel, fgdModel - 是算法内部使用的数组,我们只需要创建两个大小为(1,65)的np.float64类型零数组,
第六个参数- iterCount -是算法应运行的迭代次数,第七个参数- model -**应该是cv.GC_INIT_WITH_RECT或cv.GC_INIT_WITH_MASK或两者结合,决定我们要绘制矩形还是最终的修饰笔触
'''
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
plt.imshow(img),plt.colorbar(),plt.show()

'''
有些背景还是存在， 清除需要自己标记， 例如用白线标记需要的，黑线标记不需要的，然后在 OpenCV 中加载该掩模图像，编辑我们在新添加的掩模图像中使用相应值的原始掩模图像
# newmask是我手动标记过的mask图像
newmask = cv.imread('newmask.png',0)  #然而本人是懒狗，没标记
# 标记为白色(确保前景)的地方,更改mask = 1
# 标记为黑色(确保背景)的地方,更改mask = 0
mask[newmask == 0] = 0
mask[newmask == 255] = 1
mask, bgdModel, fgdModel = cv.grabCut(img,mask,None,bgdModel,fgdModel,5,cv.GC_INIT_WITH_MASK)
mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask[:,:,np.newaxis]
plt.imshow(img),plt.colorbar(),plt.show(
'''
