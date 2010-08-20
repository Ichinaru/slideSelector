#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""Unit test."""

__author__ = "Xavier Moles Lopez <x.moleslo@gmail.com>"
__date__ = "Aug 20, 2010"

import unittest

from annotation import *
from lxml import etree
from ndpviewstate import *
from point import *
from Hamamatsu import *
from math import *
from Image import *
from slideSelector import *
import ImageDraw

filename = ("C:/Documents and Settings/Administrator/My Documents/Python/SlideSelector/res/09H00132_KI67.ndpi.ndpa")
roi = color('red')

colors = (color('green'), color('light blue'))


class TestSelection(unittest.TestCase):
    def test_green(self):
        rni = colors[0]
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
