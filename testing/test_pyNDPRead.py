#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""Unit testing of pyNDPRead."""

__author__ = "Xavier Moles Lopez <x.moleslo@gmail.com>"
__date__ = "16-nov.-2010"

import unittest
import numpy.testing as nt
import numpy as np
import src.hamamatsu.pyNDPRead as nread
import Image


filename = "C:/Examples/hama_slides/2.ndpi"
testfilename = "C:/Examples/09H00132_KI67.jpg"

class TestHamamatsuImage(unittest.TestCase):
    """Test methods in class HamamatsuImage."""
    def test_init(self):
        h_im = nread.HamamatsuImage(filename)
        im = Image.open(filename)
        x = im.tag.get(282)[0][0]
        y = im.tag.get(283)[0][0]
        print h_im.CONV_FACT, h_im.GetSourceLens()
        print ((1./x+1./y)/2)*40.0*10**7
        self.assertEqual(h_im.CONV_FACT, ((1./x+1./y)/2)*40.0*10**7)

    def test_get_image_data(self):
        h_im = nread.HamamatsuImage(filename)
        im = h_im.GetImageData(1440,900,20558705,-403075,0,0.539467)

    def test_get_image_info(self):
        h_im = nread.HamamatsuImage(filename)
        im_infos = h_im.GetSlideImageInfo()

    def test_get_image_data_px(self):
        h_im = nread.HamamatsuImage(filename)
        im = h_im.GetImagePx2D(1440,900,720,450,0.539467)
        im.show()

if __name__ == '__main__':
    unittest.main()
