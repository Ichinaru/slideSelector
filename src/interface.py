# -*- coding:utf-8 -*-
"""
Created on 12 août 2010

@author: Frederic Morel
"""
from enthought.traits.api import Enum, File, HasTraits
from enthought.traits.ui.api import  View, Item
from enthought.traits.ui.menu import OKButton, CancelButton


class Interface(HasTraits):
    """ Interface object """

    roi = Enum('green', 'black', 'red', 'yellow', 'white', 'pink', 'light blue', 'turquoise',
        desc="",
        label="region a analyser", )
    rni = Enum('red', 'green', 'black', 'yellow', 'white', 'pink', 'light blue', 'turquoise',
        desc="",
        label="region a exclure", )
    
    filename =  File()

    view = View('roi', 'rni', Item('filename', show_label=False ), buttons = [OKButton, CancelButton])