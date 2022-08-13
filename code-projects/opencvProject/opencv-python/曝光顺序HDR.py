import cv2 as cv
import numpy as np
# Loading exposure images into a list 将曝光图像加载到列表中
img_fn = ["house1.png", "house2.png", "house3.png", "house4.png"]
img_list = [cv.imread(fn) for fn in img_fn]
exposure_times = np.array([15.0, 2.5, 0.25, 0.0333], dtype=np.float32)

# Merge exposures to HDR 将曝光合并到 HDR 图像中   HDR 图像的类型为 float32，而不是 uint8
merge_debevec = cv.createMergeDebevec()
hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())
merge_robertson = cv.createMergeRobertson()
hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())

# Tonemap HDR image  我们将 32 位浮点 HDR 数据映射到范围[0..1]。实际上，在某些情况下，值可以大于 1 或小于 0，因此请注意我们稍后将不得不剪切数据以避免溢出。
tonemap1 = cv.createTonemapDurand(gamma=2.2)
res_debevec = tonemap1.process(hdr_debevec.copy())
tonemap2 = cv.createTonemapDurand(gamma=1.3)
res_robertson = tonemap2.process(hdr_robertson.copy())

# Exposure fusion using Mertens
merge_mertens = cv.createMergeMertens()
res_mertens = merge_mertens.process(img_list)

# Convert datatype to 8-bit and save
res_debevec_8bit = np.clip(res_debevec*255, 0, 255).astype('uint8')
res_robertson_8bit = np.clip(res_robertson*255, 0, 255).astype('uint8')
res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
cv.imshow("ldr_debevec.jpg", res_debevec_8bit)
cv.imshow("ldr_robertson.jpg", res_robertson_8bit)
cv.imshow("fusion_mertens.jpg", res_mertens_8bit)

cv.waitKey(0)