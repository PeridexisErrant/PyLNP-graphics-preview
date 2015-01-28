#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing a graphics preview canvas."""
from __future__ import print_function, unicode_literals, absolute_import

import sys

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



def image_plan():
    """Return a plan to display with the selected graphics pack.

    Format:
        A list of rows, each of which is a list of tuples (char, color_name)
    """
    # placeholder - make bigger and configurable
    return [[('WALL', 'BLUE')]]

    return [[('WALL_EW', ''), ('WALL_SW', ''), ('TABLE', '')],
            [('WALL', ''), ('PILLAR', ''), ('CHAIR', '')],
            [('FLOOR', ''), ('DOOR', ''), ('FLOOR', '')]]

def return_color(name):
    """Returns the color tuple of a particular name."""
    # Will be implemented by PyLNP, so do later
    return (46, 88, 255)

def find_tile(name, image, raws):
    """Finds the specified tile within an image

    Returns:
        The location of the tile, in the format used by DF raws
    """
    pass


class MyWindow(object):
    """Should show off a graphics preview."""
    # tester class, to work on methods
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Graphics Preview")
        self.frame = Frame(parent)
        self.draw_preview()
        self.graphics_preview.pack()
        self.frame.pack()

    def draw_preview(self):
        """Draws the canvas and image"""
        self.graphics_preview = Canvas(
            width=160, height=160, highlightthickness=0,
            takefocus=False)
        self.graphics_preview.create_rectangle((0, 0, 160, 160), fill='blue')



if __name__ == "__main__":
    root = Tk()
    app = MyWindow(root)
    root.mainloop()
