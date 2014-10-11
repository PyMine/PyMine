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

from datatype_color import *

from datatype_localview import Localview
from datatype_vertex import Vertex 
from datatype_matrix import Matrix 

from center_utils import get_center_from_polyhedron

from polyhedrons_generators import generate_polyhedron_26_faces

class Poly26Hedron(object) :
  def __init__(self,side_length,display_mode="lined",lines_color=False,quads_color=False,triangles_color=False,lines_width=1,display_ls=False) :
    ''' generate an 26 faces polyhedron object with the given side length settings.
           
        display_mode    = "lined" -> only the lines will be displayed.
        display_mode    = "faced" -> only the faces will be displayed.
        display_mode    = "twice" -> The lines and the faces will be displayed.
        lines_color     = an objet <type 'Color'> representing the lines color.
        quads_color     = an objet <type 'Color'> representing the quads color.
                          an 18-items-list contains <type 'Color'> objects.  
        triangles_color = an objet <type 'Color'> representing the triangles color.
                          an 8-items-list contains <type 'Color'> objects. 
        line_width      = an integer representing the lines width.
    '''
    
    if not isinstance(side_length,int) and not isinstance(side_length,float) :
      raise TypeError(int,float)
    elif side_length < 0.0 :
      raise ValueError("Value of side_length must be greater than 0.0") 
    
    if display_mode == "lined" or display_mode == "faced" or display_mode == "twice" :
      self.display_mode=display_mode
    else :
      raise ValueError("lined","faced","twice")
    
    if lines_color :
      if not isinstance(lines_color,Color) :
        raise TypeError(lines_color,Color)
    
    if quads_color :
      if not isinstance(quads_color,Color) and not isinstance(quads_color,list) :
        raise TypeError(quads_color,Color,list)
      elif isinstance(quads_color,list) and len(quads_color) != 18 :
	print "Error quads_color argument:\nYou must give an list from 18 Color objects.\nOne Color object per face."
	quit()
      elif isinstance(quads_color,list) and len(quads_color) == 18 :
        tmp=[]
        quads_color_index=0
        while quads_color_index < 18 :
	  if type(quads_color[quads_color_index].a) == bool :
	    quads_color[quads_color_index].a=0
	  quads_color_index += 1
      
    if triangles_color :
      if not isinstance(triangles_color,Color) and not isinstance(triangles_color,list) :
        raise TypeError(triangles_color,Color,list)
      elif isinstance(triangles_color,list) and len(triangles_color) != 8 :
	print "Error triangles_color argument:\nYou must give an list from 8 Color objects.\nOne Color object per face."
	quit()
      elif isinstance(triangles_color,list) and len(triangles_color) == 8 :
        tmp=[]
        triangles_color_index=0
        while triangles_color_index < 8 :
	  if type(triangles_color[triangles_color_index].a) == bool :
	    triangles_color[triangles_color_index].a=0
	  triangles_color_index += 1    
        
    
    if not isinstance(lines_width,int) :
      raise TypeError(lines_width,int)
    elif lines_width < 1 :
      raise ValueError(lines_width,"Lines width value too little.") 
    
    if isinstance(lines_color,Color) :
      if type(lines_color.a) == bool :
        lines_color.a=0
    
    if isinstance(quads_color,Color) :
      if type(quads_color.a) == bool :
	quads_color.a=0
	
    if isinstance(triangles_color,Color) :
      if type(triangles_color.a) == bool :
	triangles_color.a=0 	
    
    if isinstance(display_ls,bool) :
      self.display_ls=display_ls
    
    self.side_length=side_length
    self.lines_color=lines_color
    self.quads_color=quads_color
    self.triangles_color=triangles_color
    self.lines_width=lines_width
    self.triangles,self.quads=generate_polyhedron_26_faces(side_length)
    self.ls=Localview()
    
    self.center=Vertex(0.0,0.0,0.0)    
    
  def update_pos(self,matrix) :
    ''' Apply changing contains in the matrix argument. '''
    
    if not isinstance(matrix, Matrix) :
      raise TypeError(matrix,Matrix)
    
    center=[]
    tmp_quads=[]
    for polygon in self.quads :
      tmp_polygon=[]
      for vertex in polygon :
	# Loop over every vertice from the polygon.
	
	res_vertex= matrix * vertex # Multiply the current vertice with the matrix
	
	# Storing the new position from the vertice.
	tmp_polygon.append(res_vertex)  # For the polyhedron polygon container.
	center.append(res_vertex)       # For polyhedron center computing.
	
      tmp_quads.append(tmp_polygon)
    
    
    self.quads=tmp_quads        # Update the quad container with the new postion from every vertice.
    
    tmp_triangles=[]
    for polygon in self.triangles :
      tmp_polygon=[]
      for vertex in polygon :
	# Loop over every vertice from the polygon.
	
	res_vertex= matrix * vertex # Multiply the current vertice with the matrix
	
	# Storing the new position from the vertice.
	tmp_polygon.append(res_vertex)  # For the polyhedron polygon container.
	center.append(res_vertex)       # For polyhedron center computing.
	  
      tmp_triangles.append(tmp_polygon)
    
    self.triangles=tmp_triangles        # Update the triangle container with the new postion from every vertice.
    
    self.center=get_center_from_polyhedron(center)  # Update the polyhedron center. 
    
    self.ls= matrix * self.ls                       # Update the localview.
    
    
    
  def display(self) :
    
    if self.display_mode == "lined" :
      # Configuration of polygons lines displaying.
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
      
      if self.lines_color :
	# Lines color configuration. 
	glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)
    
    
      for polygon in self.quads :
	# Loop over every quad from the polyhedron. 
	# For only lines displaying.
        glBegin(GL_POLYGON)
        for v in polygon :
	   # We loop over the every vertice from the polygon.
	  glVertex3fv(v.get_vertex())
        glEnd()	
      
    
    elif self.display_mode == "faced" :
      # Configuration of polygons faces displaying.
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
      
      if self.quads_color and isinstance(self.quads_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.quads_color.get_ubyte_v())
      
      
	
      quads_color_index=0  # Iterator, case there are more than one color for the faces displaying.		
	
      if self.quads_color and isinstance(self.quads_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.quads_color.get_ubyte_v())
      
      for polygon in self.quads :
	# Loop over every quad from the polyhedron. 
	if self.quads_color and isinstance(self.quads_color,list) : 
	  # Case there are more than one color for the faces displaying.
	  glColor4ubv(self.quads_color[quads_color_index].get_ubyte_v())
	
	glBegin(GL_POLYGON)
	for v in polygon :
	   # We loop over the every vertice from the polygon.
	  glVertex3fv(v.get_vertex())
	glEnd()	
    
	quads_color_index += 1
      
      if self.triangles_color and isinstance(self.triangles_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.triangles_color.get_ubyte_v())
	
      triangles_color_index=0  # Iterator, case there are more than one color for the faces displaying.	
	
      for polygon in self.triangles :
	# Loop over every triangle from the polyhedron. 
	if self.triangles_color and isinstance(self.triangles_color,list) :
	  # Case there are more than one color for the faces displaying.
	  glColor4ubv(self.triangles_color[triangles_color_index].get_ubyte_v())
	  
	glBegin(GL_POLYGON)
	for v in polygon :
	   # We loop over the every vertice from the polygon.
	  glVertex3fv(v.get_vertex())
	glEnd()
	triangles_color_index += 1
      
    elif self.display_mode == "twice" :
      # Configuration of polygons faces displaying.  
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
      
      if self.quads_color and isinstance(self.quads_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.quads_color.get_ubyte_v())
      
      
	
      quads_color_index=0  # Iterator, case there are more than one color for the faces displaying.		
	
      if self.quads_color and isinstance(self.quads_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.quads_color.get_ubyte_v())
      
      for polygon in self.quads :
	# Loop over every quad from the polyhedron. 
	if self.quads_color and isinstance(self.quads_color,list) : 
	  glColor4ubv(self.quads_color[quads_color_index].get_ubyte_v())
	
	glBegin(GL_POLYGON)
	for v in polygon :
	   # We loop over the every vertice from the polygon.
	  glVertex3fv(v.get_vertex())
	glEnd()	
    
	quads_color_index += 1
      
      if self.triangles_color and isinstance(self.triangles_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.triangles_color.get_ubyte_v())
	
      triangles_color_index=0  # Iterator, case there are more than one color for the faces displaying.	
	
      for polygon in self.triangles :
	# Loop over every triangle from the polyhedron. 
	if self.triangles_color and isinstance(self.triangles_color,list) : 
	  # Case there are more than one color for the faces displaying.
	  glColor4ubv(self.triangles_color[triangles_color_index].get_ubyte_v())
	  
	glBegin(GL_POLYGON)
	for v in polygon :
	  # We loop over the every vertice from the polygon.
	  glVertex3fv(v.get_vertex())
	glEnd()
	triangles_color_index += 1
       
      # Configuration of polygons lines displaying. 
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
      
      if self.lines_color :
	# Lines color configuration. 
	glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)
    
    
      for polygon in self.quads :
	# Loop over every quad from the polyhedron. 
	# For only lines displaying.
        glBegin(GL_POLYGON)
        for v in polygon :
	  # We loop over the every vertice from the polygon.
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
    
  def set_quads_color(self,quads_color) :
    ''' Change the faces color(s) from the polyhedron.
        Value of argument quads_color should be:
        quads_color  = An objet <type 'Color'> representing the quads faces color.
                       An 18-items-list from object <type 'Color'>.
                       One item per quad face. 
    '''
    
    if quads_color :
      
      if not isinstance(quads_color,Color) and not isinstance(quads_color,list) :
        raise TypeError(quads_color,Color,list)
      
      elif isinstance(quads_color,list) and len(quads_color) != 18 :
	print "Error quads_color argument:\nYou must give an list from 18 Color objects.\nOne Color object per face."
	quit()
	
      elif isinstance(quads_color,list) and len(quads_color) == 18 :
        tmp=[]
        quads_color_index=0
        while quads_color_index < 18 :
	  if type(quads_color[quads_color_index].a) == bool :
	    quads_color[quads_color_index].a=0
	  quads_color_index += 1
      
      elif isinstance(quads_color,Color) :
	if type(quads_color.a) == bool :
	    quads_color.a=0
      
      else :
        raise TypeError(Color)
      
      self.quads_color=quads_color
    
  def set_triangles_color(self,triangles_color) :
    ''' Change the faces color(s) from the polyhedron.
        Value of argument triangles_color should be:
        triangles_color  = An objet <type 'Color'> representing the triangles faces color.
                           An 8-items-list from object <type 'Color'>.
                           One item per triangles face. 
    '''
    
    if triangles_color :
      
      if not isinstance(triangles_color,Color) and not isinstance(triangles_color,list) :
        raise TypeError(triangles_color,Color,list)
      
      elif isinstance(triangles_color,list) and len(triangles_color) != 8 :
	print "Error triangles_color argument:\nYou must give an list from 8 Color objects.\nOne Color object per face."
	quit()
      
      elif isinstance(triangles_color,list) and len(triangles_color) == 8 :
        tmp=[]
        triangles_color_index=0
        while triangles_color_index < 8 :
	  if type(triangles_color[triangles_color_index].a) == bool :
	    triangles_color[triangles_color_index].a=0
	  triangles_color_index += 1    
      
      elif isinstance(triangles_color,Color) :
	if type(triangles_color.a) == bool :
	    triangles_color.a=0
      
      else :
        raise TypeError(Color)
      
      self.triangles_color=triangles_color  
    
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
    self.triangles,self.quads=generate_polyhedron_26_faces(side_length)
    self.ls=Localview()
  
  def __doc__(self) :
    ''' Print documentation '''
    
    print '''
    Generate an 26hedron object with position updating, 
    display and settings setters methods.
    
    The display mode set how the 26hedron will be display 
    and can take as values:
    "lined" -> Only the edges will be display.
    "faces" -> Only the faces willbbe display.
    "twice" -> The edges and the faces will be display.
    
    The lines color must be an object from <type 'Color'> available throught
    this module as datatype dealing with colors as unsigned bytes 
    or floating-points values.
    
    The quads_color color can be:
    -> An object from <type 'Color'> in which case the 26hedron quads 
       will be filled with this color.
    -> Or an 18-items-list from <type 'Color'> objects.
       1 items per quad.
       
    The triangles_color color can be:
    -> An object from <type 'Color'> in which case the 26hedron triangles 
       will be filled with this color.
    -> Or an 8-items-list from <type 'Color'> objects.
       1 items per hexagon.
    
    The lines width must be an integer representing the number of pixels from 
    the edges width.
    
    The display_ls argument must be an boolean value point to if the polyhedron 
    own Localview will be displayed. 
    The datatype Localview is available throught this module. 
    sea his documentation to know more about.
    
    '''      


