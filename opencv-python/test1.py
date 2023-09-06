import cv2
import numpy as np
import os
import random
os.chdir(os.path.split(__file__)[0]) # 控制项目的工作路径

def func(dial, pointer, back):
    """
    input : 表盘图像, 指针图像
    output : 拼接图像
    采用图像中心点对应的方式将指针图像粘贴到表盘上，并采用透明度蒙版区分表盘和指针的像素点显示
    """

    rand = random.randint(1, 3)
    rand_size_x = random.sample(range(200, 400), rand)
    rand_size_y = random.sample(range(300, 500), rand)
    b_channel, g_channel, r_channel = cv2.split(back)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    back_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    bwid, bheig, bchan = back_new.shape

    (h, w) = pointer.shape[:2]
    (cx, cy) = (w//2, h//2)
                                                                                                                                                                                         
    dial_src = dial.copy()   
    for i in range(0, rand):
        rdmangle = random.randint(-30, 90)
        M = cv2.getRotationMatrix2D((cx, cy), rdmangle, 1.0)
        pointer = cv2.warpAffine(pointer, M, (w, h), borderValue=(255,255,255))
        pointer, alpha = pointer[:,:,0:4], pointer[:,:,3:4]
        alpha2 = dial_src[:,:,3:4].copy()
        dial = np.where(alpha > 1, pointer, dial_src)
        dial[:,:,3:4] = alpha2

        width, height, channel = dial.shape
        randwid = random.uniform(0.4, 1.1)
        randheig = random.uniform(0.5, 0.9)
        pts1 = np.float32([[0,0],[width,0],[0,height],[width,height]])
        pts2 = np.float32([[0,0],[width*randwid,0],[0,height*randheig],[width*randwid,height*randheig]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(dial, M, (width, height))

        img = cv2.resize(img, (rand_size_x[i], rand_size_y[i]), interpolation=cv2.INTER_AREA)

        yy1 = 0
        yy2 = img.shape[0]
        xx1 = 0
        xx2 = img.shape[1]
        
        random_x = list(range(40, bheig-xx2+500, random.randint(400,500)))
        random_y = list(range(40, bwid-yy2+100, random.randint(350,400)))

        randy = random.randint(0, len(random_y)-1)

        x1 = random_x[i]
        x2 = x1 + xx2
        y1 = random_y[randy]
        y2 = y1 + yy2

        if x1 < 0:
            xx1 = -x1
            x1 = 0
        if y1 < 0:
            yy1 = - y1
            y1 = 0
        if x2 > back_new.shape[1]:
            xx2 = img.shape[1] - (x2 - back_new.shape[1])
            x2 = back_new.shape[1]
        if y2 > back_new.shape[0]:
            yy2 = img.shape[0] - (y2 - back_new.shape[0])
            y2 = back_new.shape[0]

        alpha_png = img[yy1:yy2,xx1:xx2,3] / 255.0
        alpha_jpg = 1 - alpha_png
        
        for c in range(0,3):
            back_new[y1:y2, x1:x2, c] = ((alpha_jpg*back_new[y1:y2,x1:x2,c]) + (alpha_png*img[yy1:yy2,xx1:xx2,c]))
    return back_new

if __name__ == '__main__':
    dial_path, pointer_path, backgrd_path = './sample/dial.png', './sample/pointer.png', './background/b.png'

    dial = cv2.imread(dial_path, -1)
    pointer = cv2.imread(pointer_path, -1)
    backgrd = cv2.imread(backgrd_path, -1)
    result = func(dial, pointer, backgrd)

    h, w, c = result.shape
    a = random.uniform(0, 0.3)
    a = 1
    b = 1-a
    g = random.randint(0, 90)
    blank = np.zeros([h,w,c], result.dtype)
    dst = cv2.addWeighted(result, a, blank, b, g)
    M = np.ones(dst.shape, dtype="uint8")*random.randint(0,30)
    dst = cv2.subtract(dst, M)
    
    cv2.namedWindow("show",0)
    cv2.imshow('show',dst)
    cv2.imwrite('./data/dst.png', dst)
    cv2.waitKey(0)