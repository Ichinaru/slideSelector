#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""basic processings for annotation export."""

__author__ = "Xavier Moles Lopez <xmoleslo@gmail.com>"
__date__ = "13/01/2011"

import os
import os.path as osp
import Image, ImageDraw
from .annotations import get_annotation_list
from .hamamatsu import HamamatsuImage
from .custom_errors import CanNotWriteDirectoryError

class BaseExporter(object):
    """"Base exporter class"""
    def __init__(self, annotation_file, magnification):
        self.mag = magnification
        self.image_file = osp.splitext(annotation_file)[0]
        self.export_folder = osp.splitext(self.image_file)[0]
        self.annotations = get_annotation_list(annotation_file)
        try:
            os.mkdir(self.export_folder)
        except:
            if len(os.listdir(self.export_folder))>0:
                raise CanNotWriteDirectoryError(self.export_folder)

    def process(self):
        h_im = HamamatsuImage(self.image_file)
        self.cv = h_im.CONV_FACT
        for annotation in self.annotations:
            x, y, width, height = annotation.get_enclosing_rectangle()
            rectangle = h_im.GetImageNm2D(width, height, x, y, self.mag)
            rectangle.show()
            self.flood_fill(rectangle, annotation)
            self.safe_save(rectangle, annotation.title)

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
        lines = [tuple(r) for r in annotation.get_point_list_px(self.mag, self.cv)]
        draw.line(lines, fill=(255,255,255))
        bb_image = self.__border_lines(image, (0, 0, 0))
        wb_image = self.__border_lines(bb_image, (255, 255, 255))
        queue = [(1,1),]
        pixel_access = wb_image.load()
        for p in queue:
            if pixel_access[p[0], p[1]] != (255, 255, 255):
                w = self.__check_west_or_east_side(pixel_access, p, -1)
                e = self.__check_west_or_east_side(pixel_access,(p[0]+1,p[1]),1)
                self.__check_up_or_down_side(w, e, pixel_access, 1, queue)
                self.__check_up_or_down_side(w, e, pixel_access, -1, queue)

    def __border_lines(self, image, color):
        """ return a copy of the given image and add a border lines color
        Arguments:
        im : PIL image
        color: 3-tuple with 'RGB' value (e.g. (0,0,0) for black)
        """
        newim= Image.new('RGB', (image.size[0]+2, image.size[1]+2), color)
        newim.paste(image, (1,1))
        return newim

    def __check_west_or_east_side(self, pix, start, direction):
        """Arguments:
        pix: PixelAccess returned by PIL function load
        initpoint: 2-tuple with coordinates of first point
        direction: -1 to go on the west or 1 to go on the east
        """
        p = start
        while pix[p[0], p[1]] != (255, 255, 255):
            pix[p[0], p[1]] = (255, 255, 255)
            p = (p[0]+direction, p[1])
        return p

    def __check_up_or_down_side(self, w, e, pix, direction, queue):
        """Arguments:
        w: returned by __check_west_or_east_side function when direction = -1
        e: returned by __check_west_or_east_side function when direction = 1
        pix: PixelAccess returned by PIL function load
        direction: -1 to go up or 1 to go on the down
        queue: list of pixels
        """
        lastpixexist = False
        for p in range (w[0]+1, e[0]):
            if pix[p, w[1]+direction] != (255, 255, 255):
                lastpix = (p, w[1]+direction)
                lastpixexist = True
            else:
                if lastpixexist and (queue[-1] != lastpix):
                    queue.append(lastpix)
        if lastpixexist and (queue[-1] != lastpix):
            queue.append(lastpix)
