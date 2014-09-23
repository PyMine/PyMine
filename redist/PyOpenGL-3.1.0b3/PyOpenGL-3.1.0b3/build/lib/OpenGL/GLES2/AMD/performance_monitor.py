'''OpenGL extension AMD.performance_monitor

This module customises the behaviour of the 
OpenGL.raw.GLES2.AMD.performance_monitor to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/AMD/performance_monitor.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.AMD.performance_monitor import *
from OpenGL.raw.GLES2.AMD.performance_monitor import _EXTENSION_NAME

def glInitPerformanceMonitorAMD():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glGetPerfMonitorGroupsAMD=wrapper.wrapper(glGetPerfMonitorGroupsAMD).setOutput(
    'numGroups',size=(1,),orPassIn=True
).setOutput(
    'groups',size=lambda x:(x,),pnameArg='groupsSize',orPassIn=True
)
glGetPerfMonitorCountersAMD=wrapper.wrapper(glGetPerfMonitorCountersAMD).setOutput(
    'numCounters',size=(1,),orPassIn=True
).setOutput(
    'maxActiveCounters',size=(1,),orPassIn=True
).setOutput(
    'counters',size=lambda x:(x,),pnameArg='counterSize',orPassIn=True
)
glGetPerfMonitorGroupStringAMD=wrapper.wrapper(glGetPerfMonitorGroupStringAMD).setOutput(
    'groupString',size=lambda x:(x,),pnameArg='bufSize',orPassIn=True
).setOutput(
    'length',size=(1,),orPassIn=True
)
glGetPerfMonitorCounterStringAMD=wrapper.wrapper(glGetPerfMonitorCounterStringAMD).setOutput(
    'length',size=(1,),orPassIn=True
).setOutput(
    'counterString',size=lambda x:(x,),pnameArg='bufSize',orPassIn=True
)
glGetPerfMonitorCounterInfoAMD=wrapper.wrapper(glGetPerfMonitorCounterInfoAMD).setOutput(
    'data',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGenPerfMonitorsAMD=wrapper.wrapper(glGenPerfMonitorsAMD).setOutput(
    'monitors',size=lambda x:(x,),pnameArg='n',orPassIn=True
)
glDeletePerfMonitorsAMD=wrapper.wrapper(glDeletePerfMonitorsAMD).setOutput(
    'monitors',size=lambda x:(x,),pnameArg='n',orPassIn=True
)
glSelectPerfMonitorCountersAMD=wrapper.wrapper(glSelectPerfMonitorCountersAMD).setOutput(
    'counterList',size=lambda x:(x,),pnameArg='numCounters',orPassIn=True
)
glGetPerfMonitorCounterDataAMD=wrapper.wrapper(glGetPerfMonitorCounterDataAMD).setOutput(
    'data',size=lambda x:(x,),pnameArg='dataSize',orPassIn=True
).setOutput(
    'bytesWritten',size=(1,),orPassIn=True
)
### END AUTOGENERATED SECTION