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


from datatype_vertex import Vertex

def get_middle_from_segment(vertex1,vertex2) :
  ''' Return the middle point of an segment as an object from type Vertex '''
  
  if not isinstance(vertex1,Vertex) or not isinstance(vertex2,Vertex) :
    raise TypeError(Vertex)

  return Vertex((vertex1.wx+vertex2.wx)/2.,(vertex1.wy+vertex2.wy)/2.,(vertex1.wz+vertex2.wz)/2.)

def get_center_from_polygon(points) :
  ''' Return the center of an polygon as an object from type Vertex '''
  
  if not isinstance(points,tuple) and not isinstance(points,list) :
    raise TypeError(tuple,list)
  
  for v in points :
    if not isinstance(v,Vertex) :
      raise TypeError(Vertex)
    
  tmp=[]
  i=-1
  while i < len(points)-1 :
    # We compute the inner (inscribe) circle points. To get the right polygone center.
    tmp.append(get_middle_from_segment(points[i],points[i+1]))
    i += 1
  points=tmp  
  
  center=[(max(map(lambda e : e.wx ,points))+min(map(lambda e : e.wx,points)))/2.,(max(map(lambda e : e.wy,points))+min(map(lambda e : e.wy,points)))/2.,(max(map(lambda e : e.wz,points))+min(map(lambda e : e.wz,points)))/2.] 
  
  return Vertex(vertexv=center)

def get_center_from_polyhedron(points) :
  ''' Return the center of an polyhedron as an object from type Vertex '''
  
  if not isinstance(points,tuple) and not isinstance(points,list) :
    raise TypeError(tuple,list)
  
  for v in points :
    if not isinstance(v,Vertex) :
      raise TypeError(Vertex)
  
  center=[(max(map(lambda e : e.wx ,points))+min(map(lambda e : e.wx,points)))/2.,(max(map(lambda e : e.wy,points))+min(map(lambda e : e.wy,points)))/2.,(max(map(lambda e : e.wz,points))+min(map(lambda e : e.wz,points)))/2.] 
  
  return Vertex(vertexv=center)