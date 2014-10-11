"""
pyggel.include
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The include module imports all necessary libraries,
as well as creates a blank, white texture for general use on non-textured objects.
"""

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class MissingModule(Exception):
    pass

try:
    import numpy
except:
    raise MissingModule("Numpy - you can it from: http://sourceforge.net/projects/numpy/files/")

try:
    from OpenGL.GL.EXT.texture_filter_anisotropic import *
    ANI_AVAILABLE = True
except:
    ANI_AVAILABLE = False

try:
    import Image as PIL
    PIL_AVAILABLE = True
except:
    PIL_AVAILABLE = False
    print "Pil not found - animated gif images not supported!"
    print "\tYou can download PIL from: http://www.pythonware.com/products/pil/"

try:
    from OpenGL.GL.EXT.framebuffer_object import *
    FBO_AVAILABLE = True
except:
    FBO_AVAILABLE = False
