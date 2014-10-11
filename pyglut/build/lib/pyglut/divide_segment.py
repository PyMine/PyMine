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

def div_segment_into_vertices(vertex1,vertex2,divider) :
  ''' Return an sequence from vertices between vertex1 and vertex2. 
      which has divide the segment (vertex1,vertex2) in the given number of vertices.
  '''

  if not isinstance(vertex1,Vertex) or not isinstance(vertex2,Vertex) :
    raise TypeError(Vertex)
  
  if not isinstance(divider,int) :
    raise TypeError(int)
    
  if divider <= 1 :
    raise ValueError(divider)
  
  # Define a vertice representing the length between vertex1 and vertex2
  length_vertex=Vertex(vertex2.wx-vertex1.wx,vertex2.wy-vertex1.wy,vertex2.wz-vertex1.wz)
  
  divider += 1      # Increment divider to get the right result.
  
  mult=1.0/divider  # Compute the value for step unit setting.  
  
  # Define a step vertice representing a step in the segment division into vertices.
  step_vertex=Vertex(length_vertex.wx*mult,length_vertex.wy*mult,length_vertex.wz*mult)
  
  position=vertex1  # Setting the start position. 
  
  steps_vertices=[]
  
  # Add the initial position to the result:
  steps_vertices.append(position)
  
  for x in range(divider) :
    # Computing next vertice.
    position=Vertex(position.wx+step_vertex.wx,position.wy+step_vertex.wy,position.wz+step_vertex.wz)
    steps_vertices.append(position)
    
  return steps_vertices  # We could return only the vertices between the start and end position: steps_vertices[1:-1]