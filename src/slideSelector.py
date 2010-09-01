# -*- coding:utf-8 -*-
"""
Created on 6 août 2010

@author: Frederic Morel
"""

from lxml import etree
from ndpviewstate import *
from annotation import *
from point import *
from Hamamatsu import *
import os
from interface import *


def color(name):
    """ change color hexadecimal to color string name
    Arguments:
    name: string with the color name
    """
    if (name == '#00ff00'):
        color = 'green'
    elif (name == '#ff0000'):
        color = 'red'
    elif (name == '#ffffff'):
        color = 'white'
    elif (name == '#ffff00'):
        color = 'yellow'
    elif (name == '#ff00ff'):
        color = 'pink'
    elif (name == '#0000ff'):
        color= 'light blue'
    elif (name == '#00ffff'):
        color= 'turquoise'
    else:
        color = 'black'
    return color

def save_image(im, foldersavename, ndpviewstate):
    """ save the image in a directory in the foldersavename
    Arguments:
    im: PIL image 
    foldersavename: string with absolute folder name.
    ndpviewstate: Ndpviewstate instance
    """
    foldersavenamecolor = foldersavename+ '/' + color(ndpviewstate.annotation.color)
    try:
        os.mkdir(foldersavenamecolor)
    except:
        pass
    if (not(os.path.exists(foldersavenamecolor + '/' + ndpviewstate.title + '.bmp'))):
        filesavename =foldersavenamecolor + '/' + ndpviewstate.title + '.bmp'
    else:
        i=1
        while (os.path.exists(foldersavenamecolor + '/' + 
                              ndpviewstate.title + 
                              '(' + str(i) + ')' + '.bmp')):
            i+=1
        filesavename = foldersavenamecolor + '/' + ndpviewstate.title+ '(' + str(i) + ')' + '.bmp'
    im.save(filesavename, "BMP")
    return filesavename

def remove_extension(filename):
    """ return the file name without the extension
    Arguments:
    filename: string with absolute file name.
    """
    return os.path.splitext(filename)[0]

def create_folder(filename):
    """ create a directory with the same name of the filename without the file extension 
    Arguments:
    filename: string with absolute file name.
    """
    foldersavename = remove_extension(remove_extension(filename)) # remove .ndpa then .npdi
    try:
        os.mkdir(foldersavename)
    except:
        pass # raise IOError('File not found') - file not found? is trying to create a directory
    return foldersavename

def exclude_rni(imroi, roicenter, roiwidth, roiheight, imrni, rnicenter, rniwidth, rniheight, magnification, hamaimage):
    """ remove the region of not-interest
    Arguments:
    imroi: PIL image with the region of interest (ROI)
    roicenter: Point instance with the physical center of the ROI
    roiwidth: float with the physical of the ROI
    roiheight: float with the physical of the ROI
    imrni: PIL image with the region of non-interest (RONI)
    rnicenter: Point instance with the physical center of the RONI
    rniwidth: float with the physical of the RONI
    rniheight: float with the physical of the RONI
    """
    physicaloffset = ( (rnicenter.x-rniwidth/2.0)-(roicenter.x- roiwidth/2.0),
                       (rnicenter.y-rniheight/2.0)-(roicenter.y - roiheight/2.0) )
    pixoffset = []
    for item in physicaloffset:
        pixoffset.append(int(magnification*item/hamaimage.CONV_FACT))
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
    roi = interface.roi
    rni = interface.roni
    magnification = int(interface.magnification)
    
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
        hamaimage = HamamatsuImage(ndpifilename)
        
        for ndpviewstate in ndpviewstates:
            if (color(ndpviewstate.annotation.color) == roi):
                imroi = ndpviewstate.image(ndpifilename, magnification)
                roicenter, roiwidth, roiheight = ndpviewstate.annotation.center_size()
                roicorner = (roicenter.x-roiwidth/2, roicenter.x+roiwidth/2, 
                             roicenter.y-roiheight/2, roicenter.y+roiheight/2)
                for other_ndpviewstate in ndpviewstates:
                    if (color(other_ndpviewstate.annotation.color) == rni):
                        rnicenter, rniwidth, rniheight = other_ndpviewstate.annotation.center_size()
                        if (rnicenter.x>=roicorner[0] and rnicenter.x<=roicorner[1] and
                            rnicenter.y>=roicorner[2] and rnicenter.y<=roicorner[3]):
                            imrni = other_ndpviewstate.image(ndpifilename, magnification)
                            exclude_rni(imroi, roicenter, roiwidth, roiheight, imrni, rnicenter, rniwidth, rniheight, magnification, hamaimage)
                            save_image(imrni, foldersavename, other_ndpviewstate)
                
                if (imroi.size[0]<2000):
                    if (imroi.size[1]<2000):
                        newim= new('RGB', (2000, 2000), (255,255,255))
                        newim.paste(imroi, (1000-imroi.size[0]/2.0,1000-imroi.size[1]/2.0)) 
                    else:
                        newim= new('RGB', (2000, imroi.size[1]), (255,255,255))
                        newim.paste(imroi, (1000-imroi.size[0]/2.0,0))
                    imroi = newim
                elif (imroi.size[1]<2000):
                    newim= new('RGB', (imroi.size[0], 2000), (255,255,255))
                    newim.paste(imroi, (0,1000-imroi.size[1]/2.0)) 
                    imroi = newim        
                save_image(imroi, foldersavename, ndpviewstate)