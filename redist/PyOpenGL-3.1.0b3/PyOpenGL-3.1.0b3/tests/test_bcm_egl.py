#! /usr/bin/env python
import ctypes, ctypes.util
bcm = ctypes.CDLL( ctypes.util.find_library( 'bcm_host' ) )
class NativeWindow( ctypes.Structure ):
    _fields_ = [
        ('element',ctypes.c_void_p),
        ('width', ctypes.c_uint32),
        ('height', ctypes.c_uint32),
    ]
    def __init__( self, element, width, height ):
        self.element = element 
        self.width = width 
        self.height = height
class Rect( ctypes.Structure ):
    _fields_ = [
        ('x',ctypes.c_int32),
        ('y',ctypes.c_int32),
        ('width',ctypes.c_int32),
        ('height',ctypes.c_int32),
    ]

bcm.bcm_host_init()
bcm.graphics_get_display_size.argtypes=[ ctypes.c_uint16, ctypes.c_uint32, ctypes.c_uint32 ]
bcm.vc_dispmanx_display_open.restype = ctypes.c_void_p
bcm.vc_dispmanx_update_start.restype = ctypes.c_void_p
bcm.vc_dispmanx_element_add.argtypes = [ 
    ctypes.c_void_p, ctypes.c_void_p, 
    ctypes.c_int32, # layer
    ctypes.POINTER(Rect),# destination
    ctypes.c_void_p, # resource
    ctypes.POINTER(Rect),# source
    ctypes.c_void_p, # protection
    ctypes.c_void_p, # alpha
    ctypes.c_void_p, # clamp
    ctypes.c_void_p, # transform
]
bcm.vc_dispmanx_element_add.restype = ctypes.c_void_p

def open_display( device ):
    return bcm.vc_dispmanx_display_open( device )
def update_start( priority ):
    return bcm.vc_dispmanx_update_start( priority )

def graphics_get_display_size( display_number=0 ):
    width,height = ctypes.c_uint32(),ctypes.c_uint32()
    bcm.graphics_get_display_size( display_number, ctypes.addressof(width), ctypes.addressof(height) )
    return width.value,height.value

def create_window(width=None, height=None):
    if width is None or height is None:
        W,H = graphics_get_display_size()
    else:
        W,H = width,height
    dst = Rect(0,0,W,H)
    src = Rect(0,0,W<<16,H<<16) # why?
    display = open_display(0)
    update = update_start(0)
    element = bcm.vc_dispmanx_element_add(
        update, display, 
        0, 
        dst, 
        ctypes.c_void_p(0),
        src,
        ctypes.c_void_p(0),
        ctypes.c_void_p(0),
        ctypes.c_void_p(0),
        ctypes.c_void_p(0),
    )
    win = NativeWindow(element, W, H)
    bcm.vc_dispmanx_update_submit_sync(update)
    return win

if __name__ == "__main__":
    print create_window()
