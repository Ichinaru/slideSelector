# -*- coding:utf-8 -*-
"""
Created on 17 août 2010

@author: Administrator
"""
from annotation import *
from lxml import etree
from ndpviewstate import *
from point import *
from Hamamatsu import *
from math import *
from Image import *
from slideSelector import *
import ImageDraw

filename = ("C:/Documents and Settings/Administrator/My Documents/Python/SlideSelector/res/09H00132_KI67.ndpi.ndpa")
roi = color('red')

colors = (color('green'), color('light blue'))

for rni in colors:

    xmltree = etree.parse(filename)
    root = xmltree.getroot()
    xmlndpviewstates = root.findall('ndpviewstate')
    
    ndpviewstates = []
    for xmlndpviewstate in xmlndpviewstates:
        ndpviewstate = Ndpviewstate(xmlndpviewstate) 
        ndpviewstates.append(ndpviewstate)
    
    ndpifilename = remove_extension(filename)
    print ndpifilename
    foldersavename = create_folder(filename)
    
    for ndpviewstate in ndpviewstates:
        if (ndpviewstate.annotation.color == roi):
            # get the image
            imroi = ndpviewstate.image(ndpifilename)
            roicenter, roiwidth, roiheight = ndpviewstate.annotation.center_size()
            roicorner = (roicenter.x-roiwidth/2, roicenter.x+roiwidth/2, 
                         roicenter.y-roiheight/2, roicenter.y+roiheight/2)
            # remove rni of roi
            for other_ndpviewstate in ndpviewstates:
                if (other_ndpviewstate.annotation.color == rni):
                    rnicenter, rniwidth, rniheight = other_ndpviewstate.annotation.center_size()
                    if (rnicenter.x>=roicorner[0] and rnicenter.x<=roicorner[1] and
                        rnicenter.y>=roicorner[2] and rnicenter.y<=roicorner[3]):
                        imrni = other_ndpviewstate.image(ndpifilename)
                        physicaloffset = ( rnicenter.x-roicenter.x+(roiwidth - rniwidth)/2,
                                          rnicenter.y-roicenter.y +(roiheight - rniheight)/2 )
                        pixoffset = []
                        hamaimage = HamamatsuImage(ndpifilename)
                        for item in physicaloffset:
                            pixoffset.append(int(20*item/9200))
                        print 'pixoffset', pixoffset
                        pixrni = imrni.load()
                        pixroi = imroi.load()
                        for x in range(0, imrni.size[0]):
                            for y in range (0, imrni.size[1]):
                                if (pixrni[x, y] != (255, 255, 255)):
                                    pixroi[x+pixoffset[0], y+pixoffset[1]] = (255, 255, 255)
                        save_image(imrni, foldersavename, other_ndpviewstate)
            
        # save image
            save_image(imroi, foldersavename, ndpviewstate)