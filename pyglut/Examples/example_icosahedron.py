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
  
from time import sleep  

from random import uniform,randint
  
from OpenGL.GL import *
from OpenGL.GLU import *

try :
  import pygame
  from pygame.locals import *
except :
  print "pygame module needed !!!\nPlease install pygame and try to run the script again."
  quit()




from pyglut import Icosahedron 

from pyglut import Color 
from pyglut import Matrix
  
def print_msg() :
  print "Press the 'm' key to switch into the display modes."
  print "Press the 'l' key to change the lines color."
  print "Press the 'f' key to change the faces color."
  print "Press the UP ARROW to increment the lines size."
  print "Press the DOWN ARROW to decrement the lines size."
  print "Press the 'd' key to display | hidden the Localview."
  print "Press the 's' key to change the polyhedron size."   
  
def resizeGL(width,height) :
  fov_angle=60.0                   # Angle of eye view.
  z_near=2.0                       # Distance from the user from the screen.
  z_far=1000.0                     # Distance in depth.

  glMatrixMode(GL_PROJECTION)      # Enable Projection matrix configuration.  
  glLoadIdentity()          
  gluPerspective( fov_angle, 
                  float(width)/float(height),
                  z_near, 
                  z_far )
                    
  glLoadIdentity()
  glOrtho( -30.0,                   # Left coordinates value.   ( x_min ) 
            30.0,                   # Right coordinates value.  ( x_max ) 
           -30.0,                   # Bottom coordinates value. ( y_min )
            30.0,                   # Top coordinates value.    ( y_max )  
           -30.0,                   # Near coordinates value.   ( z_min ) 
            30.0)                   # Far coordinates value.    ( z_max )  
            
  glMatrixMode(GL_MODELVIEW)       # Enable modelview matrix as current matrix.   
  
def initGL(width,height) :

  glClearColor(0.0, 0.0, 0.0, 0.0) # Define clear color [0.0-1.0]

  glEnable(GL_DEPTH_TEST)          # Enable GL depth functions. 

  glShadeModel(GL_FLAT)            # Define lines as polygon instead of full polygon: GL_SMOOTH. 

  resizeGL(width,height)           # Call to the resize function.



def mainloop() :
  ''' Display function '''
  
  line_width=5
  bool_display_ls=True
  display_mode=0
  
  faces_color_mode=1
  
  color_faces=[]
  for v in range(0,20) :
    color_faces.append(Color(ub_v=(randint(63,255),randint(63,255),randint(63,255))))
  
  test_icosahedron=Icosahedron(12.5,display_mode="lined",lines_color=Color(ub_v=(127,127,127,0)),faces_color=color_faces,lines_width=line_width,display_ls=True)
  i=5.625/4.0
  m=Matrix()
  m.translate((15.5,0.0,0.0))
  test_icosahedron.update_pos(m)
  while True :
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    
    m=Matrix()
    m.translate((-test_icosahedron.center.wx,-test_icosahedron.center.wy,-test_icosahedron.center.wz))
    m.rotate_x(i)
    m.rotate_y(i)
    m.rotate_z(i)
    m.translate((test_icosahedron.center.wx,test_icosahedron.center.wy,test_icosahedron.center.wz))
    m.rotate_y(i)
    test_icosahedron.update_pos(m)
    test_icosahedron.display()
    
    for event in pygame.event.get() :
      ''' So we can catch user-interaction events in the mainloop. ''' 
      
      
      if event.type == QUIT      :         # The user close the window. 
        quit()
    
      elif event.type == KEYDOWN :         # The user press a keyboard key. 
        
        if event.key == K_m  or event.key == K_SEMICOLON :
	  display_mode += 1
	  if display_mode == 1 :
	    test_icosahedron.set_display_mode("faced")
	  elif display_mode == 2 :
	    test_icosahedron.set_display_mode("twice")  
	  elif display_mode == 3 :
	    display_mode=0
	    test_icosahedron.set_display_mode("lined")
	    
	  
	elif event.key == K_l :
	  test_icosahedron.set_lines_color(Color(ub_v=(randint(63,255),randint(63,255),randint(63,255))))
	  
	elif event.key == K_f :
	  if faces_color_mode == 1 :
	    test_icosahedron.set_faces_color(Color(ub_v=(randint(63,255),randint(63,255),randint(63,255))))
	    faces_color_mode=0
	  elif faces_color_mode == 0 :
	    color_faces=[]
            for v in range(0,20) :
              color_faces.append(Color(ub_v=(randint(63,255),randint(63,255),randint(63,255))))
	    test_icosahedron.set_faces_color(color_faces) 
	    faces_color_mode=1
	    
	elif event.key == K_UP :
	  line_width += 1
	  
	  test_icosahedron.set_lines_width(line_width)
	
	elif event.key == K_DOWN :
	  line_width -= 1
	  if line_width < 1 :
	    line_width=1
	  
	  test_icosahedron.set_lines_width(line_width)  
	
	elif event.key == K_d :
	  if bool_display_ls :
	    bool_display_ls=False
	  else :
	    bool_display_ls=True
	    
	  test_icosahedron.set_display_ls(bool_display_ls)
	
	elif event.key == K_s :
	  test_icosahedron.set_side_length(uniform(1.0,15.5))
	  m=Matrix()
          m.translate((15.5,0.0,0.0))
          test_icosahedron.update_pos(m)
	  
        
    
   
    
    pygame.display.flip()    
    sleep(0.0001)  

def main() :
  global screen,width,height
  width=1024.0
  height=768.0
    
  pygame.init()                                                         # We initialise the pygame module. 
        
  screen=pygame.display.set_mode((int(width),int(height)),              # We set the window width and height
                                  HWSURFACE | OPENGL | DOUBLEBUF,       # We set flags.
                                  24)                                   # Indicator colors are coded on 24 bits.
                                  
    
  initGL(width,height)                                                  # Call to initialise function.
  
  mainloop()                                                            # We call our display function: mainloop. 
  
if __name__ == "__main__" :
  
  print_msg()
  main()    