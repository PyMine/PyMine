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


from OpenGL.GL import glLineWidth, glColor, glBegin, glVertex, glEnd
from OpenGL.GL import GL_LINES

from datatype_vertex import Vertex 
from datatype_vector import Vector
from datatype_matrix import Matrix

class Localview(object) :
  
  def __init__(self,x=0.0,y=0.0,z=0.0) :
    ''' Create an localview object with:
        -) an position represented by an Vertex.
        -) 3 free axes initialise as the X, Y, Z axes.
    '''
    
    self.pos=Vertex(x,y,z)       # Position from the localview. 
    self.right=Vector(1.,0.,0.)  # Axe X representing vector.
    self.up=Vector(0.,1.,0.)     # Axe Y representing vector.
    self.sight=Vector(0.,0.,1.)  # Axe Z representing vector.
    
  def mult_matrix(self,matrix,localview) :
    ''' Multiply the localview with an matrix, given as argument,
        which settings change the localview.
    '''    
    
    if not isinstance(matrix,Matrix) :
      raise TypeError(Matrix)
    
    if not isinstance(localview,Localview) :
      raise TypeError(Localview)
    
    localview.pos=matrix.mult_vertex(localview.pos)      # Multiply the matrix with the position Vertex.
    localview.up=matrix.mult_vector(localview.up)        # Multiply the matrix with the X axe representing vector.
    localview.right=matrix.mult_vector(localview.right)  # Multiply the matrix with the Y axe representing vector.
    localview.sight=matrix.mult_vector(localview.sight)  # Multiply the matrix with the Z axe representing vector.
    
    return localview
  
  def __mul__(self,matrix) :
    ''' Localview and Localview multiplication sign '*' wrapper. 
        Multiplying the current localview with the right operator Matrix object.
    ''' 
    
    if not isinstance(matrix,Matrix) :
      raise TypeError(Matrix)
    
    self.pos=matrix.mult_vertex(self.pos)      # Multiply the matrix with the position Vertex.
    self.up=matrix.mult_vector(self.up)        # Multiply the matrix with the X axe representing vector.
    self.right=matrix.mult_vector(self.right)  # Multiply the matrix with the Y axe representing vector.
    self.sight=matrix.mult_vector(self.sight)  # Multiply the matrix with the Z axe representing vector.
    
    return self
  
  def display(self,factor) :
    ''' Function to display the localview axes. '''
    
    right_arrow = self.right.add_vertex(self.pos,self.right.mult_vector(factor,self.right))
    up_arrow = self.up.add_vertex(self.pos,self.up.mult_vector(factor,self.up))
    sight_arrow = self.sight.add_vertex(self.pos,self.sight.mult_vector(factor,self.sight))
    
    glLineWidth(4)
    
    glColor(255,0,0)
    glBegin(GL_LINES)
    glVertex(self.pos.get_vertex())
    glVertex(right_arrow.get_vertex())
    glEnd()
    
    glColor(0,255,0)
    glBegin(GL_LINES)
    glVertex(self.pos.get_vertex())
    glVertex(up_arrow.get_vertex())
    glEnd()
    
    glColor(0,0,255)
    glBegin(GL_LINES)
    glVertex(self.pos.get_vertex())
    glVertex(sight_arrow.get_vertex())
    glEnd()
    
  def __doc__(self) :
    ''' print documentation '''
    print '''
    Localview management class implementing an
    <type 'Localview'> datatype.
    
    An localview is an object representing either an 
    -> Camera view.
    -> Local axes (X, Y, Z) of an 3D object.
    
    An locaview is made from:
    -> An localview position vertex, object from <type 'Vertex'>.
	which is the position from:
	-> The camera.
	-> The center from the 3D object.
	referenced as an attribute named: Localview.pos
	
      -> 3 axes, objects from <type 'Vector'>. Representing either:
	-> The camera orientation.
	-> The own axes from the 3D object.
	
    The Localview class implement:
      
    -) multiplication with an matrix methods:
      
    either as the method: 
    -> Localview.mult_matrix(matrix)
	  which take an matrix containing the changing to apply
	  to the localview.
    -> an multiply sign placeholder:
	  The matrix to multiply with must be at the right to
	  the localview:
	  
	    Localview * Matrix 
      
    -) An Locaview display method for debugging purpose.
          Which display the axes in their current orientation
	  from the center to the greater values from the axes.
	  At the current Localview position.
          '''      
              