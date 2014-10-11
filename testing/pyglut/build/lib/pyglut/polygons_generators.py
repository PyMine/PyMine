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

from primary_operations import translate, rotate_x, rotate_y, rotate_z

from rotation_utils import *
from center_utils import get_center_from_polygon 

def generate_polygon_on_xy_radius(edges,radius,center,offset=0) :
  ''' Return an polygon on plan XY: from edges sides, from radius radius, with offset offset.
    
            y 
            | 
        ____|____x
            |
            |              plan XY.
   '''

  if not isinstance(center,Vertex) :
    raise TypeError(Vertex)

  polygon=[]        # Polygon vertice container.
  scale=360./edges  # Computing of the angle separating 2 points from the polygon.
  i=0
  while i < edges :
  
    polygon.append(Vertex((radius*cos(radians((scale*i)+offset)))+center.wx,(radius*sin(radians((scale*i)+offset)))+center.wy,center.wz))
  
    i += 1
  
  return polygon

def generate_polygon_on_yz_radius(edges,radius,center,offset=0) :
  ''' Return an polygon on plan YZ: from edges sides, from radius radius, with offset offset.
        
            y  z
            | /
            |/
           /|
          / |              plan YZ. 
  '''
  
  if not isinstance(center,Vertex) :
    raise TypeError(Vertex)
  
  polygon=[]        # Polygon vertice container.
  scale=360./edges  # Computing of the angle separating 2 points from the polygon.
  i=0
  while i < edges :
    polygon.append(Vertex(center.wx,(radius*cos(radians((scale*i)+offset)))+center.wy,(radius*sin(radians((scale*i)+offset)))+center.wz))
  
    i += 1

  return polygon  

def generate_polygon_on_xz_radius(edges,radius,center,offset=0) :
  ''' Return an polygon on plan XZ: from edges sides, from radius radius, with offset offset.
              
             z
            /
      _____/____x
          /
         /                 plan XZ.
  '''
  
  if not isinstance(center,Vertex) :
    raise TypeError(Vertex)
      
  polygon=[]        # Polygon vertice container.
  scale=360./edges  # Computing of the angle separating 2 points from the polygon.
  i=0
  while i < edges :
    polygon.append(Vertex(radius*cos(radians((scale*i)+offset))+center.wx,center.wy,radius*sin(radians((scale*i)+offset))+center.wz))
  
    i += 1
  
  return polygon      
      
      
def generate_polygon_on_xy_side_length(edges,side_length,offset=0) :
  ''' Return an polygon on plan XY: with edges edges from length side_length, with offset offset.
    
            y 
            | 
        ____|____x
            |
            |              plan XY.
  '''

  angle=360.0/side_length
  
  polygon=[]         # Polygon vertice container.
  scale=360.0/edges  # Computing of the angle separating 2 points from the polygon.
  
  start_vertex1=Vertex(-side_length/2.,0.0,0.0)
  start_vertex2=Vertex(side_length/2.,0.0,0.0)
    
  point_to_rotate=start_vertex1
  rotate_point=start_vertex2
  
  polygon.append(point_to_rotate)
  polygon.append(rotate_point)
  
  i=2
  while i < edges :
  
    vertex=rotate_on_xy(rotate_point,abs(180-scale),point_to_rotate)
    
    point_to_rotate=rotate_point
    rotate_point=vertex
    
    polygon.append(vertex)
    
    i += 1
  
  
  center=get_center_from_polygon(polygon) # Compute polygon center.
  
  tmp=[]
  for v in polygon :
    # Translate polygon vertices so as his center is the display center.
    tmp.append(translate(v,-center.wx,-center.wy,-center.wz))
  
  if offset :
    offset_set=[]
    for v in tmp :
      offset_set.append(rotate_z(v,offset))
    
    tmp=offset_set  
  
  polygon=tmp
  return polygon     
  
def generate_polygon_on_xz_side_length(edges,side_length,offset=0) :
  ''' Return an polygon on plan XZ: with edges edges from length side_length, with offset offset. 
              
             z
            /
      _____/____x
          /
         /                 plan XZ.
   '''

  angle=360.0/side_length
  
  polygon=[]         # Polygon vertice container.
  scale=360.0/edges  # Computing of the angle separating 2 points from the polygon.
  
  start_vertex1=Vertex(-side_length/2.,0.0,0)
  start_vertex2=Vertex(side_length/2.,0.0,0)
    
  point_to_rotate=start_vertex1
  rotate_point=start_vertex2
  
  polygon.append(point_to_rotate)
  polygon.append(rotate_point)
  
  i=2
  while i < edges :
  
    vertex=rotate_on_xz(rotate_point,abs(180-scale),point_to_rotate)
    
    point_to_rotate=rotate_point
    rotate_point=vertex
    
    polygon.append(vertex)
    
    i += 1
  
  center=get_center_from_polygon(polygon) # Compute polygon center.
  
  tmp=[]
  for v in polygon :
    # Translate polygon vertices so as his center is the display center.
    tmp.append(translate(v,-center.wx,-center.wy,-center.wz))
  
  
  if offset :
    offset_set=[]
    for v in tmp :
      offset_set.append(rotate_y(v,offset))
    
    tmp=offset_set  
  
  polygon=tmp
  return polygon     
  
def generate_polygon_on_yz_side_length(edges,side_length,offset=0) :
  ''' Return an polygon on plan YZ: with edges edges from length side_length, with offset offset.
        
            y  z
            | /
            |/
           /|
          / |             plan YZ. 
  '''

  angle=360.0/side_length
  
  polygon=[]         # Polygon vertice container.
  scale=360.0/edges  # Computing of the angle separating 2 points from the polygon.
  
  start_vertex1=Vertex(0.0,-side_length/2.,0)
  start_vertex2=Vertex(0.0,side_length/2.,0)
    
  point_to_rotate=start_vertex1
  rotate_point=start_vertex2
  
  polygon.append(point_to_rotate)
  polygon.append(rotate_point)
  
  i=2
  while i < edges :
  
    vertex=rotate_on_yz(rotate_point,abs(180-scale),point_to_rotate)
    
    point_to_rotate=rotate_point
    rotate_point=vertex
    
    polygon.append(vertex)
    
    i += 1
  
  center=get_center_from_polygon(polygon) # Compute polygon center.
  
  tmp=[]
  for v in polygon :
    # Translate polygon vertices so as his center is the display center.
    tmp.append(translate(v,-center.wx,-center.wy,-center.wz))
  
  if offset :
    offset_set=[]
    for v in tmp :
      offset_set.append(rotate_x(v,offset))
    tmp=offset_set  
  
  polygon=tmp
  return polygon         