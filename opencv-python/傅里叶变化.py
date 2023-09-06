import cv2
from cv2 import magnitude
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("peien.jpeg", 0)

#---------------1.用numpy实现傅里叶变换---------------
f = np.fft.fft2(img)  #p.fft.fft2()为我们提供了频率转换
fshift = np.fft.fftshift(f)  #为了便于分析我们要把它居中，居中处理关系到np.fft.fftshift()函数
magnitude_spectrum = 20 * np.log(np.abs(fshift))

plt.subplot(121), plt.imshow(img, cmap = "gray")
plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

"""
我们可以看到幅度谱的中心有更多白色区域，说明图像低频内容更多。找到了幅度谱那我们是不是可以在频域中进行一些操作呢？
例如高通滤波和重建图像,实质就是找到逆DFT,我们首先要用尺寸为60*60的矩形窗口遮罩抵消低频信号,然后使用np.fft.ifftshift()应用反向移位,以使DC分量再次出现在左上角。
然后使用np.ifft2()函数找到逆FFT,结果同样是一个复数
"""
rows, cols = img.shape
crow, ccol = rows//2, cols//2
fshift[crow - 30:crow+31, ccol-30:ccol+31] = 0  #创建mask
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

plt.subplot(131), plt.imshow(img, cmap='gray'),
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(133), plt.imshow(img_back)
plt.title('Result in JET'), plt.xticks([]), plt.yticks([])
plt.show()


#---------------------2.opencv实现傅里叶变换----------------------
#cv.dft()和cv.idft()函数。它返回与前一个相同的结果，但是有两个通道。第一个通道是结果的实部，第二个通道是结果的虚部。输入图像首先应转换为np.float32

dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
#cv.magnitude()函数用来计算二维矢量的幅值，其中包括3个参数，第一个是InputArray类型的x，表示矢量的浮点型X坐标值，也就是实部，第二个参数是InputArray类型的y，表示矢量的浮点型Y坐标值，也就是虚部，第三个参数是输出的幅值
magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

#DFT的性能优化
#DFT的计算性能较好，例如当数组大小为2的幂时，速度最快，对于大小为2、3和5的乘积的数组，也可以非常有效地进行处理，
#关于代码的性能问题，我们可以在找到DFT之前将数组的大小修改为任何最佳大小(通过填充零)，对于OpenCV，我们必须手动填充零，但是对于Numpy，指定FFT计算的新大小，它将自动为您填充零
#寻找最优大小，OpenCV为此提供了一个函数：cv.getOptimalDFTSize()

# 计算DFT效率最佳的尺寸
nrows = cv2.getOptimalDFTSize(rows)
ncols = cv2.getOptimalDFTSize(cols)
print(nrows, ncols)

# 首先创建一个mask，中心正方形为1，其他均为0
# 如何删除图像中的高频内容，即我们将LPF应用于图像。它实际上模糊了图像。
# 为此首先创建一个在低频时具有高值的掩码，即传递LF内容，在HF区域为0。
mask = np.zeros((rows, cols, 2), np.uint8)
mask[crow - 30:crow + 30, ccol - 30:ccol + 30] = 1

# 应用掩码Mask和求逆DTF
fshift = dft_shift * mask
f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img_back, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()