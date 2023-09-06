# encoding=utf-8
from matplotlib import pyplot as plt
from MyQR import myqr
from PIL import Image  
#生成二维码存储的位置，这里想要生成动态图，因此以".gif"结尾！
save_name = 'R.gif'
myqr.run(
    words='https://blog.csdn.net/weixin_41261833',#扫描二维码后跳转的链接
    version=1, # 容错率
    level='H', # 纠错水平，范围是L、M、Q、H，从左到右依次升高
    colorized=True, # False为黑白
    contrast=1.0, # 用以调节图片的对比度，1.0 表示原始图片。
    brightness=1.0, # 用来调节图片的亮度。
    save_name=save_name, # 存储的文件名
    # 背景图片我这里给的是一张gif动态图！
    picture="R_test.gif"
    )
