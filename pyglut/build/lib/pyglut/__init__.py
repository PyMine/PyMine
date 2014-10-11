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


# Import Plato polyhedrons objects.
from pyglutTetrahedron import Tetrahedron 
from pyglutCube import Cube
from pyglutOctahedron import Octahedron
from pyglutDodecahedron import Dodecahedron
from pyglutIcosahedron import Icosahedron  

# Import the others polyhedrons objects.
from pyglut26hedron import Poly26Hedron
from pyglut32hedron import Poly32Hedron

# Import the Fulleren polyhedron object.
from pyglutFulleren import Fulleren

# Import the Toros object. 
from pyglutToros import Toros 

# Import the spheres polyhedron objects. 
from pyglutSpheres import Trigon_Sphere, Quad_Sphere 


from datatype_color import Color

from datatype_localview import Localview

from datatype_matrix import Matrix

from datatype_vector import Vector 

from datatype_vertex import Vertex 

from center_utils import get_middle_from_segment, get_center_from_polyhedron
from length_utils import get_distance_vertices, get_perimeter_from_polygon, get_perimeter_from_polyhedron
from rotation_utils import rotate_on_xy, rotate_on_xz, rotate_on_yz

from divide_segment import div_segment_into_vertices

from primary_operations import translate, scale, rotate_x, rotate_y, rotate_z

from polygons_generators import generate_polygon_on_xy_radius, generate_polygon_on_xz_radius, generate_polygon_on_yz_radius
from polygons_generators import generate_polygon_on_xy_side_length, generate_polygon_on_xz_side_length, generate_polygon_on_yz_side_length

from polyhedrons_generators import generate_tetrahedron, generate_cube, generate_octahedron, generate_dodecahedron, generate_icosahedron
from polyhedrons_generators import generate_fulleren, generate_polyhedron_26_faces, generate_polyhedron_32_faces

from spheres_generators import generate_quad_sphere, generate_trigon_sphere

# Delete the primary operations source file reference.
del(primary_operations)

# Delete the references to the used datatypes by the polyhedrons objects, sources files references. 
del(datatype_color)
del(datatype_localview)
del(datatype_matrix)
del(datatype_vector)
del(datatype_vertex)

# Delete the references to the utils used by the polyhedrons object, source files references. 
del(divide_segment)
del(center_utils)
del(length_utils)
del(rotation_utils)

# Delete the forms generators sources files references.
del(polygons_generators)
del(polyhedrons_generators)
del(spheres_generators)


# Delete the reference to the Plato polyhedron source files references.
del(pyglutCube)
del(pyglutTetrahedron)
del(pyglutOctahedron)
del(pyglutDodecahedron)
del(pyglutIcosahedron)

# Delete the reference to the others polyhedron source files references.
del(pyglut26hedron)
del(pyglut32hedron)

# Delete the reference to the fulleren polyhedron source file reference.
del(pyglutFulleren)

# Delete the reference to the toros polyhedron source file reference.
del(pyglutToros)

# Delete the reference to the spheres polyhedron source file reference.
del(pyglutSpheres)
































