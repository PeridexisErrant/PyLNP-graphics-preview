#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing a graphics preview canvas."""
from __future__ import print_function, unicode_literals, absolute_import

import sys

if sys.version_info[0] == 3:  # Alternate import names
    # pylint:disable=import-error
    from tkinter import *
    from tkinter.ttk import *
else:
    # pylint:disable=import-error
    from Tkinter import *
    from ttk import *

try:  # PIL-compatible library (e.g. Pillow); used to load PNG images (optional)
    # pylint:disable=import-error,no-name-in-module
    from PIL import Image
    has_PIL = True
except ImportError:  # Some PIL installations live outside of the PIL package
    # pylint:disable=import-error,no-name-in-module
    try:
        import Image
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

def get_plan(plan='random'):
    """Obviously a placeholder"""
    # TODO:  make this not a placeholder
    if plan == 'random':
        import random
        size, plan = 20, []
        n = ['BLACK', 'BLUE', 'GREEN', 'CYAN', 'RED', 'MAGENTA', 'BROWN',
             'LGRAY',
             'DGRAY', 'LBLUE', 'LGREEN', 'LCYAN', 'LRED', 'LMAGENTA', 'YELLOW',
             'WHITE']
        for _ in range(size):
            a = []
            plan.append(a)
            for _ in range(size):
                a.append([random.randint(0, 255), random.choice(n),
                          random.choice(n)])
        return plan
    return [[[17, 'DGRAY', ''], [19, 'LGRAY', ''], [209, 'BROWN', '']],
            [[',', 'BLUE', ''], ['O', 'YELLOW', ''], [210, 'BROWN', '']],
            [["'", 'RED', ''], [197, 'RED', ''], ['+', 'RED', '']]]

def image_plan(plan=None, text=False):
    """Return a plan to display with the selected graphics pack.

    Format:
        if text:
            A string, lines separated by newlines (for displaying font tiles)
        else:
            A list of rows, each of which is a list of lists
                [char, fg_color_name, bg_color_name]
            'char' may be either a character, or it's ord
            color_name must be one of the names uses by DF, capitalised

        An invalid or missing char will be converted to 219 (window border)
        An invalid or missing color will be converted to 'BLACK'

        All tiles are converted to the ord of their chr, for later manipulation
    """
    if plan is None:
        plan = get_plan()
    if text and isinstance(plan, str):
        plan = [zip(list(line), ['WHITE']*len(plan), ['BLACK']*len(plan))
                for line in plan.split('\n')]
    # validate plan
    n = ['BLACK', 'BLUE', 'GREEN', 'CYAN', 'RED', 'MAGENTA', 'BROWN', 'LGRAY',
         'DGRAY', 'LBLUE', 'LGREEN', 'LCYAN', 'LRED', 'LMAGENTA', 'YELLOW',
         'WHITE']
    for row in plan:
        for cell in row:
            if not cell[1] in n:
                cell[1] = 'WHITE'
            if not cell[2] in n:
                cell[2] = 'BLACK'
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


def make_tile(tileset, ord_int=219, fg_c=(0, 0, 0), bg_c=(0, 0, 0)):
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
    # Get the tile
    tile_x, tile_y = tuple(int(n/16) for n in tileset.size)
    x = tile_x * (ord_int % 16)
    y = tile_y * (ord_int // 16)
    tile = tileset.crop((x, y, x + tile_x, y + tile_y)).copy()

    # Add color
    # TODO:  check that this works the same way as DF
    tile.paste(fg_c, None, tile)
    inverted = Image.eval(tile, lambda x: 255-x)
    tile.paste(bg_c, None, inverted)
    return tile.convert('RGB')


def make_image(tileset, plan):
    """Returns an image object of the whole preview."""
    c = get_colors()
    tileset = open_tileset()
    tile_x, tile_y = tuple(int(n/16) for n in tileset.size)
    image_x, image_y = max([len(r) for r in plan]), len(plan)
    preview = Image.new('RGB', (tile_x * image_x, tile_y * image_y),
                        (128, 0, 128))
    for y, row in enumerate(plan):
        for x, cell in enumerate(row):
            char, fg_c, bg_c = cell[0], cell[1], cell[2]
            tile = make_tile(tileset, char, c[fg_c], c[bg_c]).copy()
            box = (x * tile_x, y * tile_y)
            preview.paste(tile, box)
    return preview


class MyWindow(object):
    """Should show off a graphics preview."""
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
        self.preview.create_image(0, 0, anchor='nw', image=self.TK_image)


if __name__ == "__main__":
    root = Tk()
    app = MyWindow(root)
    root.mainloop()
