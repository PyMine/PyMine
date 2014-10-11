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


from math import sqrt

from datatype_vertex import Vertex

def get_distance_vertices(vertex1,vertex2) :
  ''' Return the distance between 2 vertices: vertex1 and vertex2. '''

  if not isinstance(vertex1,Vertex) or not isinstance(vertex2,Vertex) :
    raise TypeError(Vertex)

  return sqrt(pow(vertex1.wx-vertex2.wx,2)+pow(vertex1.wy-vertex2.wy,2)+pow(vertex1.wz-vertex2.wz,2))
    
def get_perimeter_from_polygon(points) :
  ''' return the length of the perimeter of the polygon which vertex sequence is given as argument. '''
  
  if not isinstance(points,tuple) and not isinstance(points,list) :
      raise TypeError(tuple,list)
    
  for v in points :
    if not isinstance(v,Vertex) :
      raise TypeError(Vertex)
  
  perimeter=0.0  # Perimeter value container variable.
  
  i=-1           # Initialisation of the iterator variable so that 
		 # we can access it, added from one, for the points list indexing.
		  
  while i < len(points)-1 :
    # Loop on every segment from the polygon.
    
    # We increment the variable perimeter with the returning from the function computing 
    # the distance beetween 2 vertices.
    perimeter += get_distance_vertices(points[i],points[i+1])
    
    i += 1       # Iterator variable incrementation.
    
  return perimeter 

def get_perimeter_from_polyhedron(points) :
  ''' Return the length of the perimeter from the polyhedron which polygon sequence is given as argument. '''
  
  if not isinstance(points,tuple) and not isinstance(points,list) :
      raise TypeError(tuple,list)
    
  for v in points :
    if not isinstance(v,tuple) and not isinstance(v,list) :
      raise TypeError(tuple,list)
    
    for y in v :
      if not isinstance(y,Vertex) :
	raise TypeError(Vertex)
      
  list_checked=[]  # Container for already computed sides from the polyhedron.
  
  perimeter=0.0    # Perimeter value container variable.
  
  for v in points :
    # We iterate on every polygon from the polyhedron.
    
    i=-1      # Initialisation of the iterator variable so that 
	      # we can access it, added from one, for the points list indexing.
	  
    while i < len(v)-1 :
      # Iteration on the vertex from an polygon composing the polyhedron.
      
      if not (v[i],v[i+1]) in list_checked and not (v[i+1],v[i]) in list_checked :
	# Side not already computed.
	
	# We increment the variable perimeter with the returning from the function computing 
	# the distance beetween 2 vertices.
	perimeter += get_distance_vertices(v[i],v[i+1])
	
	# We append this polyhedron side to the already computed side list.
	list_checked.append((v[i],v[i+1]))
      
      i += 1  # Iterator variable incrementation.
    
  return perimeter     