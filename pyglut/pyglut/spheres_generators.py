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


from datatype_vertex import Vertex

from primary_operations import rotate_y

from polygons_generators import generate_polygon_on_xy_radius

def generate_quad_sphere(basis,radius) :
  ''' Generate an quads sphere and return an tuple from 2 arrays: 
      (lined displaying vertices sequence list, surface displaying vertices sequence list).
      In relationship with the base for the sphere generating:  faces count = basis * basis
      and the given sphere radius.
  '''

  if not isinstance(basis,int) :
    raise TypeError(int)

  if basis < 6 or basis % 2 :
    print "the basis for the sphere must be greater as 5 and basis % 2 == 0 "
    quit()

  if not isinstance(radius,int) and not isinstance(radius,float) :
    raise TypeError(int,float)


  # We generate the base polygon for the sphere generating with the given radius:
  polygon_1=generate_polygon_on_xy_radius(basis,radius,Vertex(0.0,0.0,0.0),0)

  polygons=[]        # Container for the polygons.

  i=2                # The iterator variable is initialise with the value 2
                     # because this one is used for string formating and the polygon_1 variable exist.

  while i <= basis :
    # Generate from empty lists by execution, with the directive exec(),
    # from formattted strings.
    # Instead of defining variables because the number of polygons is relativ to the basis argument value.
    exec("polygon_{0}=[]".format(i))
    exec("polygons.append(polygon_{0})".format(i))
    i += 1

  for v in polygon_1 :
    # Iteration over every vertice from our base polygon.
    i=0
    angle=360.0/basis  # Computing of the degress between 2 polygons on the XZ surface.
    while i < len(polygons) :
      # generating of all polygons containing the vertices from the sphere.
      polygons[i].append(rotate_y(v,angle))
      i += 1
      angle += 360./basis

  polygons_array=[]  # temporary container variable definition.

  i=1                # The iterator variable is initialise with the value 1
                     # because this one is used for string formating.
  while i <= basis :
    # Filling from the temporary container variable
    # with the computed polygons containing the vertice from our sphere.
    # Which we gonna need to compute the quads from composing the sphere .
    exec("polygons_array.append(polygon_{0})".format(i))
    i += 1


  i=0
  tmp_1=[]

  while i < len(polygons_array) :
    # Iteration over the temporary polygon container variable to compute the quads.
    ii=0
    tmp_2=[]
    while ii < basis-1 :
      # We compute the quads: from the polygons list to an quads list.
      if not i == basis-1 :
        tmp_2.append(polygons_array[i][ii])
        tmp_2.append(polygons_array[i+1][ii])
        tmp_2.append(polygons_array[i+1][ii+1])
        tmp_2.append(polygons_array[i][ii+1])
      else :
        tmp_2.append(polygons_array[i][ii])
        tmp_2.append(polygons_array[0][ii])
        tmp_2.append(polygons_array[0][ii+1])
        tmp_2.append(polygons_array[i][ii+1])

      ii += 1
      tmp_1.append(tmp_2)
    i += 1

  polygons_line_array=polygons_array  # Affectation of the variable to return for the case of lined sphere displaying.

  polygons_quad_array=tmp_1           # Affectation of the variable to return for the case of surfaces sphere displaying.

  return (polygons_line_array,polygons_quad_array)

def generate_trigon_sphere(basis,radius) :
  ''' Sphere generating function which has for faces triangles and return an tuple from 2 arrays: 
      (lined displaying vertices sequence list, surface displaying vertices sequence list).
      In relationship with the base for the sphere generating:  faces count = basis * basis
      and the given sphere radius.
  '''

  if not isinstance(basis,int) :
    raise TypeError(int)

  if basis < 8 or basis % 4 :
    print "the basis for the sphere miust be greater as 7 and basis % 4 == 0 "
    quit()

  if not isinstance(radius,int) and not isinstance(radius,float) :
    raise TypeError(int,float)


  # We generate the base polygon for the sphere generating with the given radius:
  base_polygon=generate_polygon_on_xy_radius(basis,radius,Vertex(0.0,0.0,0.0),0)

  polygons=[]       # Polygon for trigonized sphere generating container.

  i=0
  angle=360./basis  # Computing of the degress between 2 polygons on the XZ surface.

  while i < basis :
    # Loop generating an quads sphere polygons list.
    tmp=[]
    for v in base_polygon :
      # Iteration over every vertice from the base polygon
      # and compting from the next polygon vertices rotate from
      # the distance between the base polygon and the next polygon.
      tmp.append(rotate_y(v,angle))

    polygons.append(tmp)

    i += 1
    angle += 360./basis  # Distance between the base polygon and the next polygon inctrementing.

  boolean=False
  tmp_1=[]
  i=0

  while i < len(polygons) :
    # Iteration over the quads sphere polygons
    # to compute the polygons on the XZ surface with an alternativ offset.
    ii=0
    tmp_2=[]
    while ii < len(polygons[0]) :

      if boolean :
        tmp_2.append(rotate_y(polygons[ii][i],360./basis/2.))
      else :
        tmp_2.append(polygons[ii][i])

      ii += 1

    if boolean :
      boolean=False
    else :
      boolean=True

    i += 1
    tmp_1.append(tmp_2)



  tmp_2=tmp_1
  i=-1
  polygons_trigons_array=[]
  boolean=False

  while i < len(tmp_2)-1 :
    # Loop to compute the triangles from our sphere.
    # Throught iterating over the polygons on the XZ surface.
    ii=-1
    while ii < len(tmp_2[i])-1 :
      tmp=[]

      if boolean :
        tmp.append(tmp_2[i][ii])
        tmp.append(tmp_2[i][ii+1])
        tmp.append(tmp_2[i+1][ii])
      else :
        tmp.append(tmp_2[i][ii])
        tmp.append(tmp_2[i][ii+1])
        tmp.append(tmp_2[i+1][ii+1])

      polygons_trigons_array.append(tmp)

      ii += 1

    if boolean :
      boolean=False
    else :
      boolean=True

    i += 1
  
  polygon_vertice_array=tmp_1
  
  # Return an polygon array building an sphere and an array of triangles composing our trigon sphere.
  return (polygon_vertice_array,polygons_trigons_array)