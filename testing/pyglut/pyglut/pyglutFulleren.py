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

from polyhedrons_generators import generate_fulleren






class Fulleren(object) :
  def __init__(self,side_length,display_mode="lined",lines_color=False,pentagons_color=False,hexagons_color=False,lines_width=1,display_ls=False) :
    ''' generate an cube object with the given side length settings.
    
        display_mode    = "lined" -> only the lines will be displayed.
        display_mode    = "faced" -> only the faces will be displayed.
        display_mode    = "twice" -> The lines and the faces will be displayed.
        lines_color     = an objet <type 'Color'> representing the lines color.
        pentagons_color = an objet <type 'Color'> representing the pentagons color.
                          an 12-items-list contains <type 'Color'> objects.  
        hexagons_color  = an objet <type 'Color'> representing the hexagons color.
                          an 20-items-list contains <type 'Color'> objects. 
        line_width      = an integer representing the lines width.
    '''
    
    if not isinstance(side_length,int) and not isinstance(side_length,float) :
      raise TypeError(int,float)
    elif side_length <= 0.0 :
      raise ValueError("Value of side_length must be greater than 0.0") 
    
    if display_mode == "lined" or display_mode == "faced" or display_mode == "twice" :
      self.display_mode=display_mode
    else :
      raise ValueError("lined","faced","twice")
    
    if lines_color :
      if not isinstance(lines_color,Color) :
        raise TypeError(lines_color,Color)
      
    
    if pentagons_color :
      if not isinstance(pentagons_color,Color) and not isinstance(pentagons_color,list) :
        raise TypeError(pentagons_color,Color,list)
      elif isinstance(pentagons_color,list) and len(pentagons_color) != 12 :
	print "Error pentagons_color argument:\nYou must give an list from 12 Color objects.\nOne Color object per face."
	quit()
      elif isinstance(pentagons_color,list) and len(pentagons_color) == 12 :
        tmp=[]
        pentagons_color_index=0
        while pentagons_color_index < 12 :
	  if type(pentagons_color[pentagons_color_index].a) == bool :
	    pentagons_color[pentagons_color_index].a=0
	  pentagons_color_index += 1
      
    if hexagons_color :
      if not isinstance(hexagons_color,Color) and not isinstance(hexagons_color,list) :
        raise TypeError(hexagons_color,Color,list)
      elif isinstance(hexagons_color,list) and len(hexagons_color) != 20 :
	print "Error hexagons_color argument:\nYou must give an list from 20 Color objects.\nOne Color object per face."
	quit()
      elif isinstance(hexagons_color,list) and len(hexagons_color) == 20 :
        tmp=[]
        hexagons_color_index=0
        while hexagons_color_index < 20 :
	  if type(hexagons_color[hexagons_color_index].a) == bool :
	    hexagons_color[hexagons_color_index].a=0
	  hexagons_color_index += 1    
        
    
    if not isinstance(lines_width,int) :
      raise TypeError(lines_width,int)
    elif lines_width < 1 :
      raise ValueError(lines_width,"Lines width value too little.") 
    
    if isinstance(lines_color,Color) :
      if type(lines_color.a) == bool :
        lines_color.a=0
    
    if isinstance(pentagons_color,Color) :
      if type(pentagons_color.a) == bool :
	pentagons_color.a=0
	
    if isinstance(hexagons_color,Color) :
      if type(hexagons_color.a) == bool :
	hexagons_color.a=0 	
    
    if isinstance(display_ls,bool) :
      self.display_ls=display_ls
    
    self.side_length=side_length
    self.lines_color=lines_color
    self.pentagons_color=pentagons_color
    self.hexagons_color=hexagons_color
    self.lines_width=lines_width
    self.hexagons,self.pentagons=generate_fulleren(side_length)
    self.ls=Localview()
    
    self.center=Vertex(0.0,0.0,0.0)    
    
  def update_pos(self,matrix) :
    ''' Apply changing contains in the matrix argument. '''
    
    if not isinstance(matrix, Matrix) :
      raise TypeError(matrix,Matrix)
    
    center=[]
    tmp_pentagons=[]
    for polygon in self.pentagons :
      # Loop over every pentagon from the polyhedron. 
      tmp_polygon=[]
      for lines in polygon :
	tmp_lines=[]
	for vertex in lines :
	  # Loop over every vertice from the polygon.
	  res_vertex= matrix * vertex # Multiply the current vertice with the matrix
	  
	  # Storing the new position from the vertice.
	  tmp_lines.append(res_vertex)  # For the polyhedron polygon container.
	  center.append(res_vertex)       # For polyhedron center computing.
	  
	tmp_polygon.append(tmp_lines)  
      tmp_pentagons.append(tmp_polygon)
    
    self.pentagons=tmp_pentagons          # Update the pentagon container with the new postion from every vertice.
    
    tmp_hexagons=[]
    for polygon in self.hexagons :
      # Loop over every hexagon from the polyhedron. 
      tmp_polygon=[]
      for lines in polygon :
	tmp_lines=[]
	for vertex in lines :
	  # Loop over every vertice from the polygon.
	
	  res_vertex= matrix * vertex # Multiply the current vertice with the matrix
	  
	  # Storing the new position from the vertice.
	  tmp_lines.append(res_vertex)  # For the polyhedron polygon container.
	  center.append(res_vertex)       # For polyhedron center computing.
	
	tmp_polygon.append(tmp_lines)  
      tmp_hexagons.append(tmp_polygon)
    
    self.hexagons=tmp_hexagons            # Update the hexagon container with the new postion from every vertice.
    
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
    
    
      for polygon in self.hexagons :
	# Loop over every hexagon from the polyhedron. 
	# For only lines displaying.
        glBegin(GL_POLYGON)
        for lines in polygon :
	  for v in lines :
	    # We loop over the every vertice from the polygon.
	    glVertex3fv(v.get_vertex())
        glEnd()	
      
    
    elif self.display_mode == "faced" :
      # Configuration of polygons faces displaying.
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
      if self.pentagons_color and isinstance(self.pentagons_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.pentagons_color.get_ubyte_v())
      
      
	
      pentagons_color_index=0  # Iterator, case there are more than one color for the faces displaying.	
	
      if self.pentagons_color and isinstance(self.pentagons_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.pentagons_color.get_ubyte_v())
      
      for polygon in self.pentagons :
	# Loop over every pentagon from the polyhedron. 
	if self.pentagons_color and isinstance(self.pentagons_color,list) : 
	  # Case there are more than one color for the faces displaying.
	  glColor4ubv(self.pentagons_color[pentagons_color_index].get_ubyte_v())
	  
	glBegin(GL_POLYGON)
	for lines in polygon :
	  for v in lines :
	    # We loop over the every vertice from the polygon.
	    glVertex3fv(v.get_vertex())
	glEnd()	
    
	pentagons_color_index += 1
      
      if self.hexagons_color and isinstance(self.hexagons_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.hexagons_color.get_ubyte_v())
	
      hexagons_color_index=0  # Iterator, case there are more than one color for the faces displaying. 	
	
      for polygon in self.hexagons :
	# Loop over every hexagon from the polyhedron. 
	if self.hexagons_color and isinstance(self.hexagons_color,list) : 
	  # Case there are more than one color for the faces displaying.
	  glColor4ubv(self.hexagons_color[hexagons_color_index].get_ubyte_v())
	  
	glBegin(GL_POLYGON)
	for lines in polygon :
	  for v in lines :
	    # We loop over the every vertice from the polygon.
	    glVertex3fv(v.get_vertex())
	glEnd()
	hexagons_color_index += 1
      
    elif self.display_mode == "twice" :
      # Configuration of polygons faces displaying.
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
      if self.pentagons_color and isinstance(self.pentagons_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.pentagons_color.get_ubyte_v())
      
      
	
      pentagons_color_index=0	
      for polygon in self.pentagons :
	# Loop over every pentagon from the polyhedron. 
	if self.pentagons_color and isinstance(self.pentagons_color,list) : 
	  # Case there are more than one color for the faces displaying.
	  glColor4ubv(self.pentagons_color[pentagons_color_index].get_ubyte_v())
	  
	glBegin(GL_POLYGON)
	for lines in polygon :
	  for v in lines :
	    # We loop over the every vertice from the polygon.
	    glVertex3fv(v.get_vertex())
	glEnd()	
    
	pentagons_color_index += 1
      
      if self.hexagons_color and isinstance(self.hexagons_color,Color) :
	# Case one same color for the faces displaying.
	glColor4ubv(self.hexagons_color.get_ubyte_v())
	
      hexagons_color_index=0  # Iterator, case there are more than one color for the faces displaying.	
	
      for polygon in self.hexagons :
	# Loop over every hexagon from the polyhedron. 
	if self.hexagons_color and isinstance(self.hexagons_color,list) :
	  # Case there are more than one color for the faces displaying.
	  glColor4ubv(self.hexagons_color[hexagons_color_index].get_ubyte_v())
	  
	glBegin(GL_POLYGON)
	for lines in polygon :
	  for v in lines :
	    # We loop over the every vertice from the polygon.
	    glVertex3fv(v.get_vertex())
	glEnd()
	
	hexagons_color_index += 1
      
      # Configuration of polygons lines displaying.
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
      
      if self.lines_color :
	# Lines color configuration. 
	glColor4ubv(self.lines_color.get_ubyte_v())
      
      glLineWidth(self.lines_width)
    
    
      for polygon in self.hexagons :
	# Loop over every hexagon from the polyhedron.
	# For only lines displaying.
        glBegin(GL_POLYGON)
        for lines in polygon :
	  for v in lines :
	    # We loop over the every vertice from the polygon.
	    glVertex3fv(v.get_vertex())
        glEnd()	
      
    if self.display_ls :
      # Displaying the Localview.
      self.ls.display(self.side_length*4.0/10.0)
      
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
    
  def set_pentagons_color(self,pentagons_color) :
    ''' Change the faces color(s) from the polyhedron.
        Value of argument faces_color should be:
        faces_color  = An objet <type 'Color'> representing the pentagons faces color.
                       An 12-items-list from object <type 'Color'>.
                       One item per pentagon face. 
    '''
    
    if pentagons_color :
      
      if not isinstance(pentagons_color,Color) and not isinstance(pentagons_color,list) :
        raise TypeError(pentagons_color,Color,list)
      
      elif isinstance(pentagons_color,list) and len(pentagons_color) != 12 :
	print "Error pentagons_color argument:\nYou must give an list from 12 Color objects.\nOne Color object per face."
	quit()
	
      elif isinstance(pentagons_color,list) and len(pentagons_color) == 12 :
        tmp=[]
        pentagons_color_index=0
        while pentagons_color_index < 12 :
	  if type(pentagons_color[pentagons_color_index].a) == bool :
	    pentagons_color[pentagons_color_index].a=0
	  pentagons_color_index += 1
    
      elif isinstance(pentagons_color,Color) :
	if type(pentagons_color.a) == bool :
	    pentagons_color.a=0	  
      
      else :
	raise TypeError(Color)
      
      self.pentagons_color=pentagons_color
    
  def set_hexagons_color(self,hexagons_color) :
    ''' Change the faces color(s) from the polyhedron.
        Value of argument faces_color should be:
        faces_color  = An objet <type 'Color'> representing the hexagons faces color.
                       An 20-items-list from object <type 'Color'>.
                       One item per hexagons face. 
    '''
    
    if hexagons_color :
      
      if not isinstance(hexagons_color,Color) and not isinstance(hexagons_color,list) :
        raise TypeError(hexagons_color,Color,list)
      
      elif isinstance(hexagons_color,list) and len(hexagons_color) != 20 :
	print "Error hexagons_color argument:\nYou must give an list from 20 Color objects.\nOne Color object per face."
	quit()
      
      elif isinstance(hexagons_color,list) and len(hexagons_color) == 20 :
        tmp=[]
        hexagons_color_index=0
        while hexagons_color_index < 20 :
	  if type(hexagons_color[hexagons_color_index].a) == bool :
	    hexagons_color[hexagons_color_index].a=0
	  hexagons_color_index += 1    
      
      elif isinstance(hexagons_color,Color) :
	if type(hexagons_color.a) == bool :
	    hexagons_color.a=0	  
      
      else :
	raise TypeError(Color)
      
      self.hexagons_color=hexagons_color  
    
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
    self.hexagons,self.pentagons=generate_fulleren(side_length) 
    self.ls=Localview()
  
  def __doc__(self) :
    ''' Print documentation '''
    
    print '''
    Generate an fulleren object with position updating, 
    display and settings setters methods.
    
    The display mode set how the fulleren will be display 
    and can take as values:
    "lined" -> Only the edges will be display.
    "faces" -> Only the faces willbbe display.
    "twice" -> The edges and the faces will be display.
    
    The lines color must be an object from <type 'Color'> available throught
    this module as datatype dealing with colors as unsigned bytes 
    or floating-points values.
    
    The pentagons_color color can be:
    -> An object from <type 'Color'> in which case the fulleren pentagons 
       will be filled with this color.
    -> Or an 12-items-list from <type 'Color'> objects.
       1 item per pentagon.
       
    The hexagons_color color can be:
    -> An object from <type 'Color'> in which case the fulleren hexagons 
       will be filled with this color.
    -> Or an 20-items-list from <type 'Color'> objects.
       1 item per hexagon.
    
    The lines width must be an integer representing the number of pixels from 
    the edges width.
    
    The display_ls argument must be an boolean value point to if the polyhedron 
    own Localview will be displayed. 
    The datatype Localview is available throught this module. 
    sea his documentation to know more about.
    
    '''      