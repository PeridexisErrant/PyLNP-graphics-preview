#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing a graphics preview canvas."""
from __future__ import print_function, unicode_literals, absolute_import

import sys

## FROM PyLNP tkgui/graphics
if sys.version_info[0] == 3:  # Alternate import names
    # pylint:disable=import-error
    from tkinter import *
    from tkinter.ttk import *
    import tkinter.messagebox as messagebox
    import tkinter.simpledialog as simpledialog
else:
    # pylint:disable=import-error
    from Tkinter import *
    from ttk import *
    import tkMessageBox as messagebox
    import tkSimpleDialog as simpledialog

## FROM PyLNP tkgui/tkgui
try:  # PIL-compatible library (e.g. Pillow); used to load PNG images (optional)
    # pylint:disable=import-error,no-name-in-module
    from PIL import Image, ImageTk
    has_PIL = True
except ImportError:  # Some PIL installations live outside of the PIL package
    # pylint:disable=import-error,no-name-in-module
    try:
        import Image
        import ImageTk
        has_PIL = True
    except ImportError:  # No PIL compatible library
        has_PIL = False

########################################

#from . import colors

def get_colors(colorscheme=None):
    """Return dictionary with keys=color_names, values=color_tuples"""
    # TODO:  With PyLNP, just use same func as color preview, ie:
    #cols = colors.get_colors(colorscheme)

    colors = [] # failure state of the above, so use vanilla colors
    if not colors:
        colors = [[0, 0, 0],
                  [0, 0, 128],
                  [0, 128, 0],
                  [0, 128, 128],
                  [128, 0, 0],
                  [128, 0, 128],
                  [128, 128, 0],
                  [192, 192, 192],
                  [128, 128, 128],
                  [0, 0, 255],
                  [0, 255, 0],
                  [0, 255, 255],
                  [255, 0, 0],
                  [255, 0, 255],
                  [255, 255, 0],
                  [255, 255, 255]]
    n = ['BLACK', 'BLUE', 'GREEN', 'CYAN', 'RED', 'MAGENTA', 'BROWN', 'LGRAY',
         'DGRAY', 'LBLUE', 'LGREEN', 'LCYAN', 'LRED', 'LMAGENTA', 'YELLOW',
         'WHITE']
    return dict(zip(n, [tuple(l) for l in cols]))
    
def open_tilesets(font, g_font):
    """Return tuple of the requested image objects"""
    # note:  this will be more complex once tileset previews etc are implemented
    return Image.open(font), Image.open(g_font)

def get_plan(plan=None):
    """Obviously a placeholder"""
    return [[(200, 'DGRAY'), (183, 'BLACK'), (209, 'BROWN')],
            [(',', 'BLUE'), ('O', 'BLACK'), (210, 'BROWN')],
            [("'", 'RED'), (197, 'RED'), ('+', 'RED')]]

def image_plan():
    """Return a plan to display with the selected graphics pack.

    Format:
        A list of rows, each of which is a list of tuples (char, color_name)
        'char' may be either a character, or it's ord
        color_name must be one of the names uses by DF, capitalised

        An invalid char will be converted to 219 (window border)
        An invalid color will be converted to 'BLACK'

        All tiles are converted to the ord of their chr, for later manipulation
    """
    n = ['BLACK', 'BLUE', 'GREEN', 'CYAN', 'RED', 'MAGENTA', 'BROWN', 'LGRAY',
         'DGRAY', 'LBLUE', 'LGREEN', 'LCYAN', 'LRED', 'LMAGENTA', 'YELLOW',
         'WHITE']
    plan = get_plan()
    for row in plan:
        for cell in row:
            tile, color = cell
            if not color in n:
                color = 'BLACK'
            while not type(tile) == int and not 0 <= tile <= 255:
                # loop ensures ord does not give out-of-range value
                try: tile = ord(tile)
                except: tile = 219
            cell = (tile, color)
    return plan


def make_tile(tileset, ord_int=219, color='BLACK'):
    """Returns an image objectof the tile, colored.

    Arguments:
        tileset:
            the Image object of the tileset to use
        ord_int:
            the ord integer of the character to use, illegal -> blank (ie 219)
        color:
            a RGB color tuple, illegal -> (0, 0, 0)

    Returns:
        An image object the size of a tile in the tileset
    """
    pass

def make_image(tileset, plan):
    """Returns an image object of the whole preview."""



class MyWindow(object):
    """Should show off a graphics preview."""
    # tester class, to work on methods
    def __init__(self, parent):
        """Constructor for a *very* basic window."""
        self.root = parent
        self.root.title("Graphics Preview")
        self.frame = Frame(parent)
        self.draw_preview()
        self.graphics_preview.pack()
        self.frame.pack()

    def draw_preview(self):
        """Draws the canvas and image."""
        # TODO: get correct tileset
        tileset = Image.open('CLA.png')
        plan = image_plan()
        PIL_preview_image = make_image(tileset, plan)

        # TODO:  make canvas of correct size,
        # save preview as tempfile gif,
        # paste into canvas
        self.graphics_preview = Canvas(
            width=160, height=160, highlightthickness=0,
            takefocus=False)
        self.graphics_preview.create_rectangle((0, 0, 160, 160), fill='blue')


if __name__ == "__main__":
    root = Tk()
    app = MyWindow(root)
    root.mainloop()
