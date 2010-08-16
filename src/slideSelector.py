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
    foldersavenamecolor = foldersavename+ '/' + ndpviewstate.get_annotation().get_color()
    try:
        os.mkdir(foldersavenamecolor)
    except:
        pass
    if (not(os.path.exists(foldersavenamecolor + '/' + ndpviewstate.get_title() + '.jpg'))):
        filesavename =foldersavenamecolor + '/' + ndpviewstate.get_title() + '.jpg'
    else:
        i=1
        while (os.path.exists(foldersavenamecolor + '/' + 
                              ndpviewstate.get_title() + 
                              '(' + str(i) + ')' + '.jpg')):
            i+=1
        filesavename = foldersavenamecolor + '/' + ndpviewstate.get_title()+ '(' + str(i) + ')' + '.jpg'
    im.save(filesavename, "JPEG")
 
app = App()
app.configure_traits()
filename = app.filename
roi = color(app.roi)
rni = color(app.rni)
print roi, rni

if filename == "":
    print "you didn't choose a file"

else:
    # parsing xml 
    xmltree = etree.parse(filename)
    root = xmltree.getroot()
    xmlndpviewstates = root.findall('ndpviewstate')
    
    ndpviewstates = []
    for xmlndpviewstate in xmlndpviewstates:
        ndpviewstate = Ndpviewstate()
        
        xmlannotation = xmlndpviewstate.find('annotation')
        if (xmlannotation.get("type") == "freehand"):
            annotation = FreehandAnnotation()
        else :
            annotation = CirclularAnnotation()
        annotation.set_type(xmlannotation.get("type"))
        annotation.set_color(xmlannotation.get("color"))
        annotation.set_displayname(xmlannotation.get("displayname"))
        annotation.set_element(xmlannotation)      
            
        ndpviewstate.set_title(xmlndpviewstate.find('title').text)
        ndpviewstate.set_lens(float(xmlndpviewstate.find('lens').text))
        ndpviewstate.set_z(float(xmlndpviewstate.find('z').text))
        ndpviewstate.set_annotation(annotation) 
        
        ndpviewstates.append(ndpviewstate)
    
    ndpifilename = ''
    for i in range (0, len(filename)-5):
        ndpifilename = ndpifilename + filename[i]
    
    # create folder for images
    foldersavename = ''
    for i in range (0, len(ndpifilename)-5):
        foldersavename = foldersavename + ndpifilename[i]
    try:
        os.mkdir(foldersavename)
    except:
        pass
    
    for ndpviewstate in ndpviewstates:
        if (ndpviewstate.get_annotation().get_color() == roi):
            # get the image
            imroi = ndpviewstate.image(ndpifilename)
            roicenter, roiwidth, roiheight = ndpviewstate.get_annotation().center_size()
            roicorner = (roicenter.get_x()-roiwidth/2, roicenter.get_x()+roiwidth/2, 
                         roicenter.get_y()-roiheight/2, roicenter.get_y()+roiheight/2)
            # remove rni of roi
            for other_ndpviewstate in ndpviewstates:
                if (other_ndpviewstate.get_annotation().get_color() == rni):
                    rnicenter, rniwidth, rniheight = other_ndpviewstate.get_annotation().center_size()
                    if (rnicenter.get_x()>=roicorner[0] and rnicenter.get_x()<=roicorner[1] and
                        rnicenter.get_y()>=roicorner[2] and rnicenter.get_y()<=roicorner[3]):
                        print 'ok'
                        imrni = other_ndpviewstate.image(ndpifilename)
                        physicaloffset = ( rnicenter.get_x()-roicenter.get_x()+(roiwidth - rniwidth)/2,
                                          rnicenter.get_y()-roicenter.get_y() +(roiheight - rniheight)/2 )
                        print 'physicaloffset', physicaloffset
                        pixoffset = []
                        hamaimage = HamamatsuImage(ndpifilename)
                        for item in physicaloffset:
                            #pixoffset.append(int(hamaimage.GetSourceLens()*ndpviewstate.get_lens()/other_ndpviewstate.get_lens()*item/9200))
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