'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES1 import _types as _cs
# End users want this...
from OpenGL.raw.GLES1._types import *
from OpenGL.raw.GLES1 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES1_OES_texture_cube_map'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES1,'GLES1_OES_texture_cube_map',error_checker=_errors._error_checker)
GL_MAX_CUBE_MAP_TEXTURE_SIZE_OES=_C('GL_MAX_CUBE_MAP_TEXTURE_SIZE_OES',0x851C)
GL_NORMAL_MAP_OES=_C('GL_NORMAL_MAP_OES',0x8511)
GL_REFLECTION_MAP_OES=_C('GL_REFLECTION_MAP_OES',0x8512)
GL_TEXTURE_BINDING_CUBE_MAP_OES=_C('GL_TEXTURE_BINDING_CUBE_MAP_OES',0x8514)
GL_TEXTURE_CUBE_MAP_NEGATIVE_X_OES=_C('GL_TEXTURE_CUBE_MAP_NEGATIVE_X_OES',0x8516)
GL_TEXTURE_CUBE_MAP_NEGATIVE_Y_OES=_C('GL_TEXTURE_CUBE_MAP_NEGATIVE_Y_OES',0x8518)
GL_TEXTURE_CUBE_MAP_NEGATIVE_Z_OES=_C('GL_TEXTURE_CUBE_MAP_NEGATIVE_Z_OES',0x851A)
GL_TEXTURE_CUBE_MAP_OES=_C('GL_TEXTURE_CUBE_MAP_OES',0x8513)
GL_TEXTURE_CUBE_MAP_POSITIVE_X_OES=_C('GL_TEXTURE_CUBE_MAP_POSITIVE_X_OES',0x8515)
GL_TEXTURE_CUBE_MAP_POSITIVE_Y_OES=_C('GL_TEXTURE_CUBE_MAP_POSITIVE_Y_OES',0x8517)
GL_TEXTURE_CUBE_MAP_POSITIVE_Z_OES=_C('GL_TEXTURE_CUBE_MAP_POSITIVE_Z_OES',0x8519)
GL_TEXTURE_GEN_MODE_OES=_C('GL_TEXTURE_GEN_MODE_OES',0x2500)
GL_TEXTURE_GEN_STR_OES=_C('GL_TEXTURE_GEN_STR_OES',0x8D60)
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,arrays.GLfloatArray)
def glGetTexGenfvOES(coord,pname,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,arrays.GLintArray)
def glGetTexGenivOES(coord,pname,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,ctypes.POINTER(_cs.GLfixed))
def glGetTexGenxvOES(coord,pname,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLfloat)
def glTexGenfOES(coord,pname,param):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,arrays.GLfloatArray)
def glTexGenfvOES(coord,pname,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLint)
def glTexGeniOES(coord,pname,param):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,arrays.GLintArray)
def glTexGenivOES(coord,pname,params):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,_cs.GLfixed)
def glTexGenxOES(coord,pname,param):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLenum,ctypes.POINTER(_cs.GLfixed))
def glTexGenxvOES(coord,pname,params):pass
