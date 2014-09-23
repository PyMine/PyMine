'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_blend_func_separate'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_blend_func_separate',error_checker=_errors._error_checker)
GL_BLEND_DST_ALPHA_EXT=_C('GL_BLEND_DST_ALPHA_EXT',0x80CA)
GL_BLEND_DST_RGB_EXT=_C('GL_BLEND_DST_RGB_EXT',0x80C8)
GL_BLEND_SRC_ALPHA_EXT=_C('GL_BLEND_SRC_ALPHA_EXT',0x80CB)
GL_BLEND_SRC_RGB_EXT=_C('GL_BLEND_SRC_RGB_EXT',0x80C9)
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLenum,_cs.GLenum)
def glBlendFuncSeparateEXT(sfactorRGB,dfactorRGB,sfactorAlpha,dfactorAlpha):pass
