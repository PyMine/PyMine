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

class Vector(object) :
  def __init__(self,x=0,y=0,z=0) :
    ''' initialise an object from type Vector representing an vector. '''

    self.x=x
    self.y=y
    self.z=z
    self.length=sqrt(pow(x,2)+pow(y,2)+pow(z,2))

  def from_vertices(self,vertex1,vertex2) :
    ''' Return an Vector representing the vector direction: from vertex1 to vertex2. '''

    if not isinstance(vertex1,Vertex) or not isinstance(vertex2,Vertex) :
      raise TypeError(Vertex)

    self.x=vertex2.wx-vertex1.wx
    self.y=vertex2.wy-vertex1.wy
    self.z=vertex2.wz-vertex1.wz
    self.length=sqrt(pow(self.x,2)+pow(self.y,2)+pow(self.z,2))

    return Vector(self.x,self.y,self.z)

  def get_magnitude(self) :
    ''' Return the length of the vector object. '''

    return sqrt(pow(self.x,2)+pow(self.y,2)+pow(self.z,2))

  def normalize(self) :
    ''' Normalize the current vector object and Return the resulting unit vector. '''

    magnitude = self.get_magnitude()

    self.x=self.x/magnitude
    self.y=self.y/magnitude
    self.z=self.z/magnitude

    return Vector(self.x,self.y,self.z)

  def add_vector(self,vector) :
    ''' return the direction vector from the vector object. '''

    if not isinstance(vector,Vector) :
      raise TypeError(Vector)

    self.x=self.x+vector.x
    self.y=self.y+vector.y
    self.z=self.x+vector.z

    return Vector(self.x,self.y,self.z)

  def sub_vector(self,vector) :
    ''' return the direction vector (opposite direction) from the vector object. '''

    if not isinstance(vector,Vector) :
      raise TypeError(Vector)

    self.x=self.x-vector.x
    self.y=self.y-vector.y
    self.z=self.x-vector.z

    return Vector(self.x,self.y,self.z)

  def mult_vector(self,mult,vector=False) :
    ''' Multiply the vector object or the given vector with the given mult argument what:
	Increment the vector length and if mult is negativ flip the vector direction. '''

    if not isinstance(mult,int) and not isinstance(mult,float) :
      raise TypeError(int,float)
       
    if vector :
    
      if not isinstance(vector,Vector) :
	raise TypeError(Vector)
      
      return Vector(vector.x * mult, vector.y * mult, vector.z * mult) 
      
    else :
      
      self.x=self.x * mult 
      self.y=self.y * mult
      self.z=self.z * mult
      
      return Vector(self.x,self.y,self.z) 
    
  def div_vector(self,div,vector=False) :
    '''Divide the vector object or the given vector by the given div argument what:
       Decrement the vector length and if div is negativ flip the vector direction. '''

    if not isinstance(div,int) and not isinstance(div,float) :
      raise TypeError(int,float)
    
    if vector :
    
      if not isinstance(vector,Vector) :
	raise TypeError(Vector)
      
      return Vector(vector.x / div, vector.y / div, vector.z / div)
      
    else :
      
      self.x=self.x / div 
      self.y=self.y / div
      self.z=self.z / div 
      
      return Vector(self.x,self.y,self.z)  
      
  def negation(self) :
    ''' Invert the direction from the vector object. '''

    self.x= -self.x
    self.y= -self.y
    self.z= -self.z

    return Vector(self.x,self.y,self.z)

  def add_vertex(self,vertex,vector=False) :
    ''' Add the given vertex and vector and return the result as an Vertex object. '''
    if not isinstance(vertex,Vertex) :
      raise TypeError(Vertex)
    
    if vector :
    
      if not isinstance(vector,Vector) :
	raise TypeError(Vector)
      
      return Vertex(vector.x + vertex.wx, vector.y + vertex.wy, vector.z + vertex.wz)  
      
    else :
      
      self.x=self.x + vertex.wx
      self.y=self.y + vertex.wy
      self.z=self.z + vertex.wz
      
      return Vertex(self.x,self.y,self.z)  

  def cross(self,vector1,vector2) :
    ''' Compute the cross product from 2 vectors
	and return the result as an Vector object.
    '''

    if not isinstance(vector1,Vector) or not isinstance(vector2,Vector):
      raise TypeError(Vector)

    x = vector1.y*vector2.z - vector1.z*vector2.y
    y = vector1.z*vector2.x - vector1.x*vector2.z
    z = vector1.x*vector2.y - vector1.y*vector2.x

    return Vector(x,y,z)

  def __add__(self,vector) :
    ''' add sign wrapper for adding an vector to the vector object '''

    if not isinstance(vector,Vector) :
      raise TypeError(Vector)

    return Vector(self.x+vector.x,self.y+vector.y,self.x+vector.z)

  def __sub__(self,vector) :
    ''' substracting sign wrapper for substracting an vector from the vector object  '''

    if not isinstance(vector,Vector) :
      raise TypeError(Vector)

    return Vector(self.x-vector.x,self.y-vector.y,self.x-vector.z)

  def __mul__(self,mult) :
    ''' multiply sign wrapper for incrementing the vector length and
	if mult is negativ flip the vector direction. '''

    if not isinstance(mult,int) and not isinstance(mult,float) :
      raise TypeError(int,float)

    return Vector(self.x*mult,self.y*mult,self.z*mult)

  def __div__(self,div) :
    ''' divide sign wrapper for decrementing the vector length and
	if div is negativ flip the vector direction. '''

    if not isinstance(div,int) and not isinstance(div,float) :
      raise TypeError(int,float)

    return Vector(self.x/div,self.y/div,self.z/div)

  def __neg__(self) :
    ''' Invert the direction from the vector object '''

    return Vector(-self.x,-self.y,-self.z)
  
  def __doc__(self) :
    ''' Print Documentation '''
    print '''
    Vector management class implementing the
    <type 'Vector'> datatype.
    With many vectors operations methods:
    
    -> Creating an vector from 2 vertices: Vector.from_vertices(...)
    -> Getting vector length             : Vector.get_magnitude()
    -> Normalizing an vector             : Vector.normalize()
    -> Adding an vectors                 : Vector.add_vector(vector)
                                         : Vector + vector 
    -> Substracting an vectors           : Vector.sub_vector(vector)
                                         : Vector - vector
    -> Multiply an vectors               : Vector.mult_vector(multiplier,vector)
                                         : Vector * vector 
    -> Dividing an vectors               : Vector.div_vector(divider,vector)
                                         : Vector / vector 
    -> Negate an vector                  : Vector.negation()
                                         : -Vector
    -> Vertex addition                   : Vector.add_vertex(vertex)                                         
    -> Cross product of vectors          : Vector.cross(vector1,vector2)                                
    
    ---------------------------------------------------------------------------
    
    Vectors have many applications in the 3D programmation:
    
    Either for representing an direction from an vertice to another.
    
    Or for simulate an power, like the wind, 
    which have an direction: vector direction.
    And an power           : vector length.
    
    And many others purposes...
    '''