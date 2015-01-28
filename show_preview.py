#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing a graphics preview canvas."""
from __future__ import print_function, unicode_literals, absolute_import

import os, sys

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
    return dict(zip(n, [tuple(l) for l in colors]))
    
def open_tileset():
    """Return image object for the requested tileset"""
    # note:  this will be more complex once tileset previews etc are implemented
    return Image.open('CLA.png')

def get_plan(plan=None):
    """Obviously a placeholder"""
    # TODO:  make this not a placeholder
    return [[[200, 'DGRAY'], [183, 'BLACK'], [209, 'BROWN']],
            [[',', 'BLUE'], ['O', 'BLACK'], [210, 'BROWN']],
            [["'", 'RED'], [197, 'RED'], ['+', 'RED']]]

def image_plan():
    """Return a plan to display with the selected graphics pack.

    Format:
        A list of rows, each of which is a list of lists [char, color_name]
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
            if not cell[1] in n:
                cell[1] = 'BLACK'
            tile = cell[0]
            if isinstance(tile, str):
                try:
                    tile = ord(tile)
                except:
                    tile = 219
            if isinstance(tile, int):
                if not 0 <= tile <= 255:
                    tile = 219
            else:
                tile = 219
            cell[0] = tile
    return plan


def make_tile(tileset, ord_int=219, color=(0, 0, 0)):
    """Returns an image objectof the tile, colored.

    Arguments:
        tileset:
            the Image object of the tileset to use
        ord_int:
            the ord integer of the character to use
        color:
            a RGB color tuple, illegal

    Returns:
        Image object of the tile
    """
    tile_x, tile_y = tuple(int(n/16) for n in tileset.size)
    x = 16 * (ord_int % tile_x)
    y = 16 * (ord_int // tile_y)
    tile = tileset.crop((x, y, x + tile_x, y + tile_y)).copy()
    color_tile = Image.new('RGB', (tile_x , tile_y), color)
    tile.paste(color_tile, None, tile)
    tile.paste(color, None, tile)
    return tile.convert('RGB')


def make_image(tileset, plan):
    """Returns an image object of the whole preview."""
    c = get_colors()
    tileset = open_tileset()
    tile_x, tile_y = tuple(int(n/16) for n in tileset.size)
    preview = Image.new('RGB', (tile_x * len(plan[0]), tile_y * len(plan)),
                        (0, 0, 0))
    for y, row in enumerate(plan):
        for x, cell in enumerate(row):
            char, color = cell[0], cell[1]
            tile = make_tile(tileset, char, c[color])
            box = (x, y, x + tile_x, y + tile_y)
            preview.paste(tile, box)
    return preview


class MyWindow(object):
    """Should show off a graphics preview."""
    # tester class, to work on methods
    def __init__(self, parent):
        """Constructor for a *very* basic window."""
        self.root = parent
        self.root.title("Graphics Preview")
        self.frame = Frame(parent)
        self.draw_preview()
        self.preview.pack()
        self.frame.pack()

    def draw_preview(self):
        """Draws the canvas and image."""
        tileset = open_tileset()
        plan = image_plan()
        PIL_image = make_image(tileset, plan)
        PIL_image.save('preview.gif', format='GIF')
        self.TK_image = PhotoImage(file='preview.gif')
        self.preview = Canvas(
            width=PIL_image.size[0], height=PIL_image.size[1],
            highlightthickness=0, takefocus=False)
        self.preview.create_image(27, 27, image=self.TK_image)


if __name__ == "__main__":
    root = Tk()
    app = MyWindow(root)
    root.mainloop()
