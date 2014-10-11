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
  
from OpenGL.GL import GL_FRONT_AND_BACK, GL_LINE, GL_FILL, GL_POLYGON

from datatype_color import  Color
from datatype_vertex import Vertex
from datatype_localview import Localview
from datatype_matrix import Matrix 

from center_utils import get_center_from_polyhedron

from polyhedrons_generators import generate_cube

class Cube(object) :
  def __init__(self,side_length,display_mode="lined",lines_color=False,faces_color=False,lines_width=1,display_ls=False) :
    ''' Generate an cube object with the given side length settings.
        
        display_mode = "lined" -> Only the lines will be displayed.
        display_mode = "faced" -> Only the faces will be displayed.
        display_mode = "twice" -> The lines and the faces will be displayed.
        lines_color  = An objet <type 'Color'> representing the lines color.
        faces_color  = An objet <type 'Color'> representing the faces color.
                       An 6-items-list from object <type 'Color'>.
                       One item per cube face. 
        lines_width  = An integer representing the lines width.
        display_ls   = Define if the localview should be display.
    '''
    
    if not isinstance(side_length,int) and not isinstance(side_length,float) :
      raise TypeError("Argument side_length",int,float)
    elif side_length <= 0.0 :
      raise ValueError("Value of argument side_length must be greater than 0.0") 
    
    if display_mode == "lined" or display_mode == "faced" or display_mode == "twice" :
      self.display_mode=display_mode
    else :
      raise ValueError("Argument display_mode","lined","faced","twice")
    
    if lines_color :
      if not isinstance(lines_color,Color) :
        raise TypeError("Argument lines_color",Color)
    
    if faces_color :
      if not isinstance(faces_color,Color) and not isinstance(faces_color,list) :
        raise TypeError(faces_color,Color,list)
      elif isinstance(faces_color,list) and len(faces_color) != 6 :
	print "Error faces_color argument:\nYou must give an list from 6 Color objects.\nOne Color object per face."
	quit()
      elif isinstance(faces_color,list) and len(faces_color) == 6 :
        tmp=[]
        faces_color_index=0
        while faces_color_index < 6 :
	  if type(faces_color[faces_color_index].a) == bool :
	    faces_color[faces_color_index].a=0
	  faces_color_index += 1
      
         	
    
    if not isinstance(lines_width,int) :
      raise TypeError("Argument lines_width",int)
    elif lines_width < 1 :
      raise ValueError(lines_width,"Lines width value too little.") 
    
    if isinstance(lines_color,Color) :
      if type(lines_color.a) == bool :
        lines_color.a=0
    
    if isinstance(faces_color,Color) :
      if type(faces_color.a) == bool :
	faces_color.a=0
    
    if isinstance(display_ls,bool) :
      self.display_ls=display_ls
    
    self.side_length=side_length
    self.lines_color=lines_color
    self.faces_color=faces_color
    self.lines_width=lines_width
    self.polyhedron=generate_cube(side_length)
    self.ls=Localview()
    
    self.center=Vertex(0.0,0.0,0.0)    
    
  def update_pos(self,matrix) :
    ''' Apply changing contains in the matrix argument. '''
    
    if not isinstance(matrix, Matrix) :
      raise TypeError(matrix,Matrix)
    
    center=[]
    tmp_polyhedron=[]
    
    for polygon in self.polyhedron :
      # Loop over every polygon from the polyhedron. 
      tmp_polygon=[]
      
      for vertex in polygon :
	# Loop over every vertice from the polygon.
	
	res_vertex= matrix * vertex # Multiply the current vertice with the matrix
 	
 	# Storing the new position from the vertice.
 	tmp_polygon.append(res_vertex)  # For the polyhedron polygon container.
	center.append(res_vertex)       # For polyhedron center computing.
      
      tmp_polyhedron.append(tmp_polygon)
    
    self.polyhedron=tmp_polyhedron                  # Update the polygon container with the new postion from every vertice.
    
    self.center=get_center_from_polyhedron(center)  # Update the polyhedron center.  
    
    self.ls= matrix * self.ls                       # Update the localview.
    
    
    
  def display(self) :
    ''' Cube displaying method towards the settings. '''
    
    
    faces_color_index=0  # Iterator, case there are more than one color for the faces displaying.
    
    if self.display_mode == "lined" or self.display_mode == "faced" :
      
      if self.display_mode == "lined" and self.lines_color :
	  # Configuration of polygons lines displaying.
	  glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
	  
	  if self.lines_color :
	    # Lines color configuration. 
	    glColor4ubv(self.lines_color.get_ubyte_v())

	  glLineWidth(self.lines_width)
	
      elif self.display_mode == "faced" :
	# Configuration of polygons faces displaying.
	glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
	
	if self.faces_color and isinstance(self.faces_color,Color) :
	  # Faces colorizing configuration.
	  glColor4ubv(self.faces_color.get_ubyte_v())
      
      for polygon in self.polyhedron :
	# We loop over the polyhedron polygons container.
	
	if self.faces_color and isinstance(self.faces_color,list) and self.display_mode == "faced" : 
	  # Faces multi-colorizing configuration.
	  glColor4ubv(self.faces_color[faces_color_index].get_ubyte_v())
	
	# Displaying one polygon:
	glBegin(GL_POLYGON)
	for v in polygon :
	  # We loop over the every vertice from the polygon.
	  glVertex3fv(v.get_vertex())
	glEnd()	
	
	faces_color_index += 1 
      
    elif self.display_mode == "twice" :
      
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
      
      if self.faces_color and isinstance(self.faces_color,Color) :
	glColor4ubv(self.faces_color.get_ubyte_v())
	
      for faces in self.polyhedron :
	# We loop over the polyhedron polygons container.
	
	if self.faces_color and isinstance(self.faces_color,list) :
	  # Faces multi-colorizing configuration.
	  glColor4ubv(self.faces_color[faces_color_index].get_ubyte_v())
	  
	# Displaying one polygon face:  
	glBegin(GL_POLYGON)
        for v in faces :
	   # We loop over the every vertice from the face.
	  glVertex3fv(v.get_vertex())
        glEnd()
        
        faces_color_index += 1  
        
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
      
      if self.lines_color :
	# Lines color configuration. 
	glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)
      
      # Displaying one polygon face edges: 
      for faces in self.polyhedron :
	
	glBegin(GL_POLYGON)
        for v in faces :
	  # We loop over the every vertice from the face.
	  glVertex3fv(v.get_vertex())
        glEnd() 
      
    if self.display_ls :
      # Displaying the Localview.
      self.ls.display(self.side_length*2.0/10.0)
   
  def set_display_mode(self,display_mode) :
    ''' Change the polyhedron display mode. 
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
    ''' Change the lines color from the polyhedron.
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
    ''' Change the faces color(s) from the polyhedron.
        Value of argument faces_color should be:
        faces_color  = An objet <type 'Color'> representing the faces color.
                       An 6-items-list from object <type 'Color'>.
                       One item per cube face. 
    '''
    
    if not isinstance(faces_color,Color) and not isinstance(faces_color,list) :
      raise TypeError(faces_color,Color,list)
    
    elif isinstance(faces_color,list) and len(faces_color) != 6 :
      print "Error faces_color argument:\nYou must give an list from 6 Color objects.\nOne Color object per face."
      quit()
    
    elif isinstance(faces_color,list) and len(faces_color) == 6 :
      tmp=[]
      faces_color_index=0
      while faces_color_index < 6 :
	if isinstance(faces_color[faces_color_index].a,bool) :
	  faces_color[faces_color_index].a=0
	faces_color_index += 1
    
    elif isinstance(faces_color,Color) :
      if type(faces_color.a) == bool :
	faces_color.a=0	  
    
    else :
      raise TypeError(Color)
    
    self.faces_color=faces_color
    
  def set_lines_width(self,lines_width) :
    ''' Change the lines width from the polyhedron.
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
    
  def set_side_length(self,side_length) :
    if not isinstance(side_length,int) and not isinstance(side_length,float) :
      raise TypeError("Argument side_length",int,float)
    elif side_length < 0.0 :
      raise ValueError("Value of argument side_length must be greater than 0.0") 
    
    self.side_length=side_length
    self.polyhedron=generate_cube(side_length)
    self.ls=Localview()
  
  def __doc__(self) :
    ''' Print documentation '''
    
    print '''
    Generate an cube object with position updating, 
    display and settings setters methods.
    
    The display mode set how the cube will be display 
    and can take as values:
    "lined" -> Only the edges will be display.
    "faces" -> Only the faces willbbe display.
    "twice" -> The edges and the faces will be display.
    
    The lines color must be an object from <type 'Color'> available throught
    this module as datatype dealing with colors as unsigned bytes 
    or floating-points values.
    
    The faces color can be:
    -> An object from <type 'Color'> in which case the cube will be filled with 
       this color.
    -> An list from objects from <type 'Color'> in which case the list length 
       must match the number of faces and define one color per face.
    
    The lines width must be an integer representing the number of pixels from 
    the edges width.
    
    The display_ls argument must be an boolean value point to if the polyhedron 
    own Localview will be displayed. 
    The datatype Localview is available throught this module. 
    sea his documentation to know more about.
    
    '''
    
    
      
      
      
            