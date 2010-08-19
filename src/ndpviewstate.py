# -*- coding:utf-8 -*-
"""
Created on 9 août 2010

@author: Frederic Morel
"""

#title, z, lens, annotation

from annotation import *
from Hamamatsu import *

class Ndpviewstate:
    """ Ndpviewstate Class """
    
    def __init__(self, xmlndpviewstate):
        """ Arguments:
        xmlndpviewstate : ElementTree from lxml library with ndpviewstate element
        """
        xmlannotation = xmlndpviewstate.find('annotation')
        if (xmlannotation.get("type") == "freehand"):
            self.annotation = FreehandAnnotation()
        else :
            self.annotation = CircularAnnotation()
        self.annotation.type=xmlannotation.get("type")
        self.annotation.color=xmlannotation.get("color")
        self.annotation.displayname=xmlannotation.get("displayname")
        self.annotation.set_element(xmlannotation)      
            
        self.title=xmlndpviewstate.find('title').text
        self.lens=float(xmlndpviewstate.find('lens').text)
        self.z=float(xmlndpviewstate.find('z').text)
    
    def image(self, ndpifilename):
        """
        return a PIL image corresponding to the annotation in the ndpviewstate element 
        Arguments:
        ndpifilename : string with absolute file name.
        """
        hamaimage = HamamatsuImage(ndpifilename)
        center, width, height = self.annotation.center_size()
        print '------'
        im = hamaimage.GetImageNm(width, height, center.x, center.y,
                                   int(self.z), 20) #hamaimage.GetSourceLens())
        print '------'
        im=self.annotation.contour(im, 20) #hamaimage.GetSourceLens())
        return im
                          
