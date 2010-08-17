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
        self.center.set_x(int(xmlannotation.find("x").text))
        self.center.set_y(int(xmlannotation.find("y").text))
        
    # return de center and the size of the image .ndpi in nm
    def center_size(self):
        return self.center, 2*self.radius, 2*self.radius
    
    # remove outside pixels
    def contour(self, im, lens):
        pix = im.load()
        radius = self.radius*lens/9200
        print radius
        for y in range (0, im.size[0]):
            x = 0
            while (sqrt((x-radius)**2+(y-radius)**2)>radius and x<im.size[1]):
                pix [x, y] = (255, 255, 255)
                x = x + 1
            x = im.size[1]-1
            while (sqrt((x-radius)**2+(y-radius)**2)>radius and x>=0):
                pix [x, y] = (255, 255, 255)
                x = x - 1
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
    
    # return de center and the size of the image .ndpi in nm
    def center_size(self):
        xmin = min(self.x)
        xmax = max(self.x)
        ymax = max(self.y)
        ymin = min(self.y)
        center = Point((xmax+xmin)/2, (ymax+ymin)/2)
        return center, xmax-xmin, ymax-ymin
    
    # remove outside pixels
    def contour(self, im, lens):
        #remove outside pixels
        if (self.displayname != 'Rectangular Annotation'):
            #drawing contour
            draw = ImageDraw.Draw(im)
            line = []
            xmin = min(self.x)
            ymin = min(self.y)
            for i in range (0, len(self.x)):
                xpix = (self.x[i]-xmin)*lens/9200
                ypix = (self.y[i]-ymin)*lens/9200
                line.append((int(xpix), int(ypix)))
            xpix = (self.x[0]-xmin)*lens/9200
            ypix = (self.y[0]-ymin)*lens/9200
            line.append((int(xpix), int(ypix)))
            draw.line(line , fill=(255, 255, 255))
            newim= new('RGB', (im.size[0]+2, im.size[1]+2), (0, 0, 0))
            line.pop()
            newim.paste(im, (1,1))
            newim2= new('RGB', (im.size[0]+4, im.size[1]+4), (255, 255, 255))
            newim2.paste(newim, (1,1))
            pixels =[]
            pixels.append((1,1))
            im = self.flood_fill(pixels, newim2)

        return im
            
    def flood_fill(self, pixels, im):
        pix = im.load()
        print 'processing... (maybe go to take a coffee)'
        for pixel in pixels:
            if (pix[pixel[0], pixel[1]] != (255, 255, 255)):
                w = pixel
                e = pixel
                while (pix[w[0], w[1]] != (255, 255, 255)):
                    pix[w[0], w[1]] = (255, 255, 255)
                    w = (w[0]-1, w[1])
                e = (e[0]+1, e[1])
                while (pix[e[0], e[1]] != (255, 255, 255)):
                    pix[e[0], e[1]] = (255, 255, 255)
                    e = (e[0]+1, e[1])
                lastpixexist = False
                for p in range (w[0]+1, e[0]):
                    if (pix[p, w[1]+1] != (255, 255, 255)):
                        lastpix = (p, w[1]+1)
                        lastpixexist = True
                    else:
                        if(lastpixexist):
                            if (pixels[-1]!=lastpix):
                                pixels.append(lastpix)
                if(lastpixexist):
                    if (pixels[-1]!=lastpix):
                        pixels.append(lastpix)
                
                for p in range (w[0]+1, e[0]):
                    if (pix[p, w[1]-1] != (255, 255, 255)):
                        lastpix = (p, w[1]-1)
                        lastpixexist = True
                    else:
                        if(lastpixexist):
                            if (pixels[-1]!=lastpix):
                                pixels.append(lastpix)
                if(lastpixexist):
                    if (pixels[-1]!=lastpix):
                        pixels.append(lastpix)
        print 'done'
        return im
    
    """
    
            removepoint = []
            i=0
            for point in line:
                if not(point in removepoint):
                    if (i != len(line)-1):
                        icopy = i+1
                    else:
                        icopy = 0
                    while (point[1]==line[icopy][1]):
                        removepoint.append(line[icopy])
                        icopy=icopy+1
                i=i+1
            for p in removepoint:
                line.remove(p)                        
            #
            isolatepoints = []
            i=0
            for point in line:
                if (point != line[-1]):
                    if not((point[1]<line[i+1][1] and  point[1]>line[i-1][1]) or 
                       (point[1]>line[i+1][1] and  point[1]<line[i-1][1])):
                        isolatepoints.append(point)
                else:
                    if not((point[1]<=line[0][1] and  point[1]>=line[i-1][1]) or 
                       (point[1]>=line[0][1] and  point[1]<=line[i-1][1])):
                        isolatepoints.append(point)
                i=i+1
            
            isolatepoints=self.find_isolate(pix, im.size[0], im.size[1], isolatepoints)
                        
            print "isolatepoints", isolatepoints

            for y in range (0, im.size[1]):
                outsidepix = True
                findisolate = False
                for x in range (0, im.size[0]):
                    if (outsidepix):
                        if (pix[x, y] != (0, 0, 0)):
                            pix[x, y] = (0, 0, 0)
                        else:
                            if (int(x), int(y)) in isolatepoints:
                                findisolate = True
                            if (pix[x+1, y] != (0, 0, 0)):
                                if not(findisolate):
                                    outsidepix = False
                                else:
                                    findisolate = False
                    else:
                        if (pix[x, y] == (0, 0, 0)):
                            if (x==im.size[0]-1):
                                outsidepix = True 
                            else:
                                if (x, y) in isolatepoints:
                                    findisolate = True
                                if(pix[x+1, y] != (0, 0, 0)):
                                    if not(findisolate):
                                        outsidepix = True
                                    else:
                                        findisolate = False      
                                     
    
    def find_isolate(self, pix, sizex, sizey, isolatepoints):
        for isolate in isolatepoints:
            print isolate
            point = (-1,-1)
            for i in range (-1, 2):
                if (isolate[0]+i<sizex and isolate[0]+i>-1 and isolate[1]+1<sizey):
                    if (pix[isolate[0]+i, isolate[1]+1] == (0, 0, 0) and 
                        not((isolate[0]+i, isolate[1]+1) in isolatepoints)):
                        point = (isolate[0]+i, isolate[1]+1)
                        break
                if (isolate[0]+i<sizex and isolate[0]+i>-1 and isolate[1]-1>-1):
                    if (pix[isolate[0]+i, isolate[1]-1] == (0, 0, 0) and
                        not((isolate[0]+i, isolate[1]-1) in isolatepoints)):
                        point = (isolate[0]+i, isolate[1]-1)
                        break
            if (point != (-1,-1)):
                findnotblack = False
                findblack = False
                for x in range (1, sizex-point[0]):
                    if(findnotblack == False):
                        if(pix[point[0]+x, point[1]]!= (0, 0, 0)):
                            print "findnotblackD"
                            findnotblack = True
                    else:
                        if(pix[point[0]+x, point[1]] == (0, 0, 0)):
                            print "findblackD"
                            findblack = True
                            break
                if (not(findblack)):
                    findnotblack = False
                    for x in range (1, isolate[0]):
                        if(findnotblack == False):
                            if(pix[point[0]-x, point[1]]!= (0, 0, 0)):
                                print "findnotblackG"
                                findnotblack = True
                        else:
                            if(pix[point[0]-x, point[1]] == (0, 0, 0)):
                                print "findblackG"
                                findblack = True
                                break
                if(not(findblack)):
                    print point
                    isolatepoints.append(point)
                    #self.find_isolate(pix, isolate, sizex, sizey, isolatepoints)
        return isolatepoints
    """ 
        