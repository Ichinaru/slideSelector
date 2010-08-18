# -*- coding:utf-8 -*-
"""
Created on 9 août 2010

@author: Frederic Morel
"""
from math import *

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def distance(self, point):
        return sqrt((self.x-point.x)**2+(self.y-point.y)**2)