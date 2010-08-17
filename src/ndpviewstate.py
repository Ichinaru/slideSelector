# -*- coding:utf-8 -*-
"""
Created on 9 août 2010

@author: Frederic Morel
"""

#title, z, lens, annotation

from annotation import *
from Hamamatsu import *

class Ndpviewstate:
    
    def __init__(self, title = '', z = None, lens = None, annotation = None):
        self.title= title
        self.z = z
        self.lens = lens
        self.annotation = annotation
    
    def image(self, ndpifilename):
        hamaimage = HamamatsuImage(ndpifilename)
        center, width, height = self.annotation.center_size()
        print '------'
        im = hamaimage.GetImageNm(width, height, center.x, center.y,
                                   int(self.z), 20) #hamaimage.GetSourceLens())
        print '------'
        im=self.annotation.contour(im, 20) #hamaimage.GetSourceLens())
        return im
                          
