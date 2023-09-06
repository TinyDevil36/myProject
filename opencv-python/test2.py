import cv2
import numpy as np
import os
os.chdir(os.path.split(__file__)[0]) # 控制项目的工作路径

def cat(dial, pointer):
    """
    input : 表盘图像, 指针图像
    output : 拼接图像
    采用图像中心点对应的方式将指针图像粘贴到表盘上，并采用透明度蒙版区分表盘和指针的像素点显示
    """
    pointer, alpha = pointer[:,:,0:4], pointer[:,:,3:4]
    alpha2 = dial[:,:,3:4].copy()
    dial = np.where(alpha > 1, pointer, dial)
    dial[:,:,3:4] = alpha2
    return dial

def f():
    pass

if __name__ == '__main__':
    dial_path, pointer_path = '../dial.png', '../pointer.png'

    dial = cv2.imread(dial_path, -1) # 读取表盘文件
    pointer = cv2.imread(pointer_path, -1) # 读取指针文件

    #img = cat(dial, pointer) # 拼接
    cv2.imshow("dial",dial)
    #cv2.imwrite('1.png', dial) # 保存图像