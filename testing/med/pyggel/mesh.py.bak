"""
pyggel.mesh
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The mesh module contains mesh classes for different kinds of meshes, as well as loaders for various kinds of meshes.
"""

from include import *
import sys,os
import image, view, data, misc, math3d
from scene import BaseSceneObject
import time
import random
import math
import pygame
import psyco
psyco.full()
pygame.init()
def OBJ(filename, pos=(0,0,0), rotation=(0,0,0), colorize=(10,10,10,1)):
    """Load a WaveFront OBJ mesh.
       filename must be the filename of the mesh to load
       pos/rotation/colorize are the starting attributes of the mesh object."""
    view.require_init()

    objs = []
    mtls = {}

    vertices = []
    normals = []
    texcoords = []

    print "*** creating object!"
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
    
        
                
        if not values: continue
        if values[0] in ("o", "g"):
            objs.append(ObjGroup(values[1]))
        elif values[0] == 'v':
            vertices.append(map(float, values[1:4]))
        elif values[0] == 'vn':
            normals.append(map(float, values[1:4]))
        elif values[0] == 'vt':
            texcoords.append(map(float, values[1:3]))
        elif values[0] in ('usemtl', 'usemat'):
            if len(objs)>0:
                objs[-1].material = mtls[values[1]]
        elif values[0] == 'mtllib':
            path = os.path.split(filename)[0]
            cur_mtl = None
            for line in open(os.path.join(path, values[1]), "r"):
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue
                if values[0] == 'newmtl':
                    cur_mtl = data.Material(values[1])
                    mtls[cur_mtl.name] = cur_mtl
                elif cur_mtl is None:
                    raise ValueError, "mtl file doesn't start with newmtl stmt"
                elif values[0] == 'map_Kd':
                    cur_mtl.texture = data.Texture(os.path.join(path, values[1]))
                elif values[0]=="Kd":
                    cur_mtl.set_color(map(float, values[1:]))
        elif values[0] == 'f':
            face = []
            tcoords = []
            norms = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    tcoords.append(int(w[1]))
                else:
                    tcoords.append(0)
                if len(w) >= 3 and len(w[2]) > 0:
                    norms.append(int(w[2]))
                else:
                    norms.append(0)
            objs[-1].faces.append((face, norms, tcoords)) 

    fin = []
    for i in objs:
        fin.append(i.compile(vertices, normals, texcoords))

    return BasicMesh(fin, pos, rotation, 1, colorize)

class ObjGroup(object):
    """Class to keep track of an objects verts and such while being loaded."""
    def __init__(self, name):
        """name is the name of the object."""
        self.name = name
        self.faces = []
        self.material = None

        self.dlist = None

    def compile(self, vertices, normals, texcoords):
        """Compile the ObjGroup into a CompiledGroup for rendering/using."""
        faces = []
        for face in self.faces:
            v,n,t = face
            uv, un, ut = [], [], [] 
            for i in xrange(len(v)):
                if n[i] > 0:
                    un.append(normals[n[i]-1])
                else:
                    un.append(None)

                if t[i] > 0:
                    ut.append(texcoords[t[i]-1])
                else:
                    ut.append(None)
                uv.append(vertices[v[i]-1])
            faces.append((uv, un, ut))
        
        final = []
        for face in faces:
            v,n,t = face
            nv = []
            for i in v:
                a,b,c = i
                nv.append((a,b,c))
            final.append((nv,n,t))

        #now build our display list!
        dlist = data.DisplayList()
        dlist.begin()

        minx = miny = minz = 0
        maxx = maxy = maxz = 0

        avgx, avgy, avgz = 0,0,0
        num = 0

        for face in final:
            v = face[0]
            for i in xrange(len(v)):
                num += 1
                x, y, z = v[i]
                avgx += x
                avgy += y
                avgz += z

        avgx = math3d.safe_div(float(avgx), num)
        avgy = math3d.safe_div(float(avgy), num)
        avgz = math3d.safe_div(float(avgz), num)

        for face in final:
            v, n, t = face
            glBegin(GL_POLYGON)
            for i in xrange(len(v)):
                if n[i]:
                    glNormal3fv(n[i])
                if t[i]:
                    glTexCoord2fv(t[i])
                x, y, z = v[i]
                glVertex3f(x-avgx, y-avgy, z-avgz)
                minx = min((minx, x))
                maxx = max((maxx, x))
                miny = min((miny, y))
                maxy = max((maxy, y))
                minz = min((minz, z))
                maxz = max((maxz, z))
            glEnd()

        dlist.end()

        if self.material == None:
            self.material = data.Material("null")

        return CompiledGroup(self.name, self.material, dlist, (minx,miny,minz, maxx, maxy, maxz),
                             (avgx, avgy, avgz))

class CompiledGroup(BaseSceneObject):
    """The core object in a mesh, each mesh object (head, torso, w/e) has one of these.
       It has it's own attributes for pos/rotation/etc. and also is affected by the parent mesh's."""
    def __init__(self, name, material, dlist, dimensions, pos):
        """Create the Group
           name is the name of the object
           material is the data.Material object the group uses
           dlist is the display list of the object
           dimensions/pos are the size/center of the vertices in the object."""
        BaseSceneObject.__init__(self)
        self.name = name
        self.material = material
        self.display_list = dlist
        self.dimensions = dimensions

        self.base_pos = pos
        self.pos = pos

    def get_dimensions(self):
        """Return the dimensions of the object."""
        d = self.dimensions
        return abs(d[0]-d[3]), abs(d[1]-d[4]), abs(d[2]-d[5])

    def side(self, name):
        if type(name) is type(""):
            names = ["left", "top", "front",
                     "right", "bottom", "back"]
            if name in names:
                return self.dimensions[names.index(name)]
            names = ["width", "height", "depth"]
            if name in names:
                return self.get_dimensions()[names.index(name)]
        elif type(name) is type(1):
            return self.dimensions[name]

    def render(self, camera=None):
        """Render the object.
           camera must be None of the camera object the scene is using to render."""
        glPushMatrix()

        x,y,z = self.pos
        glTranslatef(x,y,z)
        a, b, c = self.rotation
        glRotatef(a, 1, 0, 0)
        glRotatef(b, 0, 1, 0)
        glRotatef(c, 0, 0, 1)

        try:
            glScalef(*self.scale)
        except:
            glScalef(self.scale, self.scale, self.scale)

        if self.outline:
            misc.outline(self.dlist, self.outline_color, self.outline_size)
        glColor4f(*self.material.color)
        self.material.texture.bind()
        self.display_list.render()
        glPopMatrix()

    def copy(self):
        """Return a copy of the object."""
        new = CompiledGroup(str(self.name),
                             self.material.copy(),
                             self.display_list,
                             self.dimensions,
                            self.base_pos)
        new.pos = self.pos
        new.rotation = self.rotation
        new.scale = self.scale

        new.visible = self.visible
        new.pickable = self.pickable

        new.outline = self.outline
        new.outline_size = self.outline_size
        new.outline_color = self.outline_color
        return new

class BasicMesh(BaseSceneObject):
    """Core mesh class, contains several objects representing the objects in the mesh."""
    def __init__(self, objs, pos=(0,0,0), rotation=(0,0,0),
                 scale=1, colorize=(1,1,1,1)):
        """Create the mesh object
           objs must be a lit of the CompiledGroup objects of the mesh
           pos/rotation/scale/colorize attributes of the mesh"""
        BaseSceneObject.__init__(self)

        self.objs = objs
        self.pos = pos
        self.rotation = rotation
        self.scale = scale
        self.colorize = colorize

    def get_dimensions(self):
        """Return the width, height and depth of the mesh..."""
        minx = miny = minz = 0
        maxx = maxy = maxz = 0
        for i in self.objs:
            d = i.dimensions
            minx = min(minx, d[0])
            maxx = max(maxx, d[3])
            miny = min(minx, d[1])
            maxy = max(maxx, d[4])
            minz = min(minx, d[2])
            maxz = max(maxx, d[5])

        return abs(minx-maxx), abs(miny-maxy), abs(minz-maxz)

    def copy(self):
        """Return a copy of the mesh, sharing the same data.DisplayList"""
        new_objs = []
        for i in self.objs:
            new_objs.append(i.copy())
        new = BasicMesh(new_objs, self.pos, self.rotation, self.scale, self.colorize)
        return new

    def get_names(self):
        """Return the names of all the objects in the mesh."""
        return [i.name for i in self.objs]

    def get_obj_by_name(self, name):
        """Return the CompiledGroup object reprensting the object <name>"""
        for i in self.objs:
            if i.name == name:
                return i
        return None

    def render(self, camera=None):
        """Render the mesh
           camera must be None of the camera the scene is using"""
        glPushMatrix()
        x,y,z = self.pos
        glTranslatef(x,y,-z)
        a, b, c = self.rotation
        glRotatef(a, 1, 0, 0)
        glRotatef(b, 0, 1, 0)
        glRotatef(c, 0, 0, 1)
        try:
            glScalef(*self.scale)
        except:
            glScalef(self.scale, self.scale, self.scale)
        if self.colorize!=False:
            glColor(*self.colorize)

        if self.outline:
            new = []
            for i in self.objs:
                x = i.copy()
                x.material = data.Material("blank")
                x.material.set_color(self.outline_color)
                x.outline = False
                new.append(x)
            misc.outline(misc.OutlineGroup(new),
                         self.outline_color, self.outline_size)

        for i in self.objs:
            old = tuple(i.material.color)
            r,g,b,a = old
            if self.colorize!=False:
                r2,g2,b2,a2 = self.colorize
            else:
                r2,g2,b2,a2 = 1,1,1,1
            
            r *= r2
            g *= g2
            b *= b2
            a = a2
            i.material.color = r,g,b,a
            i.render(camera)
            i.material.color = old
        glPopMatrix()


class Exploder(BaseSceneObject):
    """A simple class to explode/dismember a mesh object."""
    def __init__(self, root_mesh, speed=0.025, frame_duration=10,
                 kill_when_finished=True):
        """Create the exploder
           root_mesh must be a BasicMesh object to explode
           speed is how fast you want each piece to move/rotate
           frame_duration is how many times it will update before dying
           kill_when_finished indicates whether the exploder should be removed
                              from the scene when it ends"""
        BaseSceneObject.__init__(self)

        self.kill_when_finished = kill_when_finished

        self.root_mesh = root_mesh
        self.angles = {}
        self.rots = {}
        for i in self.root_mesh.get_names():
            a = math3d.Vector(self.root_mesh.get_obj_by_name(i).base_pos)
            x, y, z = a.x, a.y, a.z
            if x == y == z == 0:
                x, y, z = misc.randfloat(-2,2), misc.randfloat(0,2), misc.randfloat(-2,2)
            else:
                a = a.normalize()
                x, y, z = a.x, a.y, a.z

            y += misc.randfloat(1.5,2.5)
            self.angles[i] = x+misc.randfloat(-1,1), y+misc.randfloat(-1,1), z+misc.randfloat(-1,1)
            self.rots[i] = (misc.randfloat(-10, 10),
                            misc.randfloat(-10, 10),
                            misc.randfloat(-10, 10))

        self.root_vals = {}
        for i in self.root_mesh.get_names():
            self.root_vals[i] = (self.root_mesh.get_obj_by_name(i).pos,
                                 self.root_mesh.get_obj_by_name(i).rotation)

        self.speed = speed
        self.age = 0
        self.frame_duration = frame_duration
        self.dead = False
        self.down_delta = 0

    def reset(self):
        """Reset he explosion to run again!"""
        self.angles = {}
        self.rots = {}
        for i in self.root_mesh.get_names():
            a = math3d.Vector(self.root_mesh.get_obj_by_name(i).base_pos)
            x, y, z = a.x, a.y, a.z
            if x == y == z == 0:
                x, y, z = misc.randfloat(-1,1), misc.randfloat(-1,1), misc.randfloat(-1,1)
            else:
                a = a.normalize()
                x, y, z = a.x, a.y, a.z

            y += misc.randfloat(1.5,2.5)
            self.angles[i] = x+misc.randfloat(-1,1), y+misc.randfloat(-1,1), z+misc.randfloat(-1,1)
            self.rots[i] = (misc.randfloat(-10, 10),
                            misc.randfloat(-10, 10),
                            misc.randfloat(-10, 10))

        for i in self.root_vals:
            self.root_mesh.get_obj_by_name(i).pos = self.root_vals[i][0]
            self.root_mesh.get_obj_by_name(i).rotation = self.root_vals[i][1]

        self.age = 0
        self.dead = False
        self.down_delta = 0

    def render(self, camera=None):
        """Update and render the explosion
           camera must be None or the camera the scene is using."""
        if self.age <= self.frame_duration:
            for i in self.root_mesh.objs:
                a, b, c = i.pos
                d,e,f = self.angles[i.name]
                a += d *self.speed
                b += e *self.speed
                c += f *self.speed
                i.pos = a, b, c
                e -= self.down_delta
                self.down_delta += self.speed / self.frame_duration / 2
                self.angles[i.name] = d,e,f
                a,b,c = i.rotation
                d,e,f = self.rots[i.name]
                a += d *self.speed*2
                b += e *self.speed*2
                c += f *self.speed*2
                i.rotation = (a,b,c)
        self.root_mesh.render(camera)

        if self.age >= self.frame_duration:
            if self.kill_when_finished:
                self.dead_remove_from_scene = True
            self.dead = True
        else:
            self.age += 1


class Bone(object):
    """A simple bone used to animate a part of a mesh."""
    def __init__(self, start, end, anchor=0):
        """Create the bone
           start is the 3d position of the top of the bone
           end is the 3d position of the bottom of the bone
           anchor is 0.0-1.0 location of the anchor for rotations - 0=start, 1=end, 0.5=center"""
        self._start = start
        self._end = end
        self._anchor = anchor

        self.cur_start = self._start
        self.cur_end = self._end

        self.children = []

        self.rotation = (0,0,0)
        self.mod_rotation = (0,0,0)
        self.movement = (0,0,0)
        self.scale = (1,1,1)

    def get_anchor(self):
        """Calculate the current position of the anchor point."""
        a,b,c = self.cur_end
        d,e,f = self.cur_start
        a2 = (a - d)*self._anchor + d
        b2 = (b - e)*self._anchor + e
        c2 = (c - f)*self._anchor + f
        return a2,b2,c2

    def get_rotation(self):
        """Return the current rotation of the bone."""
        return self.merge(self.rotation, self.mod_rotation)

    def merge(self, a, b, amount=1):
        """add all elements of b (multiplying each element by amount) to a"""
        new = []
        for i in xrange(len(a)):
            new.append(a[i]+(b[i]*amount))
        return new

    def dif3(self, a, b, amount=1):
        """subtract all elements of b from a - multiplying the result by amount."""
        dif = []
        for i in xrange(3):
            dif.append((a[i]-b[i])*amount)
        return dif

    def move(self, x,y,z):
        """Move the bone and all children."""
        self.movement = self.merge(self.movement, (x,y,z))

    def rotate(self, x, y, z):
        """Rotate the bone and children around the anchor point."""
        self.rotation = self.merge(self.rotation, (x,y,z))

    def push_rotation(self, rot=None, anchor=None):
        """Calculate the current rotated position of the bone points."""
        if not anchor:
            anchor = self.get_anchor()
        if not rot:
            x,y,z = self.rotation
        else:
            x,y,z = rot
            self.mod_rotation = self.merge(self.mod_rotation, (x,y,z))

        vec1 = math3d.Vector(anchor)
        vec2 = math3d.Vector(self.cur_start)
        vec3 = math3d.Vector(self.cur_end)

        new1 = vec2.rotate(vec1, (-x, y, z))
        new2 = vec3.rotate(vec1, (-x, y, z))

        self.cur_start = new1.get_pos()
        self.cur_end = new2.get_pos()

        for i in self.children:
            i.push_rotation((x,y,z), anchor)

    def push_move(self, pos=None):
        """Calculate the current moved position of the bone points."""
        if not pos:
            pos = self.movement
        self.cur_start = self.merge(pos, self.cur_start)
        self.cur_end = self.merge(pos, self.cur_end)
        for i in self.children:
            i.push_move(pos)

    def scaled(self, x,y,z):
        """Scale the bone and all children."""
        self.scale = self.merge(self.scale, (x,y,z))
        for i in self.children:
            i.scaled(x,y,z)

    def get_center(self):
        """Return the current center point of the bone."""
        a,b,c = self.cur_start
        d,e,f = self.cur_end
        return (math3d.safe_div(a+d, 2.0),
                math3d.safe_div(b+e, 2.0),
                math3d.safe_div(c+f, 2.0))

    def get_points(self):
        """Return the current start, center and end points of the bone."""
        return self.cur_start, self.get_center(), self.cur_end

    def reset(self):
        """Reset the current values of the bone."""
        self.rotation = (0,0,0)
        self.mod_rotation = (0,0,0)
        self.movement = (0,0,0)
        self.cur_start = self._start
        self.cur_end = self._end
        self.scale = (1,1,1)

    def push(self):
        """Calculate the current bone values."""
        self.push_rotation()
        self.push_move()

class CoreAnimationCommand(object):
    """Basic animation command class."""
    def __init__(self, obj, val, start, end):
        """Create the command
           obj is the name of the mesh part this action works on
           val is the (x,y,z) target value - where you want the bone to be
           start - when you want this action to start, in seconds
           end - when you want it to end - bone value will equal val at this point"""
        self.obj = obj
        self.val = val
        self.start = start
        self.end = end

    def _m(self, a, b, amount=1):
        """add all elements of b (multiplying each element by amount) to a"""
        new = []
        for i in xrange(len(a)):
            new.append(a[i]+(b[i]*amount))
        return new

    def _d(self, a, b, amount=1):
        """subtract all elements of b from a - multiplying the result by amount."""
        new = []
        for i in xrange(len(a)):
            new.append((a[i]-b[i])*amount)
        return new

    def update(self, skeleton, tstamp_last, tstamp_cur):
        "Update the skeleton based on the last and current timestamps."""
        if self.obj in skeleton.bones:
            obj = skeleton.bones[self.obj]
        else:
            return None
        pos, rotation, scale = obj.get_center(), obj.rotation, obj.scale
        if tstamp_last > self.end or tstamp_cur < self.start:
            return None
        _s = max((tstamp_last, self.start))
        _e = min((tstamp_cur, self.end))
        mult = math3d.safe_div(float(_e-_s), self.end-_s)
        if self.ident == "RT":
            a,b,c = self._d(self.val, rotation, mult)
            obj.rotate(a,b,c)
        if self.ident == "MT":
            pos = self._d(self.val, pos, mult)
            obj.move(*pos)
        if self.ident == "ST":
            scale = self._d(self.val, scale, mult)
            obj.scaled(*scale)

    def reset(self, skeleton):
        """Reset changes"""
        if self.obj in skeleton.bones:
            skeleton.bones[self.obj].reset()

class RotateTo(CoreAnimationCommand):
    """Rotation command."""
    ident = "RT"

class MoveTo(CoreAnimationCommand):
    """Movement command."""
    ident = "MT"

class ScaleTo(CoreAnimationCommand):
    """Scale command."""
    ident = "ST"

class Action(object):
    """Object to store several commands into one action, like walk or attack."""
    def __init__(self, duration, commands):
        """Create the action
           duration is the total length (in seconds) this action takes
           commands is a list of commands (rotate,move,scale) to be performed"""
        self.duration = duration
        self.commands = commands

        self.reset()

    def copy(self):
        return Action(self.duration, self.commands)

    def reset(self):
        """Reset animation."""
        self.start()

    def start(self):
        """Reset animation."""
        self.tstamp_start = time.time()
        self.tstamp_last = time.time()
        self.finished_frame = False

    def update(self, skeleton):
        """Update timestamps and execute commands relavent."""
        age = time.time() - self.tstamp_start
        if age >= self.duration:
            age = self.duration
        for i in self.commands:
            i.update(skeleton, self.tstamp_last-self.tstamp_start, age)
        self.tstamp_last = age
        if age == self.duration:
            self.reset()
            self.finished_frame = True

class Skeleton(object):
    """Basic object to store several bones."""
    def __init__(self):
        """Create the skeleton."""
        self.bones = {}

    def add_bone(self, name, start, end, parent=None, anchor=0):
        """Add a new bone
           name is the name of the bone
           start, end and anchor are just like the arguments for Bone.__init__
           parent can be None or the name of the bone this is attached to"""
        new = Bone(start, end, anchor)
        if parent:
            self.bones[parent].children.append(new)
        self.bones[name] = new
        return new

    def get(self, name):
        """Return bone <name>"""
        return self.bones[name]

    def reset(self):
        """Reset all bones."""
        for i in self.bones:
            self.bones[i].reset()

    def push(self):
        """Calculate current values of all bones."""
        for i in self.bones:
            self.bones[i].push()

class Animation(BaseSceneObject):
    """Basic object to move mesh parts ased on action commands and a skeleton."""
    def __init__(self, mesh, skeleton, commands):
        """Create the Animation object
           mesh must be a BasicMesh object, used to get the mesh parts
           skeleton must be a Skeleton object representing the mesh data
           commands must be a dict of {"name":Action} pairs"""
        BaseSceneObject.__init__(self)

        self.mesh = mesh
        self.skeleton = skeleton
        self.commands = commands

        self.action = None
        self.loop = True

        self.pos = (0,0,0)
        self.rotation = (0,0,0)
        self.scale = (1,1,1)
        self.colorize=(1,1,1,1)

    def do(self, action=None, loop=True):
        """Start an animation action
           action is the name of the action in the commands list
           loop is whether to replay the animation after finishing or not"""
        if not action == self.action:
            self.action = action
            if self.action in self.commands:
                self.commands[self.action].start()
        self.loop = loop

    def is_idle(self):
        """Returns whether any animation action is currently running."""
        if self.action in self.commands:
            if self.commands[self.action].finished_frame and (not self.loop):
                return False
        return True

    def copy(self):
        """Return a copy of the Animation."""
        com = {}
        for i in self.commands:
            com[i] = self.commands[i].copy()
        new = Animation(self.mesh, self.skeleton, com)
        new.pos = self.pos
        new.rotation = self.rotation
        new.scale = self.scale
        new.colorize = self.colorize
        new.action = self.action
        new.loop = self.loop
        return new

    def render(self, camera=None):
        """Render the Animation
           camera must be None or the camera object used to render the scene."""
        use_ani = False
        if self.action:
            if self.action in self.commands:
                command = self.commands[self.action]
                command.update(self.skeleton)
                if command.finished_frame:
                    if not self.loop:
                        self.action = None

        self.skeleton.push()

        glPushMatrix()
        x,y,z = self.pos
        glTranslatef(x,y,-z)
        a, b, c = self.rotation
        glRotatef(a, 1, 0, 0)
        glRotatef(b, 0, 1, 0)
        glRotatef(c, 0, 0, 1)
        try:
            glScalef(*self.scale)
        except:
            glScalef(self.scale, self.scale, self.scale)
        glColor(*self.colorize)

        #TODO: add outlining to active models?

        for i in self.mesh.objs:
            _pos, _rot, _sca = i.pos, i.rotation, i.scale
            if i.name in self.skeleton.bones:
                bone = self.skeleton.bones[i.name]
                npos = bone.get_center()
                x, y, z = bone.get_rotation()
                nrot = x, y, -z
                nsca = bone.scale

                i.pos = npos
                i.rotation = nrot
                i.scale = nsca

            old = tuple(i.material.color)
            r,g,b,a = old
            r2,g2,b2,a2 = self.colorize
            r *= r2
            g *= g2
            b *= b2
            a *= a2
            i.material.color = r,g,b,a
            i.render(camera)
            i.material.color = old

            i.pos, i.rotation, i.scale = _pos, _rot, _sca
        glPopMatrix()

        self.skeleton.reset()
