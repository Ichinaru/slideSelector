#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""Selector modules."""

__author__ = "Xavier Moles Lopez <xmoleslo@gmail.com>"
__date__ = "13/01/2011"

import os
from enthought.traits.api import HasTraits, Directory, Button, Enum
from enthought.traits.ui.api import View

from processing import BaseExporter

def file_filter(file_list, extension, abs_root=''):
    filtered = []
    for f in file_list:
        ex = os.path.splitext(f)[1]
        if ex.endswith(extension):
            if abs_root.endswith('/'):
                filtered.append(abs_root+f)
            else:
                filtered.append(abs_root+'/'+f)
                
    return filtered

class BaseSelector(HasTraits):
    """Basic slide selector. Take a directory as an input and return the
    bmp images of the slides in that directory that have an associated
    annotation file.
    """
    folder = Directory
    magnification = Enum(1,2,4,10,20,40, label='Magnification')
    start = Button('Start Processing')

    view = View('folder', 'magnification', 'start')

    def process(self):
        """Process the specified folder"""
        file_list = os.listdir(self.folder)
        annotation_files = file_filter(file_list, 'ndpa', abs_root=self.folder)
        for an_file in annotation_files:
            exporter = BaseExporter(an_file, self.magnification)
            exporter.process()

    def _start_fired(self):
        self.process()
