#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""Custom errors module."""

__author__ = "Xavier Moles Lopez <x.moleslo@gmail.com>"
__date__ = "22-nov.-2010"

import os.path as osp

class FileNotFoundError(Exception):
    """Error thrown when providing a file that does not exists.
    """

    def __init__(self, missing_file_name):
        """Common interface for missing file.

        Arguments:
        - missing_file_name : name of the missing file

        """
        self.missing_file_name = missing_file_name

    def __str__(self):
        """Construct the error string."""
        return u'File %s does not exists!' % (self.missing_file_name,)

class CleanUpError(Exception):
    """Error thrown for clean up errors."""
    def __init__(self, cu):
        self.clean_up_code = cu

    def __str__(self):
        return u'Could not make clean up! Code returned: {0}'.format(self.clean_up_code)

class CanNotWriteDirectoryError(Exception):
    """Error thrown when unable to write in a folder."""
    def __init__(self, folder):
        self.directory = folder
        self.root_dir = osp.split(folder)[0]

    def __str__(self):
        return u'Could not write folder {0} in folder {1}.\n\
        Please make sure you have the authorization to write in {1}'.format(self.directory, self.root_dir)
