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

class Vertex(object) :
  def __init__(self,x=False,y=False,z=False,vertexv=False) :
    ''' Object from type Vertex representing an vertice '''
    if vertexv :
      # The coordinates component are given in an vector.
      self.wx=vertexv[0]
      self.wy=vertexv[1]
      self.wz=vertexv[2]
    else :
      # The coordinates component are given individually. 
      self.wx=x
      self.wy=y
      self.wz=z

  def get_vertex(self) :
    return (self.wx,self.wy,self.wz)      