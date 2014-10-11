#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################
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
from distutils.core import Extension, setup

with open("README.rst",'r') as file :
  long_description = file.read()

MODULE_NAME="pyglut"

setup(name=MODULE_NAME,version='1.0.0',
      url='https://github.com/mrcyberfighter/pyglut',
      author="Eddie Bruggemann",author_email="mrcyberfighter@gmail.com",
      maintainer="Eddie Bruggemann",maintainer_email="mrcyberfighter@gmail.com",
      long_description=long_description,
      description="pyglut an pyopengl utilities module with severals 3D programming helper classes and functions utilities.This module implement low-levels forms generating, utils, datatypes and predefine 3D objects.",
      
      packages=['pyglut'],
      package_dir={'pyglut': './pyglut'},
      package_data={'pyglut':["*.py",]},
      data_files=[('pyglut/Examples',
		   ['Examples/example_26hedron.py',
                    'Examples/example_32hedron.py', 
                    'Examples/example_cube.py',
                    'Examples/example_dodecahedron.py',
                    'Examples/example_fulleren.py',
                    'Examples/example_icosahedron.py',
                    'Examples/example_octahedron.py',
                    'Examples/example_quad_sphere.py',
                    'Examples/example_tetrahedron.py',
                    'Examples/example_toros.py',
                    'Examples/example_trigon_sphere.py']),
		   
                  ("pyglut/License",
		   ["License/gpl.txt"]),
		  
		  ("pyglut/README",
                   ["README/README.rst"]),
                  ("pyglut/Documentation",["Documentation/pyglut_documentation.zip"] 
                   )],
		  
      platforms=["Linux","Windows"],license="GPLv3")