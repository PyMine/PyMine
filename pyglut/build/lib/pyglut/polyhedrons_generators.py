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

from math import sqrt

from datatype_vertex import Vertex

from primary_operations import translate, rotate_x, rotate_y, rotate_z

from center_utils import  get_center_from_polygon, get_middle_from_segment

from length_utils import get_distance_vertices 

from divide_segment import div_segment_into_vertices

from polygons_generators import generate_polygon_on_xy_radius, generate_polygon_on_xz_radius, generate_polygon_on_yz_radius

from polygons_generators import generate_polygon_on_xy_side_length, generate_polygon_on_xz_side_length, generate_polygon_on_yz_side_length  
  


def generate_tetrahedron(side_length) :
  ''' Generate an tetrahedron in relationship to the given side length.
      And return an sequence from triangles composing the tetrahedron.
  '''    
  
  # Compute cube side length to get the diagonale length egal to the given argument,
  # so that the inscribe tetrahedron have the correct side length.
  side_length=sqrt(pow(side_length,2)+pow(side_length,2)) / 2.
  
  # Generate the cube where the tetrahedron is inscribe.
  vertex_list=[  # We begin with the back side.
                  Vertex(-side_length/2., -side_length/2., -side_length/2.), 
                  Vertex( side_length/2., -side_length/2., -side_length/2.), 
                  Vertex( side_length/2.,  side_length/2., -side_length/2.), 
                  Vertex(-side_length/2.,  side_length/2., -side_length/2.),
                  # Then with the front side.
                  Vertex(-side_length/2., -side_length/2.,  side_length/2.), 
                  Vertex( side_length/2., -side_length/2.,  side_length/2.), 
                  Vertex( side_length/2.,  side_length/2.,  side_length/2.), 
                  Vertex(-side_length/2.,  side_length/2.,  side_length/2.)
                ]
  
  # Define the 4 triangles composing the tetrahedron: 
  tetrahedron_triangle_1=(vertex_list[6],vertex_list[3],vertex_list[4])
  tetrahedron_triangle_2=(vertex_list[6],vertex_list[3],vertex_list[1])
  tetrahedron_triangle_3=(vertex_list[4],vertex_list[1],vertex_list[3])
  tetrahedron_triangle_4=(vertex_list[4],vertex_list[1],vertex_list[6])
  
  # Assemble triangles to an tetrahedron:
  tetrahedron=(tetrahedron_triangle_1,tetrahedron_triangle_2,tetrahedron_triangle_3,tetrahedron_triangle_4)
  
  return tetrahedron

def generate_cube(side_length) :
  ''' Generate an cube in relationship to the given side length. 
      And return an sequence from quads composing the cube.
  '''
  
  cube_vertex_list=[  # We begin with the back side.
                      Vertex(-side_length/2.,  side_length/2.,  side_length/2.), 
                      Vertex( side_length/2.,  side_length/2.,  side_length/2.), 
                      Vertex( side_length/2., -side_length/2.,  side_length/2.), 
                      Vertex(-side_length/2., -side_length/2.,  side_length/2.),
                      # Then with the front side.
                      Vertex(-side_length/2.,  side_length/2., -side_length/2.), 
                      Vertex( side_length/2.,  side_length/2., -side_length/2.), 
                      Vertex( side_length/2., -side_length/2., -side_length/2.), 
                      Vertex(-side_length/2., -side_length/2., -side_length/2.)
                    ]
  
  front = [cube_vertex_list[4],cube_vertex_list[5],cube_vertex_list[6],cube_vertex_list[7]] # Front QUADS.
  back  = [cube_vertex_list[0],cube_vertex_list[1],cube_vertex_list[2],cube_vertex_list[3]] # Back QUADS.

  left  = [cube_vertex_list[0],cube_vertex_list[4],cube_vertex_list[7],cube_vertex_list[3]] # Left QUADS.
  right = [cube_vertex_list[5],cube_vertex_list[1],cube_vertex_list[2],cube_vertex_list[6]] # right QUADS.

  up    = [cube_vertex_list[0],cube_vertex_list[1],cube_vertex_list[5],cube_vertex_list[4]] # up QUADS.
  down  = [cube_vertex_list[7],cube_vertex_list[6],cube_vertex_list[2],cube_vertex_list[3]] # down QUADS.

  return (front,back,left,right,up,down) 

def generate_octahedron(side_length) :
  ''' Generate an octahedron from the given side length. 
      And return an sequence from triangles composing the octahedron.
  '''
  
  quad_xy=generate_polygon_on_xy_side_length(4,side_length,45)  # Generate an quad on the plan XY.
          # You can use the function: generate_polygon_on_xy_radius(...) instead.
          
  quad_xz=generate_polygon_on_xz_side_length(4,side_length,45)  # Generate an quad on the plan XZ.
         # You can use the function: generate_polygon_on_xz_radius(...) instead.
         
  quad_yz=generate_polygon_on_yz_side_length(4,side_length,45)  # Generate an quad on the plan YZ.
         # You can use the function: generate_polygon_on_yz_radius(...) instead.
         
  return ((quad_xy[0],quad_yz[0],quad_yz[1]),(quad_xy[0],quad_yz[1],quad_yz[2]),(quad_xy[0],quad_yz[2],quad_yz[3]),(quad_xy[0],quad_yz[3],quad_yz[0]),
	  (quad_xy[2],quad_yz[0],quad_yz[1]),(quad_xy[2],quad_yz[1],quad_yz[2]),(quad_xy[2],quad_yz[2],quad_yz[3]),(quad_xy[2],quad_yz[3],quad_yz[0]) 
	  ) # Return 8 triangles sequences who form assembled an octahedron.


def generate_icosahedron(side_length) :
  ''' Generate an icosahedron from the given side length and 
      return an array of 20 triangles component from the icosahedron 
      and his construction base quad set. ''' 
  
  side_lt=side_length                   # Define the littler side of the rectangle.  
  side_gt=side_length*((1+sqrt(5))/2.)  # Compute the length of the greater side with the gold number ( (1+sqrt(5))/2. )
  
  # Define the base quad so that his center is Vertex(0.0, 0.0, 0.0) :
  quad1=[Vertex(-side_lt/2.,-side_gt/2.,0.0),Vertex(side_lt/2.,-side_gt/2.,0.0),Vertex(side_lt/2.,side_gt/2.,0.0),Vertex(-side_lt/2.,side_gt/2.,0.0)]
  
  # Rotate the base quad on the y and z axes from 90°, to obtain the second crossing quad.
  quad2=[rotate_z(rotate_y(quad1[0],90),90), rotate_z(rotate_y(quad1[1],90),90), rotate_z(rotate_y(quad1[2],90),90), rotate_z(rotate_y(quad1[3],90),90)]
  
  # Rotate the base quad on the y and x axes from 90°, to obtain the third crossing quad. 
  quad3=[rotate_x(rotate_y(quad1[0],90),90), rotate_x(rotate_y(quad1[1],90),90), rotate_x(rotate_y(quad1[2],90),90), rotate_x(rotate_y(quad1[3],90),90)]
  
  icosahedron_base_quads=[quad1,quad2,quad3] # We set the bases quads for our polyhedron: an icosahedron.
  
  # Define an array composed of triangles because an icosahedron is composed from 20 equilateral triangles:
  icosahedron_triangle_array=[(icosahedron_base_quads[0][0],icosahedron_base_quads[0][1],icosahedron_base_quads[2][1]),
                              (icosahedron_base_quads[0][1],icosahedron_base_quads[1][0],icosahedron_base_quads[1][1]),
                              (icosahedron_base_quads[0][0],icosahedron_base_quads[0][1],icosahedron_base_quads[2][2]),
                              (icosahedron_base_quads[0][0],icosahedron_base_quads[1][2],icosahedron_base_quads[1][3]),
                              (icosahedron_base_quads[0][0],icosahedron_base_quads[1][3],icosahedron_base_quads[2][1]),
                              (icosahedron_base_quads[0][1],icosahedron_base_quads[2][1],icosahedron_base_quads[1][0]),
                              (icosahedron_base_quads[0][1],icosahedron_base_quads[1][1],icosahedron_base_quads[2][2]),
                              (icosahedron_base_quads[0][0],icosahedron_base_quads[2][2],icosahedron_base_quads[1][2]),
                              (icosahedron_base_quads[0][2],icosahedron_base_quads[0][3],icosahedron_base_quads[2][3]),
                              (icosahedron_base_quads[0][3],icosahedron_base_quads[1][2],icosahedron_base_quads[1][3]),
                              (icosahedron_base_quads[0][2],icosahedron_base_quads[0][3],icosahedron_base_quads[2][0]),
                              (icosahedron_base_quads[0][2],icosahedron_base_quads[1][0],icosahedron_base_quads[1][1]),
                              (icosahedron_base_quads[0][2],icosahedron_base_quads[1][1],icosahedron_base_quads[2][3]),
                              (icosahedron_base_quads[0][3],icosahedron_base_quads[2][3],icosahedron_base_quads[1][2]),
                              (icosahedron_base_quads[0][3],icosahedron_base_quads[1][3],icosahedron_base_quads[2][0]),
                              (icosahedron_base_quads[0][2],icosahedron_base_quads[2][0],icosahedron_base_quads[1][0]),
                              (icosahedron_base_quads[2][0],icosahedron_base_quads[2][1],icosahedron_base_quads[1][3]),
                              (icosahedron_base_quads[2][0],icosahedron_base_quads[2][1],icosahedron_base_quads[1][0]),
                              (icosahedron_base_quads[2][2],icosahedron_base_quads[2][3],icosahedron_base_quads[1][1]),
                              (icosahedron_base_quads[2][2],icosahedron_base_quads[2][3],icosahedron_base_quads[1][2])]
  
  
  # We return the base quad set and the triangle array.
  return [quad1,quad2,quad3],icosahedron_triangle_array 

def generate_dodecahedron(side_length) :
  ''' Generate an dodecahedron in relationship to the argument side_length
      taken as basis for the dodecahedron generation. 
      And return an sequence of pentagons composing the dodecahedron. '''
  
  ####################################################################
  # The commented print directives are set to made the evidence that #
  # the dodecahedron is not regular:                                 #
  # for every pentagon there one only segment length which is not    #
  # equal to the others and i don't know why.                        # 
  # The theorie from the icosahedron face center,                    #
  # issue from the book from Marius Apetri doesn't work like it      #
  # should. Maybe my implementation from the concept.                #
  # If you find an answers thank's to contact me by                  #
  # mail: mrcyberfighter@gmail.com                                   #
  ####################################################################
  
  ico=generate_icosahedron(side_length)[1]
  
  dodecahedron=[]  # Define the pentagones contains array container.
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[0]))
  pentagone.append(get_center_from_polygon(ico[5]))
  pentagone.append(get_center_from_polygon(ico[1]))
  pentagone.append(get_center_from_polygon(ico[6]))
  pentagone.append(get_center_from_polygon(ico[2]))
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "1"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[0]),get_center_from_polygon(ico[5]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[5]),get_center_from_polygon(ico[1]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[1]),get_center_from_polygon(ico[6]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[6]),get_center_from_polygon(ico[2]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[0]),get_center_from_polygon(ico[2]))

  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[9]))
  pentagone.append(get_center_from_polygon(ico[3]))
  pentagone.append(get_center_from_polygon(ico[7]))
  pentagone.append(get_center_from_polygon(ico[19]))
  pentagone.append(get_center_from_polygon(ico[13]))
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "2"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[9]),get_center_from_polygon(ico[3]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[3]),get_center_from_polygon(ico[7]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[7]),get_center_from_polygon(ico[19]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[19]),get_center_from_polygon(ico[13]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[13]),get_center_from_polygon(ico[9]))
  
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[9])) 
  pentagone.append(get_center_from_polygon(ico[14])) 
  pentagone.append(get_center_from_polygon(ico[16])) 
  pentagone.append(get_center_from_polygon(ico[4]))
  pentagone.append(get_center_from_polygon(ico[3]))
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "3"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[9]),get_center_from_polygon(ico[14]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[14]),get_center_from_polygon(ico[16]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[16]),get_center_from_polygon(ico[4]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[4]),get_center_from_polygon(ico[3]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[3]),get_center_from_polygon(ico[9]))
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[0])) 
  pentagone.append(get_center_from_polygon(ico[2]))
  pentagone.append(get_center_from_polygon(ico[7]))
  pentagone.append(get_center_from_polygon(ico[3]))
  pentagone.append(get_center_from_polygon(ico[4]))
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "4"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[0]),get_center_from_polygon(ico[2]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[2]),get_center_from_polygon(ico[7]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[7]),get_center_from_polygon(ico[3]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[3]),get_center_from_polygon(ico[4]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[4]),get_center_from_polygon(ico[0]))
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[5])) 
  pentagone.append(get_center_from_polygon(ico[0]))
  pentagone.append(get_center_from_polygon(ico[4]))
  pentagone.append(get_center_from_polygon(ico[16]))
  pentagone.append(get_center_from_polygon(ico[17])) 
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "5"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[5]),get_center_from_polygon(ico[0]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[0]),get_center_from_polygon(ico[4]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[4]),get_center_from_polygon(ico[16]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[16]),get_center_from_polygon(ico[17]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[17]),get_center_from_polygon(ico[5]))
  
  pentagone=[]  # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[17])) 
  pentagone.append(get_center_from_polygon(ico[5]))
  pentagone.append(get_center_from_polygon(ico[1]))
  pentagone.append(get_center_from_polygon(ico[11]))
  pentagone.append(get_center_from_polygon(ico[15])) 
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "6"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[17]),get_center_from_polygon(ico[5]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[5]),get_center_from_polygon(ico[1]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[1]),get_center_from_polygon(ico[11]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[11]),get_center_from_polygon(ico[15]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[15]),get_center_from_polygon(ico[17]))
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[15])) 
  pentagone.append(get_center_from_polygon(ico[17]))
  pentagone.append(get_center_from_polygon(ico[16]))
  pentagone.append(get_center_from_polygon(ico[14]))
  pentagone.append(get_center_from_polygon(ico[10])) 
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "7"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[15]),get_center_from_polygon(ico[17]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[17]),get_center_from_polygon(ico[16]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[16]),get_center_from_polygon(ico[14]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[14]),get_center_from_polygon(ico[10]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[15]),get_center_from_polygon(ico[10]))
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[10])) 
  pentagone.append(get_center_from_polygon(ico[14]))
  pentagone.append(get_center_from_polygon(ico[9]))
  pentagone.append(get_center_from_polygon(ico[13]))
  pentagone.append(get_center_from_polygon(ico[8])) 
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "8"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[10]),get_center_from_polygon(ico[14]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[14]),get_center_from_polygon(ico[9]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[9]),get_center_from_polygon(ico[13]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[13]),get_center_from_polygon(ico[8]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[8]),get_center_from_polygon(ico[10]))
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[8])) 
  pentagone.append(get_center_from_polygon(ico[10]))
  pentagone.append(get_center_from_polygon(ico[15]))
  pentagone.append(get_center_from_polygon(ico[11]))
  pentagone.append(get_center_from_polygon(ico[12])) 
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "9"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[8]),get_center_from_polygon(ico[10]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[10]),get_center_from_polygon(ico[15]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[15]),get_center_from_polygon(ico[11]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[11]),get_center_from_polygon(ico[12]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[12]),get_center_from_polygon(ico[8]))
  
  pentagone=[]  # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[11])) 
  pentagone.append(get_center_from_polygon(ico[12]))
  pentagone.append(get_center_from_polygon(ico[18])) 
  pentagone.append(get_center_from_polygon(ico[6]))
  pentagone.append(get_center_from_polygon(ico[1]))
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "10"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[11]),get_center_from_polygon(ico[12]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[12]),get_center_from_polygon(ico[18]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[18]),get_center_from_polygon(ico[6]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[6]),get_center_from_polygon(ico[1]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[1]),get_center_from_polygon(ico[11]))
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[12])) 
  pentagone.append(get_center_from_polygon(ico[18]))
  pentagone.append(get_center_from_polygon(ico[19])) 
  pentagone.append(get_center_from_polygon(ico[13]))
  pentagone.append(get_center_from_polygon(ico[8]))
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  
  
  # print 80*'-'
  # print "11"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[12]),get_center_from_polygon(ico[18]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[18]),get_center_from_polygon(ico[19]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[19]),get_center_from_polygon(ico[13]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[13]),get_center_from_polygon(ico[8]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[8]),get_center_from_polygon(ico[12]))
  
  pentagone=[]     # Define an pentagone temporary container.
  pentagone.append(get_center_from_polygon(ico[6]))
  pentagone.append(get_center_from_polygon(ico[2]))
  pentagone.append(get_center_from_polygon(ico[7]))
  pentagone.append(get_center_from_polygon(ico[19]))
  pentagone.append(get_center_from_polygon(ico[18]))
  dodecahedron.append(pentagone) # Add pentagone to dodecahedron pentagones container.
  
  # print 80*'-'
  # print "12"
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[6]),get_center_from_polygon(ico[2]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[2]),get_center_from_polygon(ico[7]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[7]),get_center_from_polygon(ico[19]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[19]),get_center_from_polygon(ico[18]))
  # print "get length ",get_distance_vertices(get_center_from_polygon(ico[18]),get_center_from_polygon(ico[6]))
  
  return dodecahedron

def generate_fulleren(side_length) :
  ''' Generate an fulleren from the given side length and return 2 arrays:
      an array containing hexagons,
      an array containing pentagons,
      composing the fulleren.
  '''
  
  side_length *= 3
  
  trigons=generate_icosahedron(side_length)[1] # Getting the trigons from the icosahedron faces.
  
  hexagons=[]
  for v in trigons :
    # Iteration over every trigon from the base icosahedron faces.
    points=[]
    i=-1

    while i < len(v)-1 :
      # Iterate over every segment from every face.
      # And storing the result from the segment dividing
      # To get an hexagon per face.
      points.append(div_segment_into_vertices(v[i],v[i+1],2)[1:-1])
      i += 1
      
    hexagons.append(points)  
   
  ############################################################################################################
  # Computations from the pentagons for the fulleren, full faced, displaying.
  pentagon_01=[hexagons[0][2][0],hexagons[1][1][0],hexagons[1][0][1],hexagons[2][2][0],hexagons[2][1][1]] 
  pentagon_02=[hexagons[2][1][0],hexagons[2][0][1],hexagons[3][1][0],hexagons[3][0][1],hexagons[4][0][1]]
  pentagon_03=[hexagons[4][0][0],hexagons[4][2][1],hexagons[16][1][1],hexagons[5][2][0],hexagons[5][1][1]]
  pentagon_04=[hexagons[5][0][0],hexagons[5][2][1],hexagons[17][0][0],hexagons[11][1][1],hexagons[11][2][0]]
  pentagon_05=[hexagons[6][0][0],hexagons[6][2][1],hexagons[18][1][0],hexagons[7][2][0],hexagons[7][1][1]]
  pentagon_06=[hexagons[7][0][0],hexagons[7][2][1],hexagons[19][2][1],hexagons[9][1][1],hexagons[9][2][0]]
  pentagon_07=[hexagons[9][0][1],hexagons[9][1][0],hexagons[8][2][0],hexagons[10][1][1],hexagons[10][2][0]]
  pentagon_08=[hexagons[10][1][0],hexagons[10][0][1],hexagons[11][1][0],hexagons[12][1][0],hexagons[12][0][1]]
  pentagon_09=[hexagons[14][1][1],hexagons[16][0][0],hexagons[16][2][1],hexagons[3][0][0],hexagons[3][2][1]]
  pentagon_10=[hexagons[15][1][1],hexagons[15][2][0],hexagons[17][1][0],hexagons[14][2][1],hexagons[14][0][0]]
  pentagon_11=[hexagons[1][0][0],hexagons[1][2][1],hexagons[11][0][0],hexagons[12][2][0],hexagons[18][0][0]]
  pentagon_12=[hexagons[13][1][1],hexagons[13][2][0],hexagons[18][1][1],hexagons[12][2][1],hexagons[8][0][0]]
  ############################################################################################################
  
  pentagons=[(pentagon_01,),(pentagon_02,),(pentagon_03,),(pentagon_04,),(pentagon_05,),(pentagon_06,),(pentagon_07,),(pentagon_08,),(pentagon_09,),(pentagon_10,),(pentagon_11,),(pentagon_12,)]  
   
  return hexagons,pentagons

def generate_polyhedron_26_faces(side_length) :
  ''' Generate an 26 faces polyhedron from the given side length 
      and return an array of triangles and an array of quads
      composing the 26 faces of the polyhedron.
  '''
  
  # Generation of octogons, bases of the 32 polyhedron mesh.
  octogon1=generate_polygon_on_xy_side_length(8,side_length)
  octogon2=generate_polygon_on_xy_side_length(8,side_length)
  octogon3=generate_polygon_on_xz_side_length(8,side_length)
  octogon4=generate_polygon_on_xz_side_length(8,side_length)
  octogon5=generate_polygon_on_yz_side_length(8,side_length)
  octogon6=generate_polygon_on_yz_side_length(8,side_length)
  
  # Translation to construct the polyhedron mesh.
  res=[] 
  for v in octogon1 :
    res.append(translate(v,0.0,0.0,-side_length/2.0))
  octogon1=res
  
  # Translation to construct the polyhedron mesh.
  res=[]
  for v in octogon2 :
    res.append(translate(v,0.0,0.0,side_length/2.0))
  octogon2=res 
  
  # Translation to construct the polyhedron mesh.
  res=[] 
  for v in octogon3 :
    res.append(translate(v,0.0,-side_length/2.0,0.0))
  octogon3=res
  
  # Translation to construct the polyhedron mesh.
  res=[]
  for v in octogon4 :
    res.append(translate(v,0.0,side_length/2.0,0.0))
  octogon4=res 
  
  # Translation to construct the polyhedron mesh.
  res=[] 
  for v in octogon5 :
    res.append(translate(v,-side_length/2.0,0.0,0.0))
  octogon5=res
  
  # Translation to construct the polyhedron mesh.
  res=[]
  for v in octogon6 :
    res.append(translate(v,side_length/2.0,0.0,0.0))
  octogon6=res 
  
  # We construct the polyhedron quads:
  quads_xy=[]
  i=-1
  while i < len(octogon1)-1 :
    # by iterating overs octogon1 and octogon2
    # which are in the plan XY.
    # With clever indexing.
    quads=[]
    quads.append(octogon1[i])
    quads.append(octogon1[i+1])
    quads.append(octogon2[i+1])
    quads.append(octogon2[i])
    quads_xy.append(quads)
    i += 1
  
  # We construct the polyhedron quads:
  quads_xz=[]
  i=-1
  while i < len(octogon3)-1 :
    # by iterating overs octogon3 and octogon4
    # which are in the plan XZ.
    # With clever indexing.
    quads=[]
    quads.append(octogon3[i])
    quads.append(octogon3[i+1])
    quads.append(octogon4[i+1])
    quads.append(octogon4[i])
    quads_xz.append(quads)
    i += 1 
  
  # We construct the polyhedron quads:
  quads_yz=[]
  i=-1
  while i < len(octogon1)-1 :
    # by iterating overs octogon3 and octogon4
    # which are in the plan XZ.
    # With clever indexing.
    quads=[]
    quads.append(octogon5[i])
    quads.append(octogon5[i+1])
    quads.append(octogon6[i+1])
    quads.append(octogon6[i])
    quads_yz.append(quads)
    i += 1  
  
  
  # Finally we keep only the needed quads. To not have doubles.
  polyhedron=[]
  for v in quads_xz :
    polyhedron.append(v)
    
  polyhedron.append(quads_xy[0])
  polyhedron.append(quads_xy[1])
  polyhedron.append(quads_xy[2])
  polyhedron.append(quads_xy[4])
  polyhedron.append(quads_xy[5])
  polyhedron.append(quads_xy[6])
  
  polyhedron.append(quads_yz[0])
  polyhedron.append(quads_yz[2])
  polyhedron.append(quads_yz[4])
  polyhedron.append(quads_yz[6])
  
  # Finally we construct the triangles of the polyhedron.
  triangle1=[polyhedron[1][1],polyhedron[3][0],polyhedron[12][3]]
  triangle2=[polyhedron[3][1],polyhedron[5][0],polyhedron[12][0]]
  triangle3=[polyhedron[5][1],polyhedron[6][1],polyhedron[12][1]]
  triangle4=[polyhedron[7][1],polyhedron[1][0],polyhedron[12][2]]
  
  triangle5=[polyhedron[7][2],polyhedron[1][3],polyhedron[9][3]]
  triangle6=[polyhedron[5][3],polyhedron[4][3],polyhedron[9][1]]
  triangle7=[polyhedron[6][3],polyhedron[7][3],polyhedron[9][0]]
  triangle8=[polyhedron[1][2],polyhedron[2][2],polyhedron[9][2]]
  
  return [triangle1,triangle2,triangle3,triangle4,triangle5,triangle6,triangle7,triangle8], polyhedron


def generate_polyhedron_32_faces(side_length) :
  ''' Generate an 32 faces polyhedron from the given side length, 
      return an 2-array composed from:
      an sequence of the triangles from the 32hedron
      an sequence of the pentagons from the 32hedron.
  '''    
  
  ico_base_quads,ico=generate_icosahedron(side_length) # Return the ico construction base quads
                                                       # and the triangles from the icosahedron.
  
  upper=ico_base_quads[2][2]	# Top vertice from the icosahedron we gonna use as construction reference.
  
   
  penta_1=[ico_base_quads[2][3],ico_base_quads[1][2],ico_base_quads[0][0],ico_base_quads[0][1],ico_base_quads[1][1]]
  
  penta_2=[ico_base_quads[2][1],ico_base_quads[1][3],ico_base_quads[0][3],ico_base_quads[0][2],ico_base_quads[1][0]]
  
  down=ico_base_quads[2][0]	# Down vertice from the icosahedron we gonna use as construction reference.
  
  pentagon_top=[]
  pentagon_bottom=[]
  
  for v in penta_1 :
    # Loop to generate the top pentagon from the 32hedron.
    pentagon_top.append(get_middle_from_segment(upper,v))
  
  for v in penta_2 :
    # Loop to generate the bottom pentagon from the 32hedron.
    pentagon_bottom.append(get_middle_from_segment(down,v))
  
  ###############################################################################
  # Generate the pentagons beetween the top and the middle from the 32 hedron.
  pentagon_middle_top_1=[]
  pentagon_middle_top_1.append(get_middle_from_segment(penta_1[0],upper))
  pentagon_middle_top_1.append(get_middle_from_segment(penta_1[0],penta_1[1]))
  pentagon_middle_top_1.append(get_middle_from_segment(penta_1[0],penta_2[2]))
  pentagon_middle_top_1.append(get_middle_from_segment(penta_1[0],penta_2[3]))
  pentagon_middle_top_1.append(get_middle_from_segment(penta_1[0],penta_1[4]))
  
  pentagon_middle_top_2=[]
  pentagon_middle_top_2.append(get_middle_from_segment(penta_1[1],upper))
  pentagon_middle_top_2.append(get_middle_from_segment(penta_1[1],penta_1[2]))
  pentagon_middle_top_2.append(get_middle_from_segment(penta_1[1],penta_2[1]))
  pentagon_middle_top_2.append(get_middle_from_segment(penta_1[1],penta_2[2]))
  pentagon_middle_top_2.append(get_middle_from_segment(penta_1[1],penta_1[0]))
  
  pentagon_middle_top_3=[]
  pentagon_middle_top_3.append(get_middle_from_segment(penta_1[2],upper))
  pentagon_middle_top_3.append(get_middle_from_segment(penta_1[2],penta_1[3]))
  pentagon_middle_top_3.append(get_middle_from_segment(penta_1[2],penta_2[0]))
  pentagon_middle_top_3.append(get_middle_from_segment(penta_1[2],penta_2[1]))
  pentagon_middle_top_3.append(get_middle_from_segment(penta_1[2],penta_1[1]))
  
  pentagon_middle_top_4=[]
  pentagon_middle_top_4.append(get_middle_from_segment(penta_1[3],upper))
  pentagon_middle_top_4.append(get_middle_from_segment(penta_1[3],penta_1[4]))
  pentagon_middle_top_4.append(get_middle_from_segment(penta_1[3],penta_2[4]))
  pentagon_middle_top_4.append(get_middle_from_segment(penta_1[3],penta_2[0]))
  pentagon_middle_top_4.append(get_middle_from_segment(penta_1[3],penta_1[2]))
  
  pentagon_middle_top_5=[]
  pentagon_middle_top_5.append(get_middle_from_segment(penta_1[4],upper))
  pentagon_middle_top_5.append(get_middle_from_segment(penta_1[4],penta_1[0]))
  pentagon_middle_top_5.append(get_middle_from_segment(penta_1[4],penta_2[3]))
  pentagon_middle_top_5.append(get_middle_from_segment(penta_1[4],penta_2[4]))
  pentagon_middle_top_5.append(get_middle_from_segment(penta_1[4],penta_1[3]))
  ################################################################################ 
  
  ###############################################################################
  # Generate the pentagons beetween the bottom and the middle from the 32 hedron.
  pentagon_middle_bottom_1=[]
  pentagon_middle_bottom_1.append(get_middle_from_segment(penta_2[0],down))
  pentagon_middle_bottom_1.append(get_middle_from_segment(penta_2[0],penta_2[1]))
  pentagon_middle_bottom_1.append(get_middle_from_segment(penta_2[0],penta_1[2]))
  pentagon_middle_bottom_1.append(get_middle_from_segment(penta_2[0],penta_1[3]))
  pentagon_middle_bottom_1.append(get_middle_from_segment(penta_2[0],penta_2[4]))
  
  pentagon_middle_bottom_2=[]
  pentagon_middle_bottom_2.append(get_middle_from_segment(penta_2[1],down))
  pentagon_middle_bottom_2.append(get_middle_from_segment(penta_2[1],penta_2[2]))
  pentagon_middle_bottom_2.append(get_middle_from_segment(penta_2[1],penta_1[1]))
  pentagon_middle_bottom_2.append(get_middle_from_segment(penta_2[1],penta_1[2]))
  pentagon_middle_bottom_2.append(get_middle_from_segment(penta_2[1],penta_2[0]))
  
  pentagon_middle_bottom_3=[]
  pentagon_middle_bottom_3.append(get_middle_from_segment(penta_2[2],down))
  pentagon_middle_bottom_3.append(get_middle_from_segment(penta_2[2],penta_2[3]))
  pentagon_middle_bottom_3.append(get_middle_from_segment(penta_2[2],penta_1[0]))
  pentagon_middle_bottom_3.append(get_middle_from_segment(penta_2[2],penta_1[1]))
  pentagon_middle_bottom_3.append(get_middle_from_segment(penta_2[2],penta_2[1]))
  
  pentagon_middle_bottom_4=[]
  pentagon_middle_bottom_4.append(get_middle_from_segment(penta_2[3],down))
  pentagon_middle_bottom_4.append(get_middle_from_segment(penta_2[3],penta_2[4]))
  pentagon_middle_bottom_4.append(get_middle_from_segment(penta_2[3],penta_1[4]))
  pentagon_middle_bottom_4.append(get_middle_from_segment(penta_2[3],penta_1[0]))
  pentagon_middle_bottom_4.append(get_middle_from_segment(penta_2[3],penta_2[2]))
  
  pentagon_middle_bottom_5=[]
  pentagon_middle_bottom_5.append(get_middle_from_segment(penta_2[4],down))
  pentagon_middle_bottom_5.append(get_middle_from_segment(penta_2[4],penta_2[0]))
  pentagon_middle_bottom_5.append(get_middle_from_segment(penta_2[4],penta_1[3]))
  pentagon_middle_bottom_5.append(get_middle_from_segment(penta_2[4],penta_1[4]))
  pentagon_middle_bottom_5.append(get_middle_from_segment(penta_2[4],penta_2[3]))
  
  ###############################################################################
  
  #########################################################################
  # Triangles between the top and the middle.
  triangle_top_1=[pentagon_middle_top_1[4],pentagon_top[4],pentagon_top[0]]
  triangle_top_2=[pentagon_middle_top_2[4],pentagon_top[0],pentagon_top[1]]
  triangle_top_3=[pentagon_middle_top_3[4],pentagon_top[1],pentagon_top[2]]
  triangle_top_4=[pentagon_middle_top_4[4],pentagon_top[2],pentagon_top[3]]
  triangle_top_5=[pentagon_middle_top_5[4],pentagon_top[3],pentagon_top[4]]
  
  #########################################################################
  # Triangles in the top-middle.
  triangle_middle_top_1=[pentagon_middle_top_1[3],pentagon_middle_top_1[4],pentagon_middle_top_5[2]]
  triangle_middle_top_2=[pentagon_middle_top_2[3],pentagon_middle_top_2[4],pentagon_middle_top_1[2]]
  triangle_middle_top_3=[pentagon_middle_top_3[3],pentagon_middle_top_3[4],pentagon_middle_top_2[2]]
  triangle_middle_top_4=[pentagon_middle_top_4[3],pentagon_middle_top_4[4],pentagon_middle_top_3[2]]
  triangle_middle_top_5=[pentagon_middle_top_5[3],pentagon_middle_top_5[4],pentagon_middle_top_4[2]]
  
  #########################################################################
  # Triangles in the bottom-middle.
  triangle_middle_bottom_1=[pentagon_middle_bottom_1[3],pentagon_middle_bottom_1[4],pentagon_middle_bottom_5[2]]
  triangle_middle_bottom_2=[pentagon_middle_bottom_2[3],pentagon_middle_bottom_2[4],pentagon_middle_bottom_1[2]]
  triangle_middle_bottom_3=[pentagon_middle_bottom_3[3],pentagon_middle_bottom_3[4],pentagon_middle_bottom_2[2]]
  triangle_middle_bottom_4=[pentagon_middle_bottom_4[3],pentagon_middle_bottom_4[4],pentagon_middle_bottom_3[2]]
  triangle_middle_bottom_5=[pentagon_middle_bottom_5[3],pentagon_middle_bottom_5[4],pentagon_middle_bottom_4[2]]
  
  #########################################################################
  # Triangles between the bottom and the middle.
  triangle_bottom_1=[pentagon_middle_bottom_1[4],pentagon_bottom[4],pentagon_bottom[0]]
  triangle_bottom_2=[pentagon_middle_bottom_2[4],pentagon_bottom[0],pentagon_bottom[1]]
  triangle_bottom_3=[pentagon_middle_bottom_3[4],pentagon_bottom[1],pentagon_bottom[2]]
  triangle_bottom_4=[pentagon_middle_bottom_4[4],pentagon_bottom[2],pentagon_bottom[3]]
  triangle_bottom_5=[pentagon_middle_bottom_5[4],pentagon_bottom[3],pentagon_bottom[4]]
  
  sequence_of_triangles = [triangle_top_1,triangle_top_2,triangle_top_3,triangle_top_4,triangle_top_5,
	                  triangle_middle_top_1,triangle_middle_top_2,triangle_middle_top_3,triangle_middle_top_4,triangle_middle_top_5,
	                  triangle_middle_bottom_1,triangle_middle_bottom_2,triangle_middle_bottom_3,triangle_middle_bottom_4,triangle_middle_bottom_5,
	                  triangle_bottom_1,triangle_bottom_2,triangle_bottom_3,triangle_bottom_4,triangle_bottom_5]
  
  sequence_of_pentagons = [pentagon_top,
                           pentagon_middle_top_1,pentagon_middle_top_2,pentagon_middle_top_3,pentagon_middle_top_4,pentagon_middle_top_5,
                           pentagon_middle_bottom_1,pentagon_middle_bottom_2,pentagon_middle_bottom_3,pentagon_middle_bottom_4,pentagon_middle_bottom_5,
                           pentagon_bottom]
  
  
  return [sequence_of_triangles,sequence_of_pentagons]

def generate_toros(base,base_radius,toros_radius) :
  ''' Generate an toros in relationship to the given settings:
      base:         the toros basis polygon.
      base_radius:  the toros basis polygon radius.
      toros_radius: the toros radius (without the base polygon radius). 
      and return an sequence of polygons base from the toros.
  '''    
      
  base_polygon=generate_polygon_on_yz_radius(base,base_radius,Vertex(0.,0.,0.))
  i=0
  toros=[]
  while i < 360.0 :
    polygon=[]
    for v in base_polygon :
      vertex=rotate_y(translate(v,0.0,0.0,toros_radius),i)
      polygon.append(vertex)
    
    i += 360.0/base
    toros.append(polygon)
    
  return toros  
