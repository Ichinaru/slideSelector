# -*- coding:utf-8 -*-
"""
Created on 23 août 2010

@author: Frederic Morel
"""

from distutils.core import setup
import py2exe
from glob import glob
  
#data_files = [("Microsoft.VC90.CRT", glob(r'C:/Documents and Settings/Administrator/My Documents/Python/SlideSelector/src/ms-vc-runtime/*.*'))]

setup(console=['slideSelector.py'], options = {"py2exe": {"packages": ["gzip", "lxml"]}})