# -*- coding:utf-8 -*-
"""
Created on 17 août 2010

@author: Frederic Morel
"""
from annotation import *
from lxml import etree
from ndpviewstate import *
from Hamamatsu import *
from slideSelector import *
import ImageDraw

filename = ("C:/Documents and Settings/Administrator/My Documents/Python/SlideSelector/res/09H00132_KI67.ndpi.ndpa")
roi = 'red'

colors = ('green', 'light blue')

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
        if (color(ndpviewstate.annotation.color) == roi):
            # get the image
            imroi = ndpviewstate.image(ndpifilename)
            roicenter, roiwidth, roiheight = ndpviewstate.annotation.center_size()
            roicorner = (roicenter.x-roiwidth/2, roicenter.x+roiwidth/2, 
                         roicenter.y-roiheight/2, roicenter.y+roiheight/2)
            # remove rni of roi
            for other_ndpviewstate in ndpviewstates:
                if (color(other_ndpviewstate.annotation.color) == rni):
                    rnicenter, rniwidth, rniheight = other_ndpviewstate.annotation.center_size()
                    if (rnicenter.x>=roicorner[0] and rnicenter.x<=roicorner[1] and
                        rnicenter.y>=roicorner[2] and rnicenter.y<=roicorner[3]):
                        imrni = other_ndpviewstate.image(ndpifilename)
                        exclude_rni(imroi, roicenter, roiwidth, roiheight, imrni, rnicenter, rniwidth, rniheight)
                        save_image(imrni, foldersavename, other_ndpviewstate)
            
            save_image(imroi, foldersavename, ndpviewstate)