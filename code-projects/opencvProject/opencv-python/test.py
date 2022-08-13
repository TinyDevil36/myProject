import turtle
import requests
from urllib.parse import quote
import re

# 这个函数是爬虫获取汉字的笔画坐标信息
def obtain_coordinate(target_word):  # 获取汉字的坐标
    """
    获取汉字的坐标
    :param target_word:
    :return:
    """
    url = "https://bihua.bmcx.com/web_system/bmcx_com_www/system/file/bihua/get_0/"

    params = {
        'font': quote(target_word).replace("%", "").lower(),
        'shi_fou_zi_dong': '1',
        'cache_sjs1': '20031914',
    }
    response = requests.get(url, params=params)
    content = response.text
    content = content.replace('hzbh.main(', '').split(');document.getElementById')[0]
    content = content.split('{')[-1].split("}")[0]
    pattern = re.compile(r'\w:\[(.+?)\]')
    result = re.split(pattern, content)
    order_xy_routine = []
    words_cnt = 0
    for r in result:
        sec = re.findall(r'\'.+?\'', r)
        if len(sec):
            orders = sec[1].split('#')
            for order in orders:
                order_str = re.findall(r'\(\d+,\d+\)', order)
                order_xy = [eval(xy) for xy in order_str]
                order_xy_routine.append(order_xy)
            words_cnt += 1
    print(order_xy_routine)
    
    return order_xy_routine

def draw_words(target_words, startx, starty, lineNum=1):  # 画汉字
    """
    画汉字
    :param target_words:
    :param startx:
    :param starty:
    :param lineNum:
    :return:
    """
    turtle.color("black", "black")  # 设置画笔颜色
    turtle.pu()  # 抬起画笔
    coordinates = obtain_coordinate(target_words)
    for index, coordinate in enumerate(coordinates):
        turtle.goto((startx + coordinate[0][0])/2, -(starty + coordinate[0][1])/2)
        turtle.pd()
        for xy in coordinate:
            x,y=xy
            turtle.goto((startx+x)/2, -(starty+y)/2)
        turtle.pu()

draw_words("算", -800, -600)
draw_words("法", 0, 0)

turtle.done()