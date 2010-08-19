# -*- coding:utf-8 -*-
"""
Created on 9 août 2010

@author: Frederic Morel
"""
from math import *

class Point:
    """ Point class """
    
    def __init__(self, x, y):
        """Arguments:
        x: int with x-coordinate
        y: int with y-coordinate
        """
        self.x = x
        self.y = y
        
    def distance(self, point):
        """
        return the distance between this point and the given point
        Arguments:
        point : Point
        """
        return sqrt((self.x-point.x)**2+(self.y-point.y)**2)