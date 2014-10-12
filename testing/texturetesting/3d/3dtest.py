import os
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from objects.matrix44 import *
from objects.vector3 import *

from math import radians 

SCREEN_SIZE = (800, 600)

def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_FLAT)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)        
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))    
    
    
class Cube(object):
    
    
    def __init__(self, position, color):
        
        self.position = position
        self.color = color
    
    num_faces = 6
        
    vertices = [ (0.0, 0.0, 1.0),
                 (1.0, 0.0, 1.0),
                 (1.0, 1.0, 1.0),
                 (0.0, 1.0, 1.0),
                 (0.0, 0.0, 0.0),
                 (1.0, 0.0, 0.0),
                 (1.0, 1.0, 0.0),
                 (0.0, 1.0, 0.0) ]
        
    normals = [ (0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left 
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ] # bottom
    
    vertex_indices = [ (0, 1, 2, 3),  # front
                       (4, 5, 6, 7),  # back
                       (1, 5, 6, 2),  # right
                       (0, 4, 7, 3),  # left
                       (3, 2, 6, 7),  # top
                       (0, 1, 5, 4) ] # bottom    

    def render(self):                
        
        glColor( self.color )
    
        # Adjust all the vertices so that the cube is at self.position
        vertices = [tuple(Vector3(v) + self.position) for v in self.vertices]
            
        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)
    
        for face_no in xrange(self.num_faces):
                        
            glNormal3dv( self.normals[face_no] )
            
            v1, v2, v3, v4 = self.vertex_indices[face_no]
                    
            glVertex( vertices[v1] )
            glVertex( vertices[v2] )
            glVertex( vertices[v3] )
            glVertex( vertices[v4] )            
        
        glEnd()
        

class Map(object):
    
    def __init__(self,map_file):
        
        self.map_file = map_file
        
        
        map_surface = pygame.image.load(self.map_file)
        self.map_surface = map_surface
        self.map_surface.lock()
        
        w, h = self.map_surface.get_size()
        
        self.cubes = []
        
        # Create a cube for every non-white pixel
        for y in range(h):            
            for x in range(w):
                                
                r, g, b, a = self.map_surface.get_at((x, y))
                
                if (r, g, b) != (255, 255, 255):
                    
                    gl_col = (r/255.0, g/255.0, b/255.0)
                    position = (float(x), 0.0, float(y))
                    cube = Cube( position, gl_col )
                    self.cubes.append(cube)                    
                
        
        self.map_surface.unlock()
    
        self.display_list = None
    
    def render(self):
                
        if self.display_list is None:
            
            # Create a display list
            self.display_list = glGenLists(1)                
            glNewList(self.display_list, GL_COMPILE)
            
            # Draw the cubes
            for cube in self.cubes:
                cube.render()
                
            # End the display list
            glEndList()
            
        else:
            
            # Render the display list            
            glCallList(self.display_list)
                    

def run():
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    
    resize(*SCREEN_SIZE)
    init()
    
    clock = pygame.time.Clock()    
    
    glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
    glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

    # This object renders the 'map'
    current_dir = os.path.join(os.path.abspath(''))
    testing_dir = os.path.join(current_dir,"testing","texturetesting","3d")
    map_file = os.path.join(testing_dir,"map.png")
    map = Map(map_file)
    print(map.map_file)

    # Camera transform matrix
    camera_matrix = Matrix44()
    camera_matrix.translate = (10.0, .5, 10.0)

    # Initialize speeds and directions
    rotation_direction = Vector3()
    rotation_speed = radians(180.0)
    movement_direction = Vector3()
    movement_speed = 20.0    

    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return                
            
        # Clear the screen, and z-buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                        
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0
        
        pressed = pygame.key.get_pressed()
        
        # Reset rotation and movement directions
        rotation_direction.set(0.0, 0.0, 0.0)
        movement_direction.set(0.0, 0.0, 0.0)
        
        # Modify direction vectors for key presses
        if pressed[K_LEFT]:
            rotation_direction.y = +1.0
        elif pressed[K_RIGHT]:
            rotation_direction.y = -1.0
        if pressed[K_UP]:
            rotation_direction.x = +1.0
        elif pressed[K_DOWN]:
            rotation_direction.x = -1.0
        if pressed[K_a]:
            movement_direction.x = -1.0
        elif pressed[K_d]:
            movement_direction.x = +1.0
        if pressed[K_w]:
            movement_direction.z = -1.0
        elif pressed[K_s]:
            movement_direction.z = +1.0
        
        # Calculate rotation matrix and multiply by camera matrix    
        rotation = rotation_direction * rotation_speed * time_passed_seconds
        rotation_matrix = Matrix44.xyz_rotation(*rotation)
        camera_matrix *= rotation_matrix
        
        # Calcluate movment and add it to camera matrix translate
        heading = Vector3(camera_matrix.forward)
        heading_right = Vector3(camera_matrix.right)
        heading_top = Vector3(camera_matrix.top)
        movement_x = heading_right * movement_direction.x * movement_speed
        movement_y = heading_top * movement_direction.y * movement_speed
        movement_z = heading * movement_direction.z * movement_speed
        camera_matrix.translate += (movement_z * time_passed_seconds) + (movement_y * time_passed_seconds) + (movement_x * time_passed_seconds)
        
        # Upload the inverse camera matrix to OpenGL
        glLoadMatrixd(camera_matrix.get_inverse().to_opengl())
                
        # Light must be transformed as well
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0))
                
        # Render the map
        map.render()
        
                
        # Show the screen
        pygame.display.flip()

run()