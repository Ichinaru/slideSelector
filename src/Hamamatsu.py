import os
import HamaWrapper
import Image
import numpy as np
os.environ['PATH'] = os.environ['PATH'] + ';' + os.path.abspath(os.path.dirname(__file__))

# All functions work the same way as NDPRead doc, except when needed you have to specify the frame dimension,
# this is equivalent to a call of SetCameraResolution() in NDRRead

# GetImageInfo(args) does not exists in NDPRead, this gives general informations on the image, useful to know the center 
# in the nanometer based coordinates system.

# Function whose name starts with Show means they will attempt to show the image on the screen after retrieving it from the file. These functions
# does not return any value.

class HamamatsuImage:
    """ Hamamatsu image class """
    
    _conversionfactor = 9200 # convert nm to pixels for a magnification of 1
    
    def __init__(self, filename):
        """Arguments:
        filename: string with absolute file name.
        """
        self.filename = filename
        
    def GetImageDataNm(self, physical_width, physical_height,x_center,y_center, z_plan, magnification):
        """Arguments:
        physical_width: long with the width in nm.
        physical_height: long with the height in nm.
        x_center: long with the physical X pos of the desired image in nm.
        y_center: long with the physical Y pos of the desired image in nm.
        z_plan: long with the physical Z (focal) pos of the desired image in nm.
        magnification: long with the objective magnification.
        """
        width = int(magnification*physical_width/HamamatsuImage._conversionfactor)+1
        height = int(magnification*physical_height/HamamatsuImage._conversionfactor)+1
        if os.path.exists(self.filename):
            return HamaWrapper.getImageData(self.filename, width, height,x_center,y_center, z_plan, magnification)
        else:
            print "Error: File not found!"
        
    def GetImageData(self, frame_width, frame_height,x_center,y_center, z_plan, magnification):
        """Arguments:
        frame_width: long with the width in pixel.
        frame_height: long with the height in pixel.
        x_center: long with the physical X pos of the desired image in nm.
        y_center: long with the physical Y pos of the desired image in nm.
        z_plan: long with the physical Z (focal) pos of the desired image in nm.
        magnification: long with the objective magnification.
        """
        if os.path.exists(self.filename):
            return HamaWrapper.getImageData(self.filename,frame_width, frame_height,x_center,y_center, z_plan, magnification)
        else:
            print "Error: File not found!"
            
    def GetMap(self,desired_frame_width,desired_frame_height):
        """Arguments:
        frame_width: long with the width in pixel.
        frame_height: long with the height in pixel.
        """
        if os.path.exists(self.filename):
            return HamaWrapper.getMap(self.filename,desired_frame_width,desired_frame_height)
        else:
            print "Error: File not found!"
            
    def GetZRange(self):
        if os.path.exists(self.filename):
            return HamaWrapper.getZRange(self.filename)
        else:
            print "Error: File not found!"
            
    def GetSourcePixelSize(self):
        if os.path.exists(self.filename):
            return HamaWrapper.getSourcePixelSize(self.filename)
        else:
            print "Error: File not found!"
            
    def GetImageWidth(self):
        if os.path.exists(self.filename):
            return HamaWrapper.getImageWidth(self.filename)
        else:
            print "Error: File not found!"
            
    def GetImageHeight(self):
        if os.path.exists(self.filename):
            return HamaWrapper.getImageHeight(self.filename)
        else:
            print "Error: File not found!"
            
    def GetSlideImage(self):
        if os.path.exists(self.filename):
            return HamaWrapper.getSlideImage(self.filename)
        else:
            print "Error: File not found!"
            
    def GetSourceLens(self):
        if os.path.exists(self.filename):
            return HamaWrapper.getSourceLens(self.filename)
        else:
            print "Error: File not found!"
            
    def GetImageInfo(self):
        if os.path.exists(self.filename):
            return HamaWrapper.getImageInfo(self.filename)
        else:
            print "Error: File not found!"
            
    def CleanUp(self):
        return HamaWrapper.cleanUp()
    
    def GetLastErrorMessage(self):
        print HamaWrapper.getLastErrorMessage();
        
    def ShowSourceSlide(self):
        if os.path.exists(self.filename):
            arr=HamaWrapper.getSlideImage(self.filename)
            im=Image.frombuffer("RGB",(arr.shape[2],arr.shape[1]),arr.data)
            im.show()
        else:
            print "Error: File not found!"
            
    def ShowMap(self,desired_frame_width, desired_frame_height):
        """Arguments:
        frame_width: long with the width in pixel.
        frame_height: long with the height in pixel.
        """
        if os.path.exists(self.filename):
            arr=HamaWrapper.getMap(self.filename,desired_frame_width, desired_frame_height)
            im=Image.frombuffer("RGB",(arr.shape[2],arr.shape[1]),arr.data)
            im.show()
        else:
            print "Error: File not found!"
            
    def GetImage(self,desired_frame_width, desired_frame_height,x_coord,y_coord,z_depth, magnification):
        """Arguments:
        frame_width: long with the width in pixel.
        frame_height: long with the height in pixel.
        x_center: long with the physical X pos of the desired image in nm.
        y_center: long with the physical Y pos of the desired image in nm.
        z_plan: long with the physical Z (focal) pos of the desired image in nm.
        magnification: long with the objective magnification.
        """
        if os.path.exists(self.filename):
            arr=HamaWrapper.getImageData(self.filename,desired_frame_width, desired_frame_height,x_coord,y_coord,z_depth, magnification)
            im=Image.frombuffer("RGB",(arr.shape[2],arr.shape[1]),arr.data)
            return im
        else:
            print "Error: File not found!"
    
    def GetImageNm(self,physical_width, physical_height,x_coord,y_coord,z_depth, magnification):
        """Arguments:
        physical_width: long with the width in nm.
        physical_height: long with the height in nm.
        x_center: long with the physical X pos of the desired image in nm.
        y_center: long with the physical Y pos of the desired image in nm.
        z_plan: long with the physical Z (focal) pos of the desired image in nm.
        magnification: long with the objective magnification.
        """
        width = int(magnification*physical_width/HamamatsuImage._conversionfactor)+1
        height = int(magnification*physical_height/HamamatsuImage._conversionfactor)+1
        if os.path.exists(self.filename):
            arr=HamaWrapper.getImageData(self.filename,width, height,x_coord,y_coord,z_depth, magnification)
            im=Image.frombuffer("RGB",(arr.shape[2],arr.shape[1]),arr.data)
            return im
        else:
            print "Error: File not found!"
            
    def ColorConvolution(self, width, height,x,y,z,mag,stain_matrix):
        if os.path.exists(self.filename):
            arr=HamaWrapper.convolution(self.filename, width, height,x,y,z,mag,stain_matrix)
            return arr;
        else:
            print "Error: File not found!"
            
    def HDAB_stainmatrix(self):
        stain=np.zeros((3,3),float)
        stain[0][0]=0.650;
        stain[0][1]=0.704;
        stain[0][2]=0.286;
        stain[1][0]=0.268;
        stain[1][1]=0.570;
        stain[1][2]=0.776;
        stain[2][0]=0.0;
        stain[2][1]=0.0;
        stain[2][2]=0.0;
        return stain;

    
    
    
    
    
    
    
    