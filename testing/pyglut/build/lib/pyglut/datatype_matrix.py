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

from OpenGL.GL import glLineWidth, glColor, glBegin, glVertex, glEnd, glMatrixMode, glLoadMatrixd, glMultMatrixd, glGetFloatv
from OpenGL.GL import GL_LINES, GL_MODELVIEW, GL_MODELVIEW_MATRIX

from datatype_vertex import Vertex 
from datatype_vector import Vector

class Localview(object) :
  # This class is redefine here because we cannot import it because it cause import crossing errors:
  # The Localview class depends from the Matrix class and
  # The Matrix class depends from the Localview class !!!
  
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

class Matrix(object) :
  def __init__(self,vertex=False) :
    ''' Create an matrix object to process move, scaling, matrix, vectors, localviews and vertex operations. '''
    
    if vertex :
      
      if not isinstance(vertex,Vertex) :
        raise TypeError(Vertex)
      
      self.x=vertex.wx
      self.y=vertex.wy
      self.z=vertex.wz
    
    else :
      
      self.x=1.0
      self.y=1.0
      self.z=1.0
    
    # Create the main matrix.
    self.main_matrix=range(0,16)
    self.main_matrix[0]=self.x ; self.main_matrix[4]=0      ; self.main_matrix[8]=0       ; self.main_matrix[12]=0 ;
    self.main_matrix[1]=0      ; self.main_matrix[5]=self.y ; self.main_matrix[9]=0       ; self.main_matrix[13]=0 ;
    self.main_matrix[2]=0      ; self.main_matrix[6]=0      ; self.main_matrix[10]=self.z ; self.main_matrix[14]=0 ;
    self.main_matrix[3]=0      ; self.main_matrix[7]=0      ; self.main_matrix[11]=0      ; self.main_matrix[15]=1 ;
    
    
    self._processing_matrix=range(0,16) # Generate an array used as processing matrix.                  
    
  
  def translate(self,vector) :
    ''' Apply an translation move. ''' 
    
    if not isinstance(vector,tuple) and not isinstance(vector,list) and not isinstance(vector,Vector) :
      raise TypeError(tuple,list,Vector)
    
    if isinstance(vector,tuple) or isinstance(vector,list) :
      # Initialise the processing matrix with the translation vector. 
      self._processing_matrix[0]=1 ; self._processing_matrix[4]=0 ; self._processing_matrix[8]=0  ; self._processing_matrix[12]=vector[0]  ;
      self._processing_matrix[1]=0 ; self._processing_matrix[5]=1 ; self._processing_matrix[9]=0  ; self._processing_matrix[13]=vector[1]  ;
      self._processing_matrix[2]=0 ; self._processing_matrix[6]=0 ; self._processing_matrix[10]=1 ; self._processing_matrix[14]=vector[2]  ;
      self._processing_matrix[3]=0 ; self._processing_matrix[7]=0 ; self._processing_matrix[11]=0 ; self._processing_matrix[15]=1          ;
   
    elif isinstance(vector,Vector) :
      # Initialise the processing matrix with the translation vector. 
      self._processing_matrix[0]=1 ; self._processing_matrix[4]=0 ; self._processing_matrix[8]=0  ; self._processing_matrix[12]=vector.x  ;
      self._processing_matrix[1]=0 ; self._processing_matrix[5]=1 ; self._processing_matrix[9]=0  ; self._processing_matrix[13]=vector.y  ;
      self._processing_matrix[2]=0 ; self._processing_matrix[6]=0 ; self._processing_matrix[10]=1 ; self._processing_matrix[14]=vector.z  ;
      self._processing_matrix[3]=0 ; self._processing_matrix[7]=0 ; self._processing_matrix[11]=0 ; self._processing_matrix[15]=1          ;
    
    # Multiply the processing matrix with the main matrix.
    # To apply the translation to it. 
    self._multiply()
    
  def scale(self,factor) :
    ''' Apply an scaling operation. '''
    
    if not isinstance(factor,int) and not isinstance(factor,float) :
      raise TypeError(int,float)
    
    # Initialise the processing matrix with the scaling factor. 
    self._processing_matrix[0]=factor ; self._processing_matrix[4]=0      ; self._processing_matrix[8]=0       ; self._processing_matrix[12]=0 ;
    self._processing_matrix[1]=0      ; self._processing_matrix[5]=factor ; self._processing_matrix[9]=0       ; self._processing_matrix[13]=0 ;
    self._processing_matrix[2]=0      ; self._processing_matrix[6]=0      ; self._processing_matrix[10]=factor ; self._processing_matrix[14]=0 ;
    self._processing_matrix[3]=0      ; self._processing_matrix[7]=0      ; self._processing_matrix[11]=0      ; self._processing_matrix[15]=1 ;
    
    # Multiply the processing matrix with the main matrix.
    # To apply the scaling to it. 
    self._multiply()
    
  def rotate_x(self,degrees) :
    ''' Rotation around the X axe from the given angle in degrees. '''
    
    if not isinstance(degrees,int) and not isinstance(degrees,float) :
      raise TypeError(int,float)
    
    c=cos(radians(degrees))  # Compute the cosine from the given angle.
    s=sin(radians(degrees))  # Compute the sine from the given angle.
    
    # Initialise the processing matrix with the cosine and sine from the given angle. 
    self._processing_matrix[0]=1 ; self._processing_matrix[4]=0 ; self._processing_matrix[8]=0  ; self._processing_matrix[12]=0 ;
    self._processing_matrix[1]=0 ; self._processing_matrix[5]=c ; self._processing_matrix[9]=-s ; self._processing_matrix[13]=0 ;
    self._processing_matrix[2]=0 ; self._processing_matrix[6]=s ; self._processing_matrix[10]=c ; self._processing_matrix[14]=0 ;
    self._processing_matrix[3]=0 ; self._processing_matrix[7]=0 ; self._processing_matrix[11]=0 ; self._processing_matrix[15]=1 ;
    
    # Multiply the processing matrix with the main matrix.
    # To apply the rotation to it. 
    self._multiply()
  
  def rotate_y(self,degrees) :
    ''' Rotation around the Y axe from the given angle in degrees. '''
    
    if not isinstance(degrees,int) and not isinstance(degrees,float) :
      raise TypeError(int,float)
    
    c=cos(radians(degrees))  # Compute the cosine from the given angle.
    s=sin(radians(degrees))  # Compute the sine from the given angle.
    
    # Initialise the processing matrix with the cosine and sine from the given angle. 
    self._processing_matrix[0]=c  ; self._processing_matrix[4]=0 ; self._processing_matrix[8]=s  ; self._processing_matrix[12]=0 ;
    self._processing_matrix[1]=0  ; self._processing_matrix[5]=1 ; self._processing_matrix[9]=0  ; self._processing_matrix[13]=0 ;
    self._processing_matrix[2]=-s ; self._processing_matrix[6]=0 ; self._processing_matrix[10]=c ; self._processing_matrix[14]=0 ;
    self._processing_matrix[3]=0  ; self._processing_matrix[7]=0 ; self._processing_matrix[11]=0 ; self._processing_matrix[15]=1 ;
    
    # Multiply the processing matrix with the main matrix.
    # To apply the rotation to it. 
    self._multiply()
  
  def rotate_z(self,degrees) :
    ''' Rotation around the Y axe from the given angle in degrees. '''
    
    if not isinstance(degrees,int) and not isinstance(degrees,float) :
      raise TypeError(int,float)
    
    c=cos(radians(degrees))  # Compute the cosine from the given angle.
    s=sin(radians(degrees))  # Compute the sine from the given angle.
    
    # Initialise the processing matrix with the cosine and sine from the given angle. 
    self._processing_matrix[0]=c ; self._processing_matrix[4]=-s ; self._processing_matrix[8]=0  ; self._processing_matrix[12]=0 ;
    self._processing_matrix[1]=s ; self._processing_matrix[5]=c  ; self._processing_matrix[9]=0  ; self._processing_matrix[13]=0 ;
    self._processing_matrix[2]=0 ; self._processing_matrix[6]=0  ; self._processing_matrix[10]=1 ; self._processing_matrix[14]=0 ;
    self._processing_matrix[3]=0 ; self._processing_matrix[7]=0  ; self._processing_matrix[11]=0 ; self._processing_matrix[15]=1 ;
    
    # Multiply the processing matrix with the main matrix.
    # To apply the rotation to it. 
    self._multiply()
  
  def rows(self,vector_a,vector_b,vector_c) :
    ''' build an row matrix with the given vectors. '''
    
    if not isinstance(vector_a,Vector) and not isinstance(vector_b,Vector) and not isinstance(vector_c,Vector) :
      raise TypeError(Vector) 
    
    # Initialise the processing matrix with the given vectors components. 
    self._processing_matrix[0]=vector_a.x ; self._processing_matrix[4]=vector_a.y ; self._processing_matrix[8] =vector_a.z ; self._processing_matrix[12]=0 ;
    self._processing_matrix[1]=vector_b.x ; self._processing_matrix[5]=vector_b.y ; self._processing_matrix[9] =vector_b.z ; self._processing_matrix[13]=0 ;
    self._processing_matrix[2]=vector_c.x ; self._processing_matrix[6]=vector_c.y ; self._processing_matrix[10]=vector_b.z ; self._processing_matrix[14]=0 ;
    self._processing_matrix[3]=0          ; self._processing_matrix[7]=0          ; self._processing_matrix[11]=0          ; self._processing_matrix[15]=1 ;
    
    # Multiply the processing matrix with the main matrix.
    # To apply the row computing to it. 
    self._multiply()
  
  def columns(self,vector_a,vector_b,vector_c) :
    ''' build an column matrix with the given vectors. '''
    
    if not isinstance(vector_a,Vector) and not isinstance(vector_b,Vector) and not isinstance(vector_c,Vector) :
      raise TypeError(Vector) 
    
    # Initialise the processing matrix with the given vectors components. 
    self._processing_matrix[0]=vector_a.x ; self._processing_matrix[4]=vector_b.x ; self._processing_matrix[8] =vector_c.x ; self._processing_matrix[12]=0 ;
    self._processing_matrix[1]=vector_a.y ; self._processing_matrix[5]=vector_b.y ; self._processing_matrix[9] =vector_c.y ; self._processing_matrix[13]=0 ;
    self._processing_matrix[2]=vector_a.z ; self._processing_matrix[6]=vector_b.z ; self._processing_matrix[10]=vector_b.z ; self._processing_matrix[14]=0 ;
    self._processing_matrix[3]=0          ; self._processing_matrix[7]=0          ; self._processing_matrix[11]=0          ; self._processing_matrix[15]=1 ;
    
    # Multiply the processing matrix with the main matrix.
    # To apply the column computing to it. 
    self._multiply()
  
  def load_hardware(self) :
    ''' Load the current matrix instance as the, display, MODELVIEW matrix. '''
    
    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixd(self.main_matrix)
    
  def multiply_hardware(self) :
    ''' multiply the current matrix instance with the, display, MODELVIEW matrix. '''
    
    glMatrixMode(GL_MODELVIEW)
    glMultMatrixd(self.main_matrix)
  
  def get_hardware(self) :
    ''' Return the current MODELVIEW matrix as an array. '''
    
    matrix_get=glGetFloatv(GL_MODELVIEW_MATRIX)
    
    modelview_matrix[0]=matrix_get[0][0] ; modelview_matrix[4]=matrix_get[0][1] ; modelview_matrix[8] =matrix_get[0][2] ; modelview_matrix[12]=matrix_get[0][3] ;
    modelview_matrix[1]=matrix_get[1][0] ; modelview_matrix[5]=matrix_get[1][1] ; modelview_matrix[9] =matrix_get[1][2] ; modelview_matrix[13]=matrix_get[1][3] ;
    modelview_matrix[2]=matrix_get[2][0] ; modelview_matrix[6]=matrix_get[2][1] ; modelview_matrix[10]=matrix_get[2][2] ; modelview_matrix[14]=matrix_get[2][3] ;
    modelview_matrix[4]=matrix_get[3][0] ; modelview_matrix[7]=matrix_get[3][1] ; modelview_matrix[11]=matrix_get[3][2] ; modelview_matrix[15]=matrix_get[3][3] ;
    
    return modelview_matrix
  
  def mult_vertex(self,vertex) :
    ''' Multiply the current main matrix with the given vertex. 
        And return the result as an Vertex.
    '''
    
    if not isinstance(vertex,Vertex) :
      raise TypeError(Vertex)
    
    res_x= vertex.wx * self.main_matrix[0] + vertex.wy * self.main_matrix[4] + vertex.wz * self.main_matrix[8]  + self.main_matrix[12]
    res_y= vertex.wx * self.main_matrix[1] + vertex.wy * self.main_matrix[5] + vertex.wz * self.main_matrix[9]  + self.main_matrix[13]
    res_z= vertex.wx * self.main_matrix[2] + vertex.wy * self.main_matrix[6] + vertex.wz * self.main_matrix[10] + self.main_matrix[14]
    
    return Vertex(res_x,res_y,res_z)   
  
  def mult_vector(self,vector) :
    ''' Multiply the current main matrix with the given vector. 
        And return the result as an Vector.
    '''
    
    if not isinstance(vector,Vector) :
      raise TypeError(Vector)
    
    x= vector.x * self.main_matrix[0] + vector.y * self.main_matrix[4] + vector.z * self.main_matrix[8]
    y= vector.x * self.main_matrix[1] + vector.y * self.main_matrix[5] + vector.z * self.main_matrix[9]
    z= vector.x * self.main_matrix[2] + vector.y * self.main_matrix[6] + vector.z * self.main_matrix[10]
    
    return Vector(x,y,z)
  
  def rotate_vector(self,angle,vector) :
    ''' Rotate around the given vector (representing an axe) from the given angle. '''
    
    if not isinstance(vector,Vector) :
      raise TypeError(Vector)
    
    v = vector.mult_vector((1.0 / vector.length),vector)  # Normalise the vector length.
    x = v.x ; y = v.y ; z = v.z                           # Getting values for matrix computing. 
    
    c = cos(radians(angle))  # Compute the cosine from the given angle.
    s = sin(radians(angle))  # Compute the sine from the given angle.
    
    # Initialise the processing matrix complexes computing with cos,sin and vectors components. 
    self._processing_matrix[0]= x*x*(1-c)+c   ; self._processing_matrix[4]= x*y*(1-c)-z*s ; self._processing_matrix[8] = x*z*(1-c)+y*s ; self._processing_matrix[12]=0 ;
    self._processing_matrix[1]= x*y*(1-c)+z*s ; self._processing_matrix[5]= y*y*(1-c)+c   ; self._processing_matrix[9] = y*z*(1-c)-x*s ; self._processing_matrix[13]=0 ;
    self._processing_matrix[2]= x*z*(1-c)-y*s ; self._processing_matrix[6]= y*z*(1-c)+x*s ; self._processing_matrix[10]= z*z*(1-c)+c   ; self._processing_matrix[14]=0 ;
    self._processing_matrix[3]=0              ; self._processing_matrix[7]=0              ; self._processing_matrix[11]= 0             ; self._processing_matrix[15]=1 ;
    
    # Multiply the processing matrix with the main matrix.
    # To apply the vector rotating computing to it. 
    self._multiply()
  
  def mult_localview(self,localview) :
    ''' Multiply an given localview with the current main matrix. '''
    
    localview.pos=self.mult_vertex(localview.pos)      # Localview position multiplying.
    localview.right=self.mult_vector(localview.right)  # Localview X axe vector multiplying.
    localview.up=self.mult_vector(localview.up)        # Localview Y axe vector multiplying.
    localview.sight=self.mult_vector(localview.sight)  # Localview Z axe vector multiplying.
    
    return localview
  
  def get_result(self) :
    ''' Return an vertex issue from the main matrix multiplying. '''
    
    res_x= self.x * self.main_matrix[0] + self.y * self.main_matrix[4] + self.z * self.main_matrix[8] + self.main_matrix[12]
    res_y= self.x * self.main_matrix[1] + self.y * self.main_matrix[5] + self.z * self.main_matrix[9] + self.main_matrix[13]
    res_z= self.x * self.main_matrix[2] + self.y * self.main_matrix[6] + self.z * self.main_matrix[10] + self.main_matrix[14]
    
    return Vertex(res_x,res_y,res_z) 

  def _multiply(self) :
    ''' Multiply the main matrix with the processing matrix to update it.
        It multiply rows components per columns components.
    '''
    
    tmp_matrix=range(0,16) # We must use an temporary matrix for keeping the values are right.
                           # And not multiply with soon multiply values. 
    x=0
    while x < 16 :
      # Multiply the processing matrix with the main matrix values.
      
      value1= x % 4   # Column value.
      
      value2=(x/4)*4  # Row value.
      
      tmp_matrix[x]=   self._processing_matrix[value1]    *  self.main_matrix[value2+0]    \
                     + self._processing_matrix[value1+4]  *  self.main_matrix[value2+1]    \
                     + self._processing_matrix[value1+8]  *  self.main_matrix[value2+2]    \
                     + self._processing_matrix[value1+12] *  self.main_matrix[value2+3]
      
      x += 1
    
    for v in range(0,16) :
      # Copy the result in the main matrix.
      self.main_matrix[v]=tmp_matrix[v]
      
  def __mul__(self,mult) :
    ''' Multiply sign wrapper. '''
    
    if isinstance(mult,Vertex) :
      # The right operator is an vertex.
      
      res_x= mult.wx * self.main_matrix[0] + mult.wy * self.main_matrix[4] + mult.wz * self.main_matrix[8]  + self.main_matrix[12]
      res_y= mult.wx * self.main_matrix[1] + mult.wy * self.main_matrix[5] + mult.wz * self.main_matrix[9]  + self.main_matrix[13]
      res_z= mult.wx * self.main_matrix[2] + mult.wy * self.main_matrix[6] + mult.wz * self.main_matrix[10] + self.main_matrix[14]
      
      return Vertex(res_x,res_y,res_z)   

    elif isinstance(mult,Vector) :
      # The right operator is an vector.
      
      x= mult.x*self.main_matrix[0] + mult.y*self.main_matrix[4] + mult.z*self.main_matrix[8]
      y= mult.x*self.main_matrix[1] + mult.y*self.main_matrix[5] + mult.z*self.main_matrix[9]
      z= mult.x*self.main_matrix[2] + mult.y*self.main_matrix[6] + mult.z*self.main_matrix[10]
      
      return Vector(x,y,z)    
    
    else :
      # The right operator is suppose to be an Localview otherwise.
      try :
        mult.pos=self.mult_vertex(mult.pos)      # Localview position multiplying.
        mult.right=self.mult_vector(mult.right)  # Localview X axe vector multiplying.
        mult.up=self.mult_vector(mult.up)        # Localview Y axe vector multiplying.
        mult.sight=self.mult_vector(mult.sight)  # Localview Z axe vector multiplying.
        return mult
      except :
	return None
      
  def __doc__(self) :
    ''' Print documentation '''
    
    print '''
    The Matrix computing is the heart of the 3D programmation.
    
    You can configure the matrix to apply changing to your 3D object
    with the primary operations:
    
    -) Scaling
    -) Translating
    -) Rotation around the X, Y, Z axes.
    
    and others for matrix, vectors, localviews and vertex operations.
    
    And finally for replacing or mutiply the OpenGL MODELVIEW matrix
    with the matrix containing the desire settings.
    
    For apply movement on the own axe of your 3D object you must 
    
    first: translate the vertex of your 3D object according to his
	   center, which can be retrieve throught the pyglut module 
	   function: get_center_from_polyhedron(vertex_list).
    
    Then: multiply every vertex from your 3D object with the matrix.
    
    Finally: retranslate your 3D object according to his previous center.
    
    >>> m=Matrix()
    >>> m.translate(-object.center.wx,-object.center.wy,-object.center.wz)
    >>> m.scale(factor)     # The operations you want to perform.
    >>> m.rotate_x(angle)   # The operations you want to perform.
    >>> m.rotate_x(angle)   # The operations you want to perform.
    >>> m.rotate_y(angle)   # The operations you want to perform.
    >>> m.rotate_z(angle)   # The operations you want to perform.
    >>> res=[]
    >>> for v in object.vertex_list :
	  res.append( m * v )
    >>> object.vertex_list=res      
    >>> m.translate(object.center.wx,object.center.wy,object.center.wz) 

    This process is required for scaling your 3D object.
    Or for rotating your 3D object on his own axes.
    
    You can use the Matrix class for implementing an camera view:
    
    >>> m=Matrix()
    >>> m.translate(-1.0,-1.0,-1.0)
    >>> m.rotate_y(45)
    >>> m.load_hardware()
    
    The camera is placed at position -1.0,-1.0,-1.0 
    and rotated from 45 degrees in clock sens.
    
    And many others usage...
    '''