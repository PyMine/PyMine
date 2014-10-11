#!/usr/bin/python
# -*- coding: utf-8 -*-    

#####################################################################################
#                                                                                   #       
# pyglut an pyopengl utilities module with severals 3D programming                  #
# helper class and functions.                                                       #
# Copyright (C) 2014 Brüggemann Eddie alias mrcyberfighter.                         #
#                                                                                   #
# This file is part of the pyglut module.                                           #
# pyglut is free software: you can redistribute it and/or modify                    #
# it under the terms of the GNU General Public License as published by              #
# the Free Software Foundation, either version 3 of the License, or                 #
# (at your option) any later version.                                               #
#                                                                                   #
# pyglut is distributed in the hope that it will be useful,                         #  
# but WITHOUT ANY WARRANTY; without even the implied warranty of                    # 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                      #
# GNU General Public License for more details.                                      #
#                                                                                   #
# You should have received a copy of the GNU General Public License                 #
# along with pyglut. If not, see <http://www.gnu.org/licenses/>                     #
#                                                                                   #
#####################################################################################

from math import cos,sin,radians

from datatype_vertex import Vertex

def translate(vertex,value_x,value_y,value_z) :
  ''' Translate an vertice from the given offset in every axe. '''
  
  if not isinstance(vertex,Vertex) :
    # Type control.
    raise TypeError(Vertex)
      
  x=(value_x+vertex.wx)  # We simply add the given value to translate vertex in direction x, even if it is an negativ value it work.  
  y=(value_y+vertex.wy)  # We simply add the given value to translate vertex in direction y, even if it is an negativ value it work.
  z=(value_z+vertex.wz)  # We simply add the given value to translate vertex in direction z, even if it is an negativ value it work.

  return Vertex(x,y,z)
    

def scale(vertex,factor) :
  ''' Scale from the given factor. '''
  if not isinstance(vertex,Vertex) :
    # Type control.
    raise TypeError(Vertex)
  
  # We simply multiply every vertex component (wx,wy,wz) with the given scaling factor.
    
  return Vertex(vertex.wx*factor,vertex.wy*factor,vertex.wz*factor)

def rotate_x(vertex,angle) :
  ''' Rotate an vertice around the x axe and return the result position vertice. '''
  
  if not isinstance(vertex,Vertex) :
    # Type control.
    raise TypeError(Vertex)
    
  x=vertex.wx # Because we rotate on the x axe the x value don't change.
  y=(cos(radians(angle))*vertex.wy)-(sin(radians(angle))*vertex.wz)  # Sea explications.
  z=(sin(radians(angle))*vertex.wy)+(cos(radians(angle))*vertex.wz)  # Sea explications.


  return Vertex(x,y,z) 
  
def rotate_y(vertex,angle) :
  ''' Rotate an vertice around the y axe and return the result position vertice. '''
  
  if not isinstance(vertex,Vertex) :
    # Type control.
    raise TypeError(Vertex)
  
  x=cos(radians(angle))*vertex.wx-sin(radians(angle))*vertex.wz # Sea explications.
  y=vertex.wy # Because we rotate on the y axe the y value don't change.
  z=sin(radians(angle))*vertex.wx+cos(radians(angle))*vertex.wz # Sea explications.
  
  return Vertex(x,y,z)  
  
def rotate_z(vertex,angle) :
  ''' Rotate an vertice around the z axe and return the result position vertice. '''
  
  if not isinstance(vertex,Vertex) :
    # Type control.
    raise TypeError(Vertex)

  x=cos(radians(angle))*vertex.wx-sin(radians(angle))*vertex.wy # Sea explications.
  y=sin(radians(angle))*vertex.wx+cos(radians(angle))*vertex.wy # Sea explications.
  z=vertex.wz # Because we rotate on the z axe the z value don't change.

  return Vertex(x,y,z)  
    