#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""basic processings for annotation export."""

__author__ = "Xavier Moles Lopez <xmoleslo@gmail.com>"
__date__ = "13/01/2011"

import os
import os.path as osp
import Image, ImageDraw
from numpy import ceil
from .annotations import get_annotation_list
from .hamamatsu import HamamatsuImage
from .hamamatsu.pyNDPRead import hama
from .custom_errors import CanNotWriteDirectoryError

class BaseExporter(object):
    """"Base exporter class"""
    def __init__(self, annotation_file, magnification):
        self.mag = float(magnification)
        self.image_file = osp.splitext(annotation_file)[0]
        self.export_folder = osp.splitext(self.image_file)[0]
        self.annotations = get_annotation_list(annotation_file)
        try:
            os.mkdir(self.export_folder)
        except:
            if len(os.listdir(self.export_folder))>0:
                pass
#                raise CanNotWriteDirectoryError(self.export_folder)

    def process(self):
        h_im = HamamatsuImage(self.image_file)
        self.cv = h_im.CONV_FACT
        for annotation in self.annotations:
            x, y, width, height = annotation.get_enclosing_rectangle()
            rectangle = h_im.GetImageNm2D(width, height, x, y, self.mag,5)
            im = self.flood_fill(rectangle, annotation)
            self.safe_save(im, annotation.title)

    def safe_save(self, image, name):
        export_file_fmt = self.export_folder + os.sep + name + '{0}.bmp'
        export_file = export_file_fmt.format('')
        if osp.exists(export_file):
            i=1
            while osp.exists(export_file_fmt.format('_'+str(i))):
                i+=1
            export_file = export_file_fmt.format('_'+str(i))
        image.save(export_file, "BMP")

    def flood_fill(self, image, annotation):
        draw = ImageDraw.Draw(image)
        lines = [ (r[0]+2,r[1]+2) for r in annotation.get_point_list_px(self.mag,self.cv)]
        draw.line(lines,fill=(255,255,255))
        wi, he = image.size
        draw.rectangle([(0,0),(wi-1,he-1)], outline=(255, 255, 255))
        draw.rectangle([(1,1),(wi-2,he-2)], outline=(0, 0, 0))
        queue = [(1,1),]
        pixel_access = image.load()
        for p in queue:
            if pixel_access[p[0], p[1]] != (255, 255, 255):
                w = self.__check_west_or_east_side(pixel_access, p, -1)
                e = self.__check_west_or_east_side(pixel_access,(p[0]+1,p[1]),1)
                self.__check_up_or_down_side(w, e, pixel_access, 1, queue)
                self.__check_up_or_down_side(w, e, pixel_access, -1, queue)
        return image

    def __check_west_or_east_side(self, pix, start, direction):
        """Arguments:
        pix: PixelAccess returned by PIL function load
        initpoint: 2-tuple with coordinates of first point
        direction: -1 to go on the west or 1 to go on the east
        """
        point = start
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