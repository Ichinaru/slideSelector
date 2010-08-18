# -*- coding:utf-8 -*-
"""
Created on 9 août 2010

@author: Frederic Morel
"""

from lxml import etree
from point import *
from Hamamatsu import *
from math import *
from Image import *
import ImageDraw

class Annotation:
    
    def __init__(self, color = '', type = '', displayname = '' ):
        self.color = color
        self.type = type
        self.displayname = displayname

class CirclularAnnotation(Annotation):
    
    def __init__(self, color = '', type = '', displayname = '', center = None, radius = None):
        Annotation.__init__(self,  color , type, displayname)
        self.center = center
        self.radius = radius
    
    def set_element(self, xmlannotation):
        self.radius = float(xmlannotation.find("radius").text)
        self.center = Point(int(xmlannotation.find("x").text),int(xmlannotation.find("y").text))
        
    def center_size(self):
        """ return de center and the size of the image .ndpi in nm """
        return self.center, 2*self.radius, 2*self.radius
    
    def contour(self, im, lens):
        """ set pixels outside the contour to white """
        pix = im.load()
        radius = self.radius*lens/HamamatsuImage._conversionfactor
        coordradius = Point (radius, radius)
        for y in range (0, im.size[0]):
            coordpoint = Point (0, y)
            while (coordpoint.distance(coordradius)>radius and coordpoint.x<im.size[1]):
                pix [coordpoint.x, coordpoint.y] = (255, 255, 255)
                coordpoint.x += 1
            coordpoint.x = im.size[1]-1
            while (coordpoint.distance(coordradius)>radius and coordpoint.x>=0):
                pix [coordpoint.x, coordpoint.y] = (255, 255, 255)
                coordpoint.x -= 1
        return im
        
    def print_element(self):
        print self.radius, self.center

class FreehandAnnotation(Annotation):
    
    def __init__(self):
        Annotation.__init__(self)
        self.x = []
        self.y = []
    
    def set_element(self, xmlannotation):
        pointlist = xmlannotation.findall("pointlist/point")
        for point in pointlist:
            self.x.append(int(point.find('x').text))
            self.y.append(int(point.find('y').text))
    
    def print_element(self):
        for i in range (0, len(self.x)):
            print self.x[i], self.y[i]
    
    def center_size(self):
        """ return de center and the size of the image .ndpi in nm """
        xmin = min(self.x)
        xmax = max(self.x)
        ymax = max(self.y)
        ymin = min(self.y)
        center = Point((xmax+xmin)/2, (ymax+ymin)/2)
        return center, xmax-xmin, ymax-ymin
    
    def contour(self, im, lens):
        """ set pixels outside the contour to white """
        if (self.displayname != 'Rectangular Annotation'):
            draw = ImageDraw.Draw(im)
            lines = self.__contour_lines(lens)
            draw.line(lines , fill=(255, 255, 255))
            blackborderim = self.__border_lines(im, (0, 0, 0))
            whiteborderim= self.__border_lines(blackborderim, (255, 255, 255))
            pixels =[]
            pixels.append((1,1))
            im = self.flood_fill(pixels, whiteborderim)
        return im
    
    def __border_lines(self, im, color):
        newim= new('RGB', (im.size[0]+2, im.size[1]+2), color)
        newim.paste(im, (1,1))
        return newim
    
    def __contour_lines(self, lens):
        lines = []
        xmin = min(self.x)
        ymin = min(self.y)
        for i in range (0, len(self.x)):
            xpix = (self.x[i]-xmin)*lens/HamamatsuImage._conversionfactor
            ypix = (self.y[i]-ymin)*lens/HamamatsuImage._conversionfactor
            lines.append((int(xpix), int(ypix)))
        xpix = (self.x[0]-xmin)*lens/HamamatsuImage._conversionfactor
        ypix = (self.y[0]-ymin)*lens/HamamatsuImage._conversionfactor
        lines.append((int(xpix), int(ypix)))
        return lines
    
    def __check_west_or_east_side(self, pix, initpoint, direction):
        point = initpoint
        while (pix[point[0], point[1]] != (255, 255, 255)):
            pix[point[0], point[1]] = (255, 255, 255)
            point = (point[0]+direction, point[1])
        return point
    
    def __check_up_or_down_side(self, w, e, pix, direction, pixels):
        lastpixexist = False
        for p in range (w[0]+1, e[0]):
            if (pix[p, w[1]+direction] != (255, 255, 255)):
                lastpix = (p, w[1]+direction)
                lastpixexist = True
            else:
                if(lastpixexist):
                    if (pixels[-1]!=lastpix):
                        pixels.append(lastpix)
        if(lastpixexist):
            if (pixels[-1]!=lastpix):
                pixels.append(lastpix)
           
    def flood_fill(self, pixels, im):
        pix = im.load()
        print 'processing... (maybe go to take a coffee)'
        for pixel in pixels:
            if (pix[pixel[0], pixel[1]] != (255, 255, 255)):
                w = self.__check_west_or_east_side(pix, pixel, -1)
                e = self.__check_west_or_east_side(pix, (pixel[0]+1,pixel[1]), 1)
                self.__check_up_or_down_side(w, e, pix, 1, pixels)
                self.__check_up_or_down_side(w, e, pix, -1, pixels)               
        print 'done'
        return im
    