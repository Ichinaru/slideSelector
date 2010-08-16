# -*- coding:utf-8 -*-
"""
Created on 9 août 2010

@author: Frederic Morel
"""

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y