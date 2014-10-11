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


from math import cos,sin,radians,sqrt

from datatype_vertex import Vertex

def rotate_on_xy(center,angle,vertex) :
  ''' Function to rotate an vertex given as the argument vertex 
      around a center vertex in the xy plan from the value angle in clock sens.
      Return the rotated vertex as an object from <type 'Vertex'>.
  '''
  
  if not isinstance(center,Vertex) :
    raise TypeError(Vertex)
  
  if not isinstance(vertex,Vertex) :
    raise TypeError(Vertex)
  
  return_x= vertex.wx * cos(radians(angle)) - vertex.wy * sin(radians(angle)) + center.wx*(1-cos(radians(angle))) + center.wy * sin(radians(angle))
  return_y= vertex.wx * sin(radians(angle)) + vertex.wy * cos(radians(angle)) + center.wy*(1-cos(radians(angle))) - center.wx * sin(radians(angle))
  
  return Vertex(return_x,return_y,0.)

def rotate_on_xz(center,angle,vertex) :
  ''' Function to rotate an vertex given as the argument vertex
      around a center vertex in the xz plan from the value angle in clock sens.
      Return the rotated vertex as an object from <type 'Vertex'>.
  '''
  if not isinstance(center,Vertex) :
    raise TypeError(Vertex)
  
  if not isinstance(vertex,Vertex) :
    raise TypeError(Vertex)
  
  return_x= vertex.wx * cos(radians(angle)) - vertex.wz * sin(radians(angle)) + center.wx*(1-cos(radians(angle))) + center.wz * sin(radians(angle))
  return_z= vertex.wx * sin(radians(angle)) + vertex.wz * cos(radians(angle)) + center.wz*(1-cos(radians(angle))) - center.wx * sin(radians(angle))
  
  return Vertex(return_x,0.,return_z)

def rotate_on_yz(center,angle,vertex) :
  ''' Function to rotate an vertex given as the argument vertex 
      around a center vertex in the yz plan from the value angle in clock sens.
      Return the rotated vertex as an object from <type 'Vertex'>.
  '''
  
  if not isinstance(center,Vertex) :
    raise TypeError(Vertex)
  
  if not isinstance(vertex,Vertex) :
    raise TypeError(Vertex)
  
  return_y= vertex.wy * cos(radians(angle)) - vertex.wz * sin(radians(angle)) + center.wy*(1-cos(radians(angle))) + center.wz * sin(radians(angle))
  return_z= vertex.wy * sin(radians(angle)) + vertex.wz * cos(radians(angle)) + center.wz*(1-cos(radians(angle))) - center.wy * sin(radians(angle))
  
  return Vertex(0.,return_y,return_z)