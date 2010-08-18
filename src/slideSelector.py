# -*- coding:utf-8 -*-
"""
Created on 6 août 2010

@author: Frederic Morel
"""

from lxml import etree
from ndpviewstate import *
from annotation import *
from point import *
from Tkinter import *
import tkFileDialog
from Hamamatsu import *
import os
from interface import *

# change color name to color hexadecimal
def color(name):
    if (name == 'green'):
        color = '#00ff00'
    elif (name == 'red'):
        color = '#ff0000'
    elif (name == 'white'):
        color = '#ffffff'
    elif (name == 'yellow'):
        color = '#ffff00'
    elif (name == 'pink'):
        color = '#ff00ff'
    elif (name == 'light blue'):
        color= '#0000ff'
    elif (name == 'turquoise'):
        color= '#00ffff'
    else:
        color = '#000000'
    return color

def save_image(im, foldersavename, ndpviewstate):
    foldersavenamecolor = foldersavename+ '/' + ndpviewstate.annotation.color
    try:
        os.mkdir(foldersavenamecolor)
    except:
        pass
    if (not(os.path.exists(foldersavenamecolor + '/' + ndpviewstate.title + '.jpg'))):
        filesavename =foldersavenamecolor + '/' + ndpviewstate.title + '.jpg'
    else:
        i=1
        while (os.path.exists(foldersavenamecolor + '/' + 
                              ndpviewstate.title + 
                              '(' + str(i) + ')' + '.jpg')):
            i+=1
        filesavename = foldersavenamecolor + '/' + ndpviewstate.title+ '(' + str(i) + ')' + '.jpg'
    im.save(filesavename, "JPEG")

def remove_extension(filename):
    """ return the file name without the extension"""
    return os.path.splitext(filename)[0]

def create_folder(filename):
    """ create a directory with the same name of the filename without the file extension """
    foldersavename = remove_extension(remove_extension(filename)) # remove .ndpa then .npdi
    try:
        os.mkdir(foldersavename)
    except:
        pass # raise IOError('File not found') - file not found? is trying to create a directory
    return foldersavename

def exclude_rni(imroi, roicenter, roiwidth, roiheight, imrni, rnicenter, rniwidth, rniheight):
    physicaloffset = ( rnicenter.x-roicenter.x+(roiwidth - rniwidth)/2,
                       rnicenter.y-roicenter.y+(roiheight - rniheight)/2 )
    pixoffset = []
    for item in physicaloffset:
        pixoffset.append(int(20*item/HamamatsuImage._conversionfactor))
    pixrni = imrni.load()
    pixroi = imroi.load()
    for x in range(0, imrni.size[0]):
        for y in range (0, imrni.size[1]):
            if (pixrni[x, y] != (255, 255, 255)):
                pixroi[x+pixoffset[0], y+pixoffset[1]] = (255, 255, 255)
 
if __name__ == '__main__':
    interface = Interface()
    interface.configure_traits()
    filename = interface.filename
    roi = color(interface.roi)
    rni = color(interface.rni)
    
    if filename == "":
        raise IOError('File not found')
    
    else:
        # parsing xml 
        xmltree = etree.parse(filename)
        root = xmltree.getroot()
        xmlndpviewstates = root.findall('ndpviewstate')
        
        ndpviewstates = []
        for xmlndpviewstate in xmlndpviewstates:
            ndpviewstate = Ndpviewstate(xmlndpviewstate) 
            ndpviewstates.append(ndpviewstate)
        
        ndpifilename = remove_extension(filename)
        foldersavename = create_folder(filename)
        
        for ndpviewstate in ndpviewstates:
            if (ndpviewstate.annotation.color == roi):
                imroi = ndpviewstate.image(ndpifilename)
                roicenter, roiwidth, roiheight = ndpviewstate.annotation.center_size()
                roicorner = (roicenter.x-roiwidth/2, roicenter.x+roiwidth/2, 
                             roicenter.y-roiheight/2, roicenter.y+roiheight/2)
                for other_ndpviewstate in ndpviewstates:
                    if (other_ndpviewstate.annotation.color == rni):
                        rnicenter, rniwidth, rniheight = other_ndpviewstate.annotation.center_size()
                        if (rnicenter.x>=roicorner[0] and rnicenter.x<=roicorner[1] and
                            rnicenter.y>=roicorner[2] and rnicenter.y<=roicorner[3]):
                            imrni = other_ndpviewstate.image(ndpifilename)
                            exclude_rni(imroi, roicenter, roiwidth, roiheight, imrni, rnicenter, rniwidth, rniheight)
                            save_image(imrni, foldersavename, other_ndpviewstate)
                
                save_image(imroi, foldersavename, ndpviewstate)