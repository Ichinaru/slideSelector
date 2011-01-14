#! /bin/usr/env python
# -*- coding: utf-8 -*-

"""Thin Wrapper around the NDPRead library using ctypes."""

__author__ = "Xavier Moles Lopez <x.moleslo@gmail.com>"
__date__ = "16/11/2010"

import os
from numpy import asarray
from ctypes import *
from .custom_errors import FileNotFoundError, CleanUpError
import Image

# TODO: Harmonize naming convention.

# Because of the NDPRead.dll dependencies, we need to change the working
# directory.
p = os.path.abspath(os.path.split(__file__)[0])
os.chdir(p)

hama = cdll.LoadLibrary("NDPRead.dll")

hama.GetSourceLens.restype = c_float
hama.GetImageWidth.restype = c_long
hama.GetImageHeight.restype = c_long
hama.GetImageData.restype = c_long

class HamamatsuImage:

    def __init__(self, filename):
        """Argument:
        filename -- string with absolute file name.
        """
        if os.path.exists(filename):
            self.filename = str(filename)
            im = Image.open(filename)
            x = im.tag.get(282)[0][0]
            y = im.tag.get(283)[0][0]
            self.source_lens = hama.GetSourceLens(self.filename)
            self.CONV_FACT = ((1./x+1./y)/2)*self.source_lens*10**7
            self.physical_width = hama.GetImageWidth(self.filename)
            self.physical_height = hama.GetImageHeight(self.filename)
        else:
            raise FileNotFoundError(filename)

    def GetSourceLens(self):
        return self.source_lens

    def GetImageWidthPx(self, magnification):
        return int(1.0*magnification*self.physical_width/self.CONV_FACT)+1    

    def GetImageHeightPx(self, magnification):
        return int(1.0*magnification*self.physical_height/self.CONV_FACT)+1

    def GetSlideImageInfo(self):
        o_nPhysicalX = c_long()
        o_nPhysicalY = c_long()
        o_nPhysicalWidth = c_long()
        o_nPhysicalHeight = c_long()
        i_pBuffer = c_void_p()
        io_nBufferSize = c_long()
        o_nPixelWidth = c_long()
        o_nPixelHeight = c_long()


        hama.GetSlideImage(self.filename,
                           byref(o_nPhysicalX), byref(o_nPhysicalY),
                           byref(o_nPhysicalWidth), byref(o_nPhysicalHeight),
                           i_pBuffer, byref(io_nBufferSize),
                           byref(o_nPixelWidth), byref(o_nPixelHeight))

        return [o_nPhysicalWidth.value, o_nPhysicalHeight.value, o_nPhysicalX.value, o_nPhysicalY.value]

    def GetMapInfo(self):
        o_nPhysicalX = c_long()
        o_nPhysicalY = c_long()
        o_nPhysicalWidth = c_long()
        o_nPhysicalHeight = c_long()
        i_pBuffer = c_void_p()
        io_nBufferSize = c_long()
        o_nPixelWidth = c_long()
        o_nPixelHeight = c_long()
        hama.SetCameraResolution(100,100)


        hama.GetMap(self.filename,
                    byref(o_nPhysicalX), byref(o_nPhysicalY),
                    byref(o_nPhysicalWidth), byref(o_nPhysicalHeight),
                    i_pBuffer, byref(io_nBufferSize),
                    byref(o_nPixelWidth), byref(o_nPixelHeight))

        return [o_nPhysicalWidth.value, o_nPhysicalHeight.value, o_nPhysicalX.value, o_nPhysicalY.value]

    def GetMap(self, i_nWidth, i_nHeight):
        cu = hama.CleanUp()
        if cu != 0:
            o_nPhysicalX = c_long()
            o_nPhysicalY = c_long()
            o_nPhysicalWidth = c_long()
            o_nPhysicalHeight = c_long()
            i_pBuffer = c_void_p()
            io_nBufferSize = c_long()
            o_nPixelWidth = c_long()
            o_nPixelHeight = c_long()
            hama.SetCameraResolution(i_nWidth,i_nHeight)

            hama.GetMap(self.filename,
                        byref(o_nPhysicalX), byref(o_nPhysicalY),
                        byref(o_nPhysicalWidth), byref(o_nPhysicalHeight),
                        i_pBuffer, byref(io_nBufferSize),
                        byref(o_nPixelWidth), byref(o_nPixelHeight))

            i_pBuffer = (c_byte * 3*i_nWidth*i_nHeight)()
            print io_nBufferSize.value
            hama.GetMap(self.filename,
                        byref(o_nPhysicalX), byref(o_nPhysicalY),
                        byref(o_nPhysicalWidth), byref(o_nPhysicalHeight),
                        i_pBuffer, byref(io_nBufferSize),
                        byref(o_nPixelWidth), byref(o_nPixelHeight))

            return Image.frombuffer("RGB",(o_nPixelWidth.value,o_nPixelHeight.value),i_pBuffer,"raw","BGR",0,-1)
        else:
            raise CleanUpError(cu)

    def GetImageData(self, frame_width, frame_height,x_center,y_center, z_plan, magnification):
        """Arguments:
        frame_width: long with the width in pixel.
        frame_height: long with the height in pixel.
        x_center: long with the physical X pos of the desired image in nm.
        y_center: long with the physical Y pos of the desired image in nm.
        z_plan: long with the physical Z (focal) pos of the desired image in nm.
        magnification: long with the objective magnification.
        """
        i_pBuffer = c_void_p()
        i_nPhysicalXPos = x_center
        i_nPhysicalYPos = y_center
        i_nPhysicalZPos = z_plan
        i_fMag = c_float(magnification)
        o_nPhysicalWidth = c_long()
        o_nPhysicalHeight = c_long()
        io_nBufferSize = c_long()
        hama.SetCameraResolution(frame_width,frame_height)

        hama.GetImageData(self.filename,
                          i_nPhysicalXPos, i_nPhysicalYPos, i_nPhysicalZPos,
                          i_fMag, byref(o_nPhysicalWidth), byref(o_nPhysicalHeight),
                          i_pBuffer, byref(io_nBufferSize))


        # For some reason, the second call is mandatory to copy the data.
        i_pBuffer = (c_byte * io_nBufferSize.value)()
        hama.GetImageData(self.filename,
                          i_nPhysicalXPos, i_nPhysicalYPos, i_nPhysicalZPos,
                          i_fMag, byref(o_nPhysicalWidth), byref(o_nPhysicalHeight),
                          i_pBuffer, byref(io_nBufferSize))

        return Image.frombuffer("RGB",(frame_width,frame_height),i_pBuffer,"raw","BGR",0,-1)

    def GetImageNm2D(self,width, height,x_coord,y_coord, magnification):
        """Return the image given the positions and extent in pixels. Works with 2D images.

        Arguments:
        width: frame_width in nm.
        height: frame height in nm.
        x_coord: frame x center in nm.
        y_coord: frame y center in nm.
        magnification: long with the objective magnification.
        size_offset: int: how many pixels more in height and width
        """
        frame_width = int(round(1.0*magnification*width/self.CONV_FACT)+1)
        frame_height = int(round(1.0*magnification*height/self.CONV_FACT)+1)
        return self.GetImageData(frame_width, frame_height, x_coord, y_coord, 0, magnification)

    def GetImagePx2D(self,width, height,x_coord_px,y_coord_px, magnification):
        """Return the image given the positions and extent in pixels. Works with 2D images.

        Arguments:
        width: frame_width in pixels.
        height: frame height in pixels.
        x_coord_px: frame x center in pixels.
        y_coord_px: frame y center in pixels.
        magnification: long with the objective magnification.
        """
        im_info = self.GetMapInfo()

        # x_orig = physical_x - (physical_width/2.0)
        x_orig = im_info[2] - (im_info[0]/2.0)
        y_orig = im_info[3] - (im_info[1]/2.0)
        
        x_coord = int(x_orig + (x_coord_px * self.CONV_FACT) / magnification)
        y_coord = int(y_orig + (y_coord_px * self.CONV_FACT) / magnification)
        return self.GetImageData(width, height, x_coord, y_coord, 0, magnification)

    def GetCoordinatesInNm(self, x, y, magnification):
        xa = asarray(x)
        ya = asarray(y)
        im_info = self.GetMapInfo()

        # x_orig = physical_x - (physical_width/2.0)
        x_orig = im_info[2] - (im_info[0]/2.0)
        y_orig = im_info[3] - (im_info[1]/2.0)

        x_coord = x_orig + (xa * self.CONV_FACT) / magnification
        y_coord = y_orig + (ya * self.CONV_FACT) / magnification
        
        return x_coord.astype(int), y_coord.astype(int)