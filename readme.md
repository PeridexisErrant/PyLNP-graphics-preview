Testing Graphics Previewing
---------------------------

A minor project to add a graphics pack preview to the PyLNP.

It should take a scene, tileset, colorscheme (and later graphics raws), and
display an image equivalent to a screenshot with the selected settings. This
should be useful to choose - and combine - whole graphics packs, and also
preview customisations thereof.

The 'scene' will be an array (probably a list of lists of (item, color) tuples.
Items will be given as a CP437-character, or numeric ID.  Colors will be
identified by the string used by DF.

I'm working on the basis that PIL is available:  all the image processing will
be done with PIL, and then saved to a (temporary) .gif for use in tkinter.  
A tkinter-only version is impossible anyway, since it has very poor .png
support.

Very much a work in progress, since I'm learning as I go.
