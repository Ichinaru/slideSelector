# -*- coding:utf-8 -*-
"""
Created on 30 août 2010

@author: Frederic Morel
"""

import Image

imhama = Image.open('Z:/R07h4201.bmp')
pix = imhama.load()
coordx = []
coordy = []
for x in range (0, imhama.size[0]):
    for y in range (0, imhama.size[1]):
        if pix[x, y] == (255, 0, 0):
            coordx.append(x)
            coordy.append(y)

box = (min(coordx),min(coordy), max(coordx), max(coordy))

im = imhama.crop(box)

im.show()

            