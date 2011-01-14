#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""Annotation parser module."""

__author__ = "Xavier Moles Lopez <x.moleslo@gmail.com>"
__date__ = "24-nov.-2010"

from lxml import etree
from numpy import empty, int32, asarray
from enthought.traits.api import HasTraits, String, Array, Int, Float

class Annotation(HasTraits):
    title = String()
    x = Int()
    y = Int()
    z = Int(0)
    lens = Float()

    color = String()
    type = String()
    displayname = String()

    def __init__(self, viewstate):
        self.title = viewstate.find('title').text
        self.x = int(viewstate.find('x').text)
        self.y = int(viewstate.find('y').text)        
        self.z = int(viewstate.find('z').text)
        self.lens = float(viewstate.find('lens').text)

        self.annotation = viewstate.find("annotation")

        self.color = self.annotation.get("color")
        self.type = self.annotation.get("type")
        self.displayname = self.annotation.get("displayname")

class FreehandAnnotation(Annotation):
    point_list = Array(dtype=int32, shape=(None,2))

    def __init__(self, viewstate):
        super(FreehandAnnotation, self).__init__(viewstate)
        if self.type != "freehand":
            raise TypeError("Wrong annotation type!")

        point_list = self.annotation.findall('pointlist/point')
        self.point_list = empty(shape=(len(point_list), 2))
        for i,point in enumerate(point_list):
            self.point_list[i,0] = int(point.find('x').text)
            self.point_list[i,1] = int(point.find('y').text)
        self.xmax = self.point_list[:,0].max()
        self.xmin = self.point_list[:,0].min()
        self.ymax = self.point_list[:,1].max()
        self.ymin = self.point_list[:,1].min()

    def get_enclosing_rectangle(self):
        x = int((self.xmax+self.xmin)/2.0)
        y = int((self.ymax+self.ymin)/2.0)
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        return x, y, width, height

    def get_point_list_px(self, mag, cv):
        sz = self.point_list.shape[0]
        point_list_px = empty(shape=(sz+1,2))
        for i in xrange(sz+1):
            point_list_px[i,0] = (self.point_list[i%sz,0] - self.xmin)*mag/cv
            point_list_px[i,1] = (self.point_list[i%sz,1] - self.ymin)*mag/cv
        return point_list_px

    def get_enclosing_rectangle_px(self, mag, cv):
        pl = self.get_point_list_px(mag, cv)
        xmax = pl[:,0].max()
        xmin = pl[:,0].min()
        ymax = pl[:,1].max()
        ymin = pl[:,1].min()
        x = int((xmax+xmin)/2.0)
        y = int((ymax+ymin)/2.0)
        width = xmax - xmin
        height = ymax - ymin
        return x, y, width, height

def get_annotation_list(filename):
    """Return an lxml etree. The root of it is on the ndpviewstate."""
    xmltree = etree.parse(filename)
    root = xmltree.getroot()
    viewstate_list = root.findall('ndpviewstate')

    annotation_list = []

    for viewstate in viewstate_list:
        try:
            annotation_list.append(FreehandAnnotation(viewstate))
        except Exception as e:
            print e 

    return annotation_list





