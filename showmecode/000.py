#!/usr/bin/env python3
# -*- coding: utf8 -*-

'第 0000 题：将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。'

__author__ = 'Drake-Z'

from PIL import Image, ImageDraw, ImageFont,ImageDraw2


def add_num(filname, text = '7', fillcolor = (255, 0, 0)):
    img = Image.open(filname)
    width, height = img.size
    myfont = ImageFont.truetype('/usr/share/fonts/msyhbd.ttc', size=width//8)
    fillcolor = (255, 0, 0)
    pen = ImageDraw2.Pen(fill = fillcolor,width=5)
    draw = ImageDraw.Draw(img)
    print unicode(text,'utf-8')
    draw.text((width-width//8, 0), unicode(text,'utf-8'), font=myfont, fill=fillcolor)

    draw2 = ImageDraw2.Draw(img)
    draw2.arc([0,0,100,100],0,360,fill=fillcolor)
    draw2.render(0,[0,0,100,100],pen)
    img.save('1.jpg','jpeg')
    return 0

if __name__ == '__main__':
    filname = '0.jpg'
    text = 'X'
    fillcolor = (255, 0, 0)
    add_num(filname, text, fillcolor)
