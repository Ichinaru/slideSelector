# -*- coding:utf-8 -*-
"""
Created on 9 août 2010

@author: Frederic Morel
"""

#title, z, lens, annotation

from annotation import *
from Hamamatsu import *

class Ndpviewstate:
    
    def __init__(self):
        self.title=" "
        self.z = 0
        self.lens = 0
        self.annotation = Annotation ()

    def set_title(self, title):
        self.title = title
        
    def get_title(self):
        return self.title
    
    def set_z(self, z):
        self.z = z
        
    def get_z(self):
        return self.z
    
    def set_lens(self, lens):
        self.lens = lens
        
    def get_lens(self):
        return self.lens
    
    def set_annotation(self, annotation):
        self.annotation = annotation
        
    def get_annotation(self):
        return self.annotation
    
    def image(self, ndpifilename):
        hamaimage = HamamatsuImage(ndpifilename)
        center, width, height = self.annotation.center_size()
        print '------'
        im = hamaimage.GetImageNm(width, height, center.get_x(), center.get_y(),
                                   int(self.z), 20) #hamaimage.GetSourceLens())
        print '------'
        im=self.annotation.contour(im, 20) #hamaimage.GetSourceLens())
        return im
                          
