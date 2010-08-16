# -*- coding:utf-8 -*-
"""
Created on 12 août 2010

@author: Frederic Morel
"""
from enthought.traits.api import *
from enthought.traits.ui.api import  View, Item, ButtonEditor
from tkFileDialog  import askopenfilename 
from enthought.traits.ui.menu import OKButton, CancelButton
import Tkinter


class App(HasTraits):
    """ Camera object """

    roi = Enum('green', 'black', 'red', 'yellow', 'white', 'pink', 'light blue', 'turquoise',
        desc="",
        label="region a analyser", )

    rni = Enum('red', 'green', 'black', 'yellow', 'white', 'pink', 'light blue', 'turquoise',
        desc="",
        label="region a exclure", )
    
    filename =  String()

    browse = Button()

    def _browse_fired(self):
        master = Tkinter.Tk()
        master.withdraw() #hiding tkinter window
        filename = ""
        filename = askopenfilename(title="Open file", filetypes=[("ndpa file",".ndpa")])
        self.filename = filename

    view = View('roi', 'rni', Item('filename', show_label=False ), Item('browse', show_label=False ), buttons = [OKButton, CancelButton])