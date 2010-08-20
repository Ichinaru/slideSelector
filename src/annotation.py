# -*- coding:utf-8 -*-
"""
Created on 9 août 2010

@author: Frederic Morel
"""

from point import Point
from Hamamatsu import *
from math import *
from Image import *
import ImageDraw

class Annotation(object):
    color = ''
    type = ''
    displayname = ''

    def __init__(self, **kwargs):
        """Arguments:
        color: string with '#' then RGB hexadecimal color (e.g. '#00ffff')
        type: string
        displayname: string
        """
        for k in kwargs:
            if k in ['color', 'type', 'displayname']:        
                self.__setattr__(k,kwargs[k])

class CircularAnnotation(Annotation):
    """ CircularAnnotation class inherit from Annotation """
    center = None
    radius = None

    def __init__(self, **kwargs):
        """Arguments:
        color: string with '#' then RGB hexadecimal color (e.g. '#00ffff')
        type: string
        displayname: string
        center : Point
        radius : float
        """
        super(CirclularAnnotation, self).__init__(**kwargs)
        self.center = kwargs['center']
        self.radius = kwargs['radius']
    
    def set_element(self, xmlannotation):
        """Arguments:
        xmlannotation : ElementTree from lxml library with annotation element
        """
        self.radius = float(xmlannotation.find("radius").text)
        self.center = Point(int(xmlannotation.find("x").text),int(xmlannotation.find("y").text))
        
    def center_size(self):
        """ return de center and the size of the image .ndpi in nm """
        return self.center, 2*self.radius, 2*self.radius
    
    def contour(self, im, lens):
        """ 
        set pixels outside the contour to white
        Arguments:
        im : PIL image from HamamatsuImage
        lens: float with the lens of the image
        """
        pix = im.load()
        radius = self.radius*lens/CONV_FACT
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
    """ FreehandAnnotation class inherit from Annotation """
    
    def __init__(self):
        """Arguments:
        color: string with '#' then RGB hexadecimal color (e.g. '#00ffff')
        type: string
        displayname: string
        """
        super(FreehandAnnotation, self).__init__()
        self.x = []
        self.y = []
    
    def set_element(self, xmlannotation):
        """Arguments:
        xmlannotation : ElementTree from lxml library with annotation element
        """
        pointlist = xmlannotation.findall("pointlist/point")
        for point in pointlist:
            self.x.append(int(point.find('x').text))
            self.y.append(int(point.find('y').text))
    
    def print_element(self):
        print '\n'.join([str(el) for el in zip(self.x, self.y)])

    def center_size(self):
        """ return de center and the size of the image .ndpi in nm """
        xmin = min(self.x)
        xmax = max(self.x)
        ymax = max(self.y)
        ymin = min(self.y)
        center = Point((xmax+xmin)/2, (ymax+ymin)/2)
        return center, xmax-xmin, ymax-ymin
    
    def contour(self, im, lens):
        """ set pixels outside the contour to white 
        Arguments:
        im : PIL image from HamamatsuImage
        lens: float with the lens of the image
        """
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
        """ return a copy of the given image and add a border lines color 
        Arguments:
        im : PIL image
        color: 3-tuple with 'RGB' value (e.g. (0,0,0) for black)
        """
        newim= new('RGB', (im.size[0]+2, im.size[1]+2), color)
        newim.paste(im, (1,1))
        return newim
    
    def __contour_lines(self, lens):
        """ take the lines contour in nm and return the lines contour in pixels
        Arguments:
        lens: float with the lens of the image
        """
        lines = []
        xmin = min(self.x)
        ymin = min(self.y)
        for i in range (0, len(self.x)):
            xpix = (self.x[i]-xmin)*lens/CONV_FACT
            ypix = (self.y[i]-ymin)*lens/CONV_FACT
            lines.append((int(xpix), int(ypix)))
        xpix = (self.x[0]-xmin)*lens/CONV_FACT
        ypix = (self.y[0]-ymin)*lens/CONV_FACT
        lines.append((int(xpix), int(ypix)))
        return lines
    
    def __check_west_or_east_side(self, pix, initpoint, direction):
        """Arguments:
        pix: PixelAccess returned by PIL function load
        initpoint: 2-tuple with coordinates of first point
        direction: -1 to go on the west or 1 to go on the east
        """
        point = initpoint
        while (pix[point[0], point[1]] != (255, 255, 255)):
            pix[point[0], point[1]] = (255, 255, 255)
            point = (point[0]+direction, point[1])
        return point
    
    def __check_up_or_down_side(self, w, e, pix, direction, pixels):
        """Arguments:
        w: returned by __check_west_or_east_side function when direction = -1
        e: returned by __check_west_or_east_side function when direction = 1
        pix: PixelAccess returned by PIL function load
        direction: -1 to go on the west or 1 to go on the east
        pixels: list
        """
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
        """ Implementation of the flood fill algorithm with modification to make it faster
        Arguments:
        pixels: list with one 2-tuple with coordinates of the starting point
        im: PIL image
        """
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
    