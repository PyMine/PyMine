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
  
from OpenGL.GL import GL_LINES, GL_LINE_LOOP, GL_QUADS

from datatype_vertex import Vertex
from datatype_color import Color
from datatype_localview import Localview
from datatype_matrix import Matrix

from primary_operations import translate,rotate_y

from center_utils import get_center_from_polyhedron

from polyhedrons_generators import generate_toros

class Toros(object) :
  def __init__(self,base_polygon,base_radius,toros_radius,display_mode="lined",lines_color=False,faces_color=False,lines_width=1,display_ls=False) :
    ''' Generate an toros object with the given radius and basis polygone settings.
    
        base_polygon = the toros basis polygon.
        base_radius  = the toros basis polygon radius.
        toros_radius = the toros radius (without the base polygon radius). 
        display_mode = "lined" -> only the lines will be displayed.
        display_mode = "faced" -> only the faces will be displayed.
        display_mode = "twice" -> The lines and the faces will be displayed.
        lines_color  = an objet <type 'Color'> representing the lines color.
        faces_color  = an objet <type 'Color'> representing the faces color.
        line_width   = an integer representing the lines width.
    '''
    
    if not isinstance(base_polygon,int) :
      raise TypeError("base_polygon argument",int)

    if base_polygon <= 2 :
      print "the base polygon must be greater than 2 "
      quit()
    
    
    if not isinstance(base_radius,int) and not isinstance(base_radius,float) :
      raise TypeError("base_radius argument",int,float)
    elif base_radius <= 0.0 :
      raise ValueError("Value of base_radius must be greater than 0.0") 
    
    
    if not isinstance(toros_radius,int) and not isinstance(toros_radius,float) :
      raise TypeError("toros_radius argument",int,float)
    elif toros_radius <= 0.0 :
      raise ValueError("Value of toros_radius must be greater than 0.0") 
    
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
      
    self.base_polygon=base_polygon
    self.base_radius=base_radius
    self.toros_radius=toros_radius
    self.lines_color=lines_color
    self.faces_color=faces_color
    self.lines_width=lines_width
    self.toros=generate_toros(base_polygon,base_radius,toros_radius)
    self.ls=Localview()
    self.center=Vertex(0.0,0.0,0.0)
    
  def update_pos(self,matrix) :
    ''' Apply changing contains in the matrix argument. '''
    
    if not isinstance(matrix, Matrix) :
      raise TypeError(matrix,Matrix)
    
    center=[]
    tmp_toros=[]
    
    for polygon in self.toros :
      # Loop over every polygon from the toros. 
      tmp_polygon=[]
      
      for vertex in polygon :
	# Loop over every vertice from the polygon.
	
	res_vertex= matrix * vertex # Multiply the current vertice with the matrix
 	
 	# Storing the new position from the vertice.
 	tmp_polygon.append(res_vertex)  # For the toros polygon container.
	center.append(res_vertex)       # For toros center computing.
      
      tmp_toros.append(tmp_polygon)
    
    self.toros=tmp_toros                  # Update the polygon container with the new postion from every vertice.
    
    self.center=get_center_from_polyhedron(center)  # Update the toros center.  
    
    self.ls= matrix * self.ls                       # Update the localview.  
    
  def display(self) :
    if self.display_mode == "lined" :
      if self.lines_color :
        # Lines color configuration. 	
        glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)    # Setting the line width given as argument.
      
      i=0
      while i < len(self.toros) :
	glBegin(GL_LINE_LOOP)
	for v in self.toros[i] :
	  glVertex3fv(v.get_vertex())
	glEnd()
	i += 1
      
      i=-1
      while i < len(self.toros)-1 :
	ii=0
	while ii < len(self.toros[i]) :
	  glBegin(GL_LINES)
	  glVertex3fv(self.toros[i][ii].get_vertex())
	  glVertex3fv(self.toros[i+1][ii].get_vertex())
	  glEnd()
	  ii += 1
	i += 1	
	
    elif self.display_mode == "faced" :
      
      if self.faces_color :
	# Faces color configuration. 
        glColor4ubv(self.faces_color.get_ubyte_v())
	
      i=-1
      while i < len(self.toros)-1 :
	ii=-1
	while ii < len(self.toros[i])-1 :
	  glBegin(GL_QUADS)
	  glVertex3fv(self.toros[i][ii].get_vertex())
	  glVertex3fv(self.toros[i+1][ii].get_vertex())
	  glVertex3fv(self.toros[i+1][ii+1].get_vertex())
	  glVertex3fv(self.toros[i][ii+1].get_vertex())
	  glEnd()
	  ii += 1
	i += 1	
		    
      
    elif self.display_mode == "twice" :  
      
      if self.faces_color :
        glColor4ubv(self.faces_color.get_ubyte_v())
	
      i=-1
      while i < len(self.toros)-1 :
	ii=-1
	while ii < len(self.toros[i])-1 :
	  glBegin(GL_QUADS)
	  glVertex3fv(self.toros[i][ii].get_vertex())
	  glVertex3fv(self.toros[i+1][ii].get_vertex())
	  glVertex3fv(self.toros[i+1][ii+1].get_vertex())
	  glVertex3fv(self.toros[i][ii+1].get_vertex())
	  glEnd()
	  ii += 1
	i += 1	
	
      if self.lines_color :
        # Lines color configuration. 	
        glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)    # Setting the line width given as argument.
      
      i=0
      while i < len(self.toros) :
	glBegin(GL_LINE_LOOP)
	for v in self.toros[i] :
	  glVertex3fv(v.get_vertex())
	glEnd()
	i += 1
      
      i=-1
      while i < len(self.toros)-1 :
	ii=0
	while ii < len(self.toros[i]) :
	  glBegin(GL_LINES)
	  glVertex3fv(self.toros[i][ii].get_vertex())
	  glVertex3fv(self.toros[i+1][ii].get_vertex())
	  glEnd()
	  ii += 1
	i += 1	
	
    if self.display_ls :
      # Displaying the Localview.
      self.ls.display(self.base_radius*2.0/10.0)
      
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
    '''
    
    if isinstance(faces_color,Color) :
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
    
  def set_base_polygon(self,base_polygon) :
    ''' Change the toros basis polygon. '''
    
    if not isinstance(base_polygon,int) :
      raise TypeError("base_polygon argument",int)

    if base_polygon <= 2 :
      print "the base polygon must be greater than 2 "
      quit()
    
    
    self.base_polygon=base_polygon
    self.toros=generate_toros(base_polygon,self.base_radius,self.toros_radius)
    self.ls=Localview()
    
  def set_base_radius(self,base_radius) :
    ''' Change the toros base polygon radius. '''
    
    if not isinstance(base_radius,int) and not isinstance(base_radius,float) :
      raise TypeError("base_radius argument",int,float)
    elif base_radius <= 0.0 :
      raise ValueError("Value of base_radius must be greater than 0.0") 
    
    self.base_radius=base_radius
    self.toros=generate_toros(self.base_polygon,base_radius,self.toros_radius)
    self.ls=Localview()
  
  def set_toros_radius(self,toros_radius) :
    ''' Change the toros radius (without the base polygon radius). '''
    
    if not isinstance(toros_radius,int) and not isinstance(toros_radius,float) :
      raise TypeError("toros_radius argument",int,float)
    elif toros_radius <= 0.0 :
      raise ValueError("Value of toros_radius must be greater than 0.0") 
    
    self.toros_radius=toros_radius
    self.toros=generate_toros(self.base_polygon,self.base_radius,toros_radius)
    self.ls=Localview()
  
  def __doc__(self) :
    ''' Print documentation '''
    
    print '''
    Generate an toros object with position updating, 
    display and settings setters methods.
    
    The display mode set how the toros will be display 
    and can take as values:
    "lined" -> Only the edges will be display.
    "faces" -> Only the faces willbbe display.
    "twice" -> The edges and the faces will be display.
    
    The lines color must be an object from <type 'Color'> available throught
    this module as datatype dealing with colors as unsigned bytes 
    or floating-points values.
    
    The faces color can be:
    -> An object from <type 'Color'> in which case the toros will be filled 
       with this color.
    
    The lines width must be an integer representing the number of pixels from 
    the edges width.
    
    The display_ls argument must be an boolean value point to if the polyhedron 
    own Localview will be displayed. 
    The datatype Localview is available throught this module. 
    sea his documentation to know more about.
    
    '''        