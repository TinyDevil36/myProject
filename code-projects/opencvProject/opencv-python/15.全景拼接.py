import cv2
import os

#拼接图像路径
mainFolder = 'Images'
myFolders = os.listdir(mainFolder)   
print(myFolders)

for folder in myFolders:
    path = mainFolder +'/'+folder
    images =[]
    myList = os.listdir(path)
    print(f'Total no of images detected {len(myList)}')
    for imgN in myList:
        curImg = cv2.imread(f'{path}/{imgN}')
        curImg = cv2.resize(curImg,(0,0),None,0.2,0.2)
        images.append(curImg)

#拼接图像
    stitcher = cv2.Stitcher.create()  #创建一个Stitcher实例
    (status,result) = stitcher.stitch(images)  #拼接指定的图像   #第一个返回值如果是0就正常
    if (status == cv2.STITCHER_OK):
        #print('Panorama Generated')
        cv2.imshow(folder,result)
        cv2.waitKey(1)
    else:
        print('Panorama Generation Unsuccessful')

cv2.waitKey(0)