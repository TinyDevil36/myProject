import cv2
from cv2 import imread


img1 = imread("face.jpeg", 0)
img3 = cv2.bitwise_not(img1)

img2 = cv2.bitwise_and(img1, img3)
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)
cv2.waitKey(0)