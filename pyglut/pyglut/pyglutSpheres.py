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

from OpenGL.GL import glVertex3fv, glColor4ubv, glPolygonMode, glLineWidth, glBegin, glEnd
  
from OpenGL.GL import GL_FRONT_AND_BACK, GL_LINE, GL_FILL, GL_POLYGON, GL_LINE_LOOP, GL_QUADS, GL_TRIANGLES

from datatype_color import  Color
from datatype_vertex import Vertex
from datatype_localview import Localview
from datatype_matrix import Matrix 

from center_utils import get_center_from_polyhedron

from spheres_generators import generate_quad_sphere, generate_trigon_sphere

class Quad_Sphere(object) :
  def __init__(self,radius,basis,display_mode="lined",lines_color=False,faces_color=False,lines_width=1,display_ls=False) :
    ''' generate an quad sphere object with the given radius and polygone basis. 
    
        basis        = Integer taken as basis for the sphere generating.  
        radius       = Radius of the sphere. 
        display_mode = "lined" -> only the lines will be displayed.
        display_mode = "faced" -> only the faces will be displayed.
        display_mode = "twice" -> The lines and the faces will be displayed.
        lines_color  = an objet <type 'Color'> representing the lines color.
        faces_color  = an objet <type 'Color'> representing the faces color.
        line_width   = an integer representing the lines width.
    '''
    
    if not isinstance(radius,int) and not isinstance(radius,float) :
      raise TypeError(int,float)
    elif radius <= 0.0 :
      raise ValueError("Value of radius must be greater than 0.0") 
    
    if not isinstance(basis,int) :
      raise TypeError(int)

    if basis < 6 or basis % 2 :
      print "the basis for the sphere must be greater as 5 and basis % 2 == 0 "
      quit()
    
    if display_mode == "lined" or display_mode == "faced" or display_mode == "twice" :
      self.display_mode=display_mode
    else :
      raise ValueError("Argument display_mode","lined","faced","twice")
    
    if lines_color :
      if not isinstance(lines_color,Color) :
        raise TypeError("Argument lines_color",Color)
    
    if faces_color :
      if not isinstance(faces_color,Color) : 
        raise TypeError("Argument faces_color",Color)
      
    if not isinstance(lines_width,int) :
      raise TypeError(lines_width,int)
    elif lines_width < 1 :
      raise ValueError("Lines width value too little.") 
      
    
    
    if isinstance(lines_color,Color) :
      if type(lines_color.a) == bool :
        lines_color.a=0
    
    if isinstance(faces_color,Color) :
      if type(faces_color.a) == bool :
	faces_color.a=0
    
    if isinstance(display_ls,bool) :
      self.display_ls=display_ls
    
    self.lines_color=lines_color
    self.faces_color=faces_color
    self.lines_width=lines_width
    self.basis=basis
    self.radius=radius
    self.polygons=generate_quad_sphere(basis,radius)[0]
    self.ls=Localview()
    
    self.center=Vertex(0.0,0.0,0.0)    
    
  def update_pos(self,matrix) :
    ''' Apply changing contains in the matrix argument. '''
    
    if not isinstance(matrix, Matrix) :
      raise TypeError(matrix,Matrix)
    
    center=[]
    tmp_polyhedron=[]
    for lines in self.polygons :
      # Loop over every line from the sphere. 
      tmp_polygon=[]
      for vertex in lines :
	# Loop over every line from the line.
	
	res_vertex= matrix * vertex # Multiply the current vertice with the matrix
 	
 	# Storing the new position from the vertice.
 	tmp_polygon.append(res_vertex)  # For the sphere polygon container.
	center.append(res_vertex)       # For sphere center computing.
	
      tmp_polyhedron.append(tmp_polygon)
    
    self.polygons=tmp_polyhedron
    
    self.center=get_center_from_polyhedron(center)  
    
    self.ls= matrix * self.ls
    
    
    
  def display(self) :
    if self.display_mode == "lined" :
      if self.lines_color :
        # Lines color configuration. 	
        glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)    # Setting the line width given as argument.
      
      i=0
      while i < len(self.polygons) :
	# Loop displaying the lines of the polygons on an surface of the sphere.
	# We process by crossing the line displaying.
	ii=0
	glBegin(GL_LINE_LOOP)
	while ii < len(self.polygons[i]) :
	  glVertex3fv(self.polygons[i][ii].get_vertex())
	  ii += 1 
	glEnd()
	i += 1    
      
      
      i=0
      while i < len(self.polygons) :
	# Loop displaying the lines of the polygons on an surface of the sphere.
	# We process by crossing the line displaying.
	ii=0
	glBegin(GL_LINE_LOOP)
	while ii < len(self.polygons[i]) : 
	  glVertex3fv(self.polygons[ii][i].get_vertex())
	  ii += 1  
	glEnd()
	i += 1
	
    elif self.display_mode == "faced" :
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL) 
      
      if self.faces_color :
	# Faces color configuration. 
        glColor4ubv(self.faces_color.get_ubyte_v())
	
      i=0	
      while i < len(self.polygons) :
	# Iteration over the polygon container variable to compute the quads.
	ii=0
	while ii < self.basis-1 :
	  # We compute the quads: for spheres quads displaying.
	  glBegin(GL_QUADS)
	  if not i == self.basis-1 :
	    glVertex3fv(self.polygons[i][ii].get_vertex())
	    glVertex3fv(self.polygons[i+1][ii].get_vertex())
	    glVertex3fv(self.polygons[i+1][ii+1].get_vertex())
	    glVertex3fv(self.polygons[i][ii+1].get_vertex())
	  else :
	    glVertex3fv(self.polygons[i][ii].get_vertex())
	    glVertex3fv(self.polygons[0][ii].get_vertex())
	    glVertex3fv(self.polygons[0][ii+1].get_vertex())
	    glVertex3fv(self.polygons[i][ii+1].get_vertex())
          
          glEnd()
          
	  ii += 1
	i += 1
		  
      
    elif self.display_mode == "twice" :  
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL) 
      
      if self.faces_color :
        glColor4ubv(self.faces_color.get_ubyte_v())
	
      i=0	
      while i < len(self.polygons) :
	# Iteration over the polygon container variable to compute the quads.
	ii=0
	while ii < self.basis-1 :
	  # We compute the quads: for spheres quads displaying.
	  glBegin(GL_QUADS)
	  if not i == self.basis-1 :
	    glVertex3fv(self.polygons[i][ii].get_vertex())
	    glVertex3fv(self.polygons[i+1][ii].get_vertex())
	    glVertex3fv(self.polygons[i+1][ii+1].get_vertex())
	    glVertex3fv(self.polygons[i][ii+1].get_vertex())
	  else :
	    glVertex3fv(self.polygons[i][ii].get_vertex())
	    glVertex3fv(self.polygons[0][ii].get_vertex())
	    glVertex3fv(self.polygons[0][ii+1].get_vertex())
	    glVertex3fv(self.polygons[i][ii+1].get_vertex())
          
          glEnd()
          
	  ii += 1
	i += 1
	
      if self.lines_color :
        # Lines color configuration. 	
        glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)    # Setting the line width given as argument.
      
      i=0
      while i < len(self.polygons) :
	# Loop displaying the lines of the polygons on an surface of the sphere.
	# We process by crossing the line displaying.
	ii=0
	glBegin(GL_LINE_LOOP)
	while ii < len(self.polygons[i]) :
	  glVertex3fv(self.polygons[i][ii].get_vertex())
	  ii += 1 
	glEnd()
	i += 1    
      
      
      i=0
      while i < len(self.polygons) :
	# Loop displaying the lines of the polygons on an surface of the sphere.
	# We process by crossing the line displaying.
	ii=0
	glBegin(GL_LINE_LOOP)
	while ii < len(self.polygons[i]) : 
	  glVertex3fv(self.polygons[ii][i].get_vertex())
	  ii += 1  
	glEnd()
	i += 1	
	
    if self.display_ls :
      # Displaying the Localview.
      self.ls.display(self.radius*2.0/10.0)	
	
  def set_display_mode(self,display_mode) :
    ''' Change the sphere display mode. 
        Value of argument display_mode should be:
        display_mode = "lined" -> Only the lines will be displayed.
        display_mode = "faced" -> Only the faces will be displayed.
        display_mode = "twice" -> The lines and the faces willbe displayed.
    '''
    
    if display_mode == "lined" or display_mode == "faced" or display_mode == "twice" :
      self.display_mode=display_mode
    else :
      raise ValueError("lined","faced","twice")
    
    self.display_mode=display_mode
    
  def set_lines_color(self,lines_color) :
    ''' Change the lines color from the sphere.
        Value of argument lines_color should be:
        lines_color  = An objet <type 'Color'> representing the lines color.
    '''
    
    if lines_color :
      if not isinstance(lines_color,Color) :
        raise TypeError("Argument lines_color",Color)
      
      if isinstance(lines_color.a,bool) :
	lines_color.a=0
	
    self.lines_color=lines_color
    
  def set_faces_color(self,faces_color) :
    ''' Change the faces color(s) from the sphere.
        Value of argument faces_color should be:
        faces_color  = An objet <type 'Color'> representing the faces color.
    '''                   
    
    if isinstance(faces_color,Color) :
      if type(faces_color.a) == bool :
	faces_color.a=0	  
    
    else :
      raise TypeError(Color)
    
    self.faces_color=faces_color
    
  def set_lines_width(self,lines_width) :
    ''' Change the lines width from the sphere.
        Value of argument lines_width should be:
        lines_width  = An integer representing the lines width.
    '''
    if not isinstance(lines_width,int) :
      raise TypeError("Argument lines_width",int)
    elif lines_width < 1 :
      raise ValueError(lines_width,"Lines width value too little.") 
    
    self.lines_width=lines_width
    
  def set_display_ls(self,display_ls) :
    ''' Change the Localview displaying setting.
        Value of argument display_ls should be an boolean value:
        display_ls   = Define if the localview should be display.
    '''    
        
    if isinstance(display_ls,bool) :
      self.display_ls=display_ls
    else :
      raise TypeError("Argument display_ls",bool)
    
  def set_basis(self,basis) :
    ''' Change the quad sphere basis. '''
    
    if not isinstance(basis,int) :
      raise TypeError(int)

    if basis < 6 or basis % 2 :
      print "the basis for the sphere must be greater as 5 and basis % 2 == 0 "
      quit()
    
    self.basis=basis
    self.polygons=generate_quad_sphere(basis,self.radius)[0]
    self.ls=Localview()
    
  def set_radius(self,radius) :
    ''' Change the quad sphere radius. '''
    
    if not isinstance(radius,int) and not isinstance(radius,float) :
      raise TypeError(int,float)
    elif radius < 0.0 :
      raise ValueError("Value of radius must be greater than 0.0") 
    
    self.radius=radius
    self.polygons=generate_quad_sphere(self.basis,radius)[0]
    self.ls=Localview()
    
  
  def __doc__(self) :
    ''' Print documentation '''
    
    print '''
    Generate an quad sphere object with position updating, 
    display and settings setters methods.
    
    An "quad sphere" is an sphere which faces are trapezium
    except the poles which are trigons.
    
    The display mode set how the quad sphere will be display 
    and can take as values:
    "lined" -> Only the edges will be display.
    "faces" -> Only the faces willbbe display.
    "twice" -> The edges and the faces will be display.
    
    The lines color must be an object from <type 'Color'> available throught
    this module as datatype dealing with colors as unsigned bytes 
    or floating-points values.
    
    The faces color can be:
    -> An object from <type 'Color'> in which case the quad sphere 
       will be filled with this color.
    
    The lines width must be an integer representing the number of pixels from 
    the edges width.
    
    The display_ls argument must be an boolean value point to if the sphere 
    own Localview will be displayed. 
    The datatype Localview is available throught this module. 
    sea his documentation to know more about.
    
    '''	
	
  
  
class Trigon_Sphere(object) :
  def __init__(self,radius,basis,display_mode="lined",lines_color=False,faces_color=False,lines_width=1,display_ls=False) :
    ''' generate an trigon sphere object with the given radius and polygone basis.
    
        basis        = Integer taken as basis for the sphere generating.  
        radius       = Radius of the sphere. 
        display_mode = "lined" -> only the lines will be displayed.
        display_mode = "faced" -> only the faces will be displayed.
        display_mode = "twice" -> The lines and the faces will be displayed.
        lines_color  = an objet <type 'Color'> representing the lines color.
        faces_color  = an objet <type 'Color'> representing the faces color.
        line_width   = an integer representing the lines width.
    '''
    
    if not isinstance(radius,int) and not isinstance(radius,float) :
      raise TypeError(int,float)
    elif radius <= 0.0 :
      raise ValueError("Value of radius must be greater than 0.0") 
    
    if not isinstance(basis,int) :
      raise TypeError(int)

    if basis < 6 or basis % 4 :
      print "the basis for the sphere must be greater as 5 and basis % 4 == 0 "
      quit()
    
    if display_mode == "lined" or display_mode == "faced" or display_mode == "twice" :
      self.display_mode=display_mode
    else :
      raise ValueError("Argument display_mode","lined","faced","twice")
    
    if lines_color :
      if not isinstance(lines_color,Color) :
        raise TypeError("Argument lines_color",Color)
    
    if faces_color :
      if not isinstance(faces_color,Color) : 
        raise TypeError("Argument faces_color",Color)
      
      
         	
    
    if not isinstance(lines_width,int) :
      raise TypeError(lines_width,int)
    elif lines_width < 1 :
      raise ValueError("Lines width value too little.") 
    
    if isinstance(lines_color,Color) :
      if type(lines_color.a) == bool :
        lines_color.a=0
    
    if not type(faces_color) == bool :
      if type(faces_color.a) == bool :
	faces_color.a=0
    
    if isinstance(display_ls,bool) :
      self.display_ls=display_ls
    
    self.lines_color=lines_color
    self.faces_color=faces_color
    self.lines_width=lines_width
    self.basis=basis
    self.radius=radius
    self.trigons=generate_trigon_sphere(basis,radius)[0]
    self.ls=Localview()
    
    self.center=Vertex(0.0,0.0,0.0)    
    
  def update_pos(self,matrix) :
    ''' Apply changing contains in the matrix argument. '''
    
    if not isinstance(matrix, Matrix) :
      raise TypeError(matrix,Matrix)
    
    center=[]
    tmp_polyhedron=[]
    for polygon in self.trigons :
      # Loop over every polygon from the sphere. 
      tmp_polygon=[]
      
      for vertex in polygon :
	# Loop over every vertice from the polygon.
	
	res_vertex= matrix * vertex # Multiply the current vertice with the matrix
 	
 	# Storing the new position from the vertice.
 	tmp_polygon.append(res_vertex)  # For the sphere polygon container.
	center.append(res_vertex)       # For sphere center computing.
      
      tmp_polyhedron.append(tmp_polygon)
    
    self.trigons=tmp_polyhedron                       # Update the polygon container with the new postion from every vertice.
    
    self.center=get_center_from_polyhedron(center)    # Update the sphere center.  
    
    self.ls= matrix * self.ls                         # Update the localview.
    
    
    
  def display(self) :
    if self.display_mode == "lined" :
      
      if self.lines_color :	
        # Lines color configuration. 
        glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)    # Setting the line width given as argument.
     
      i=-1
      boolean=False

      while i < len(self.trigons)-1 :
	# Loop to display the triangles from our sphere.
	# Throught iterating over the polygons on the XZ surface.
	ii=-1
	while ii < len(self.trigons[i])-1 :
          glBegin(GL_LINE_LOOP)
	  if boolean :
	    glVertex3fv(self.trigons[i][ii].get_vertex())
	    glVertex3fv(self.trigons[i][ii+1].get_vertex())
	    glVertex3fv(self.trigons[i+1][ii].get_vertex())
	  else :
	    glVertex3fv(self.trigons[i][ii].get_vertex())
	    glVertex3fv(self.trigons[i][ii+1].get_vertex())
	    glVertex3fv(self.trigons[i+1][ii+1].get_vertex())
          glEnd()
	  ii += 1

	if boolean :
	  boolean=False
	else :
	  boolean=True

	i += 1
	  
    elif self.display_mode == "faced" :
      
      if self.faces_color :	
        # Faces color configuration. 
        glColor4ubv(self.faces_color.get_ubyte_v())
      
      i=-1
      boolean=False

      while i < len(self.trigons)-1 :
	# Loop to display the triangles from our sphere.
	# Throught iterating over the polygons on the XZ surface.
	ii=-1
	while ii < len(self.trigons[i])-1 :
          glBegin(GL_TRIANGLES)
	  if boolean :
	    glVertex3fv(self.trigons[i][ii].get_vertex())
	    glVertex3fv(self.trigons[i][ii+1].get_vertex())
	    glVertex3fv(self.trigons[i+1][ii].get_vertex())
	  else :
	    glVertex3fv(self.trigons[i][ii].get_vertex())
	    glVertex3fv(self.trigons[i][ii+1].get_vertex())
	    glVertex3fv(self.trigons[i+1][ii+1].get_vertex())
          glEnd()
	  ii += 1

	if boolean :
	  boolean=False
	else :
	  boolean=True

	i += 1
		  
      
    if self.display_mode == "twice" :  
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL) 
      
      if self.faces_color :
         # Faces color configuration. 	
        glColor4ubv(self.faces_color.get_ubyte_v())
      
      
      i=-1
      boolean=False

      while i < len(self.trigons)-1 :
	# Loop to display the triangles from our sphere.
	# Throught iterating over the polygons on the XZ surface.
	ii=-1
	while ii < len(self.trigons[i])-1 :
          glBegin(GL_TRIANGLES)
	  if boolean :
	    glVertex3fv(self.trigons[i][ii].get_vertex())
	    glVertex3fv(self.trigons[i][ii+1].get_vertex())
	    glVertex3fv(self.trigons[i+1][ii].get_vertex())
	  else :
	    glVertex3fv(self.trigons[i][ii].get_vertex())
	    glVertex3fv(self.trigons[i][ii+1].get_vertex())
	    glVertex3fv(self.trigons[i+1][ii+1].get_vertex())
          glEnd()
	  ii += 1

	if boolean :
	  boolean=False
	else :
	  boolean=True

	i += 1
	
      if self.lines_color :
         # Lines color configuration. 	
        glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)    # Setting the line width given as argument.
     
      i=-1
      boolean=False

      while i < len(self.trigons)-1 :
	# Loop to display the triangles from our sphere.
	# Throught iterating over the polygons on the XZ surface.
	ii=-1
	while ii < len(self.trigons[i])-1 :
          glBegin(GL_LINE_LOOP)
	  if boolean :
	    glVertex3fv(self.trigons[i][ii].get_vertex())
	    glVertex3fv(self.trigons[i][ii+1].get_vertex())
	    glVertex3fv(self.trigons[i+1][ii].get_vertex())
	  else :
	    glVertex3fv(self.trigons[i][ii].get_vertex())
	    glVertex3fv(self.trigons[i][ii+1].get_vertex())
	    glVertex3fv(self.trigons[i+1][ii+1].get_vertex())
          glEnd()
	  ii += 1

	if boolean :
	  boolean=False
	else :
	  boolean=True

	i += 1

    if self.display_ls :
      # Displaying the Localview.
      self.ls.display(self.radius*2.0/10.0)

  def set_display_mode(self,display_mode) :
    ''' Change the sphere display mode. 
        Value of argument display_mode should be:
        display_mode = "lined" -> Only the lines will be displayed.
        display_mode = "faced" -> Only the faces will be displayed.
        display_mode = "twice" -> The lines and the faces willbe displayed.
    '''
    
    if display_mode == "lined" or display_mode == "faced" or display_mode == "twice" :
      self.display_mode=display_mode
    else :
      raise ValueError("lined","faced","twice")
    
    self.display_mode=display_mode
    
  def set_lines_color(self,lines_color) :
    ''' Change the lines color from the sphere.
        Value of argument lines_color should be:
        lines_color  = An objet <type 'Color'> representing the lines color.
    '''
    
    if lines_color :
      if not isinstance(lines_color,Color) :
        raise TypeError("Argument lines_color",Color)
      
      if isinstance(lines_color.a,bool) :
	lines_color.a=0
	
    self.lines_color=lines_color
    
  def set_faces_color(self,faces_color) :
    ''' Change the faces color(s) from the sphere.
        Value of argument faces_color should be:
        faces_color  = An objet <type 'Color'> representing the faces color.
    '''
    
    if isinstance(faces_color,Color) :
      if type(faces_color.a) == bool :
	faces_color.a=0	  
    
    else :
      raise TypeError(Color)
    
    self.faces_color=faces_color
    
  def set_lines_width(self,lines_width) :
    ''' Change the lines width from the sphere.
        Value of argument lines_width should be:
        lines_width  = An integer representing the lines width.
    '''
    if not isinstance(lines_width,int) :
      raise TypeError("Argument lines_width",int)
    elif lines_width < 1 :
      raise ValueError(lines_width,"Lines width value too little.") 
    
    self.lines_width=lines_width
    
  def set_display_ls(self,display_ls) :
    ''' Change the Localview displaying setting.
        Value of argument display_ls should be an boolean value:
        display_ls   = Define if the localview should be display.
    '''    
        
    if isinstance(display_ls,bool) :
      self.display_ls=display_ls
    else :
      raise TypeError("Argument display_ls",bool)
    
  def set_basis(self,basis) :
    ''' Change the trigon sphere basis. '''
    
    if not isinstance(basis,int) :
      raise TypeError(int)

    if basis < 6 or basis % 2 :
      print "the basis for the sphere must be greater as 5 and basis % 2 == 0 "
      quit()
    
    self.basis=basis
    self.trigons=generate_trigon_sphere(basis,self.radius)[0]
    self.ls=Localview()
    
  def set_radius(self,radius) :
    ''' Change the trigon sphere radius. '''
    
    if not isinstance(radius,int) and not isinstance(radius,float) :
      raise TypeError(int,float)
    elif radius < 0.0 :
      raise ValueError("Value of radius must be greater than 0.0") 
    
    self.radius=radius
    self.trigons=generate_trigon_sphere(self.basis,radius)[0]
    self.ls=Localview()
  
  def __doc__(self) :
    ''' Print documentation '''
    
    print '''
    Generate an trigon sphere object with position updating, 
    display and settings setters methods.
    
    An "trigon sphere" is an sphere which every faces is an trigon.
    
    The display mode set how the trigon sphere will be display 
    and can take as values:
    "lined" -> Only the edges will be display.
    "faces" -> Only the faces willbbe display.
    "twice" -> The edges and the faces will be display.
    
    The lines color must be an object from <type 'Color'> available throught
    this module as datatype dealing with colors as unsigned bytes 
    or floating-points values.
    
    The faces color can be:
    -> An object from <type 'Color'> in which case the trigon sphere 
       will be filled with this color.
    
    The lines width must be an integer representing the number of pixels from 
    the edges width.
    
    The display_ls argument must be an boolean value point to if the sphere 
    own Localview will be displayed. 
    The datatype Localview is available throught this module. 
    sea his documentation to know more about.
    
    '''    