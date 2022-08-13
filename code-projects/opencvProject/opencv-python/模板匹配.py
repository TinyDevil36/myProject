from re import template
import cv2
from cv2 import minMaxLoc
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("/home/devil/code-projects/opencvProject/faces/cxk.jpeg", 0)
img2 = img.copy()
template = cv2.imread("/home/devil/code-projects/opencvProject/basketabll.png", 0)

w,h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()


# ------------------对对象匹配-----------------
img_rgb = cv2.imread("/home/devil/code-projects/opencvProject/mario.jpeg")
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template_new = cv2.imread("/home/devil/code-projects/opencvProject/jinbi.png", 0)
w, h = template_new.shape[::-1]
res = cv2.matchTemplate(img_gray, template_new, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)  #返回坐标
#print(loc)  #(array([ 26,  26, 230, 230, 230, 231]), array([149, 174, 450, 475, 500, 450]))

for pt in zip(*loc[::-1]):  
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
cv2.imshow('res.png', img_rgb)
cv2.waitKey(0)