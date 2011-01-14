#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""Entry point of the software."""

__author__ = "Xavier Moles Lopez <xmoleslo@gmail.com>"
__date__ = "13/01/2011"

from selectors import BaseSelector

if __name__ == '__main__':
    bs = BaseSelector(folder='C:/Examples/hama_slides')
    bs.configure_traits()
  