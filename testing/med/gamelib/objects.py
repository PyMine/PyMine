import pygame
from pygame.locals import *

import math, random
import os,sys
#import psyco
import pyggel
from pyggel import *
from pyggel import particle
from pyggel.misc import ObjectGroup as Group
from pyggel.misc import ObjectInstance
#psyco.full()
pygame.mixer.set_num_channels(100)
#battlenoise = {
#    "swords":pygame.mixer.Sound((os.path.join("data", "swords.wav"))),
#    "death":pygame.mixer.Sound((os.path.join("data", "death.wav"))),
#    "arrow":pygame.mixer.Sound((os.path.join("data", "arrow.wav"))),
#    "siege":pygame.mixer.Sound((os.path.join("data", "siege.wav"))),
#}

def colliderect(a, b):
    return a[0] + a[2] > b[0] and b[0] + b[2] > a[0] and a[1] + a[3] > b[1] and b[1] + b[3] > a[1]

def collidepoint(p, r):
    if r[0] < p[0] and p[0] < r[0]+r[2]:
        if r[1] < p[1] and p[1] < r[1]+r[3]:
            return True
    return False

class Object(ObjectInstance):
    
    def __init__(self, groups):
        self.grid_color = [0, 0, 0]
        ObjectInstance.__init__(self, groups)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class GameObject(Object):
    
    def __init__(self, game, obj=None, pos=[0, 0], rotation=0, height=0, color=[1, 1, 1, 1]):
        Object.__init__(self, self.groups)
        self.game = game
        self.scene = self.game.scene
        self.pos = [pos[0], pos[1]]
        self.rotation = rotation
        self.obj = obj
        self.height = height
        self.update_obj()
    
    def update_obj(self):
        if self.obj:
            self.obj.pos = (self.pos[0], self.height, self.pos[1])
            self.obj.rotation = (self.obj.rotation[0], self.rotation, self.obj.rotation[2])
    
    def move(self, amount, rotation):
        po=0.0174532925
        self.pos[0] -= math.sin(rotation[1]*po)*amount
        self.height += math.sin(rotation[0]*po)*amount
        self.pos[1] += math.cos(rotation[1]*po)*amount
        self.update_obj()
    
    def position(self, x, y, h=None):
        self.pos[0] = x
        self.pos[1] = y
        if h:
            self.height = h
    
    def rotate(self, dx, dy, dz):
        self.obj.rotation = (self.obj.rotation[0]+dx, self.obj.rotation[1]+dy, self.obj.rotation[2]+dz)
        self.rotation = self.obj.rotation[1]
    
    def rotate_to(self, x, y, z):
        self.obj.rotation = (x, y, z)
        self.rotation = self.obj.rotation[1]
    
    def update(self):
        self.update_obj()

class Player(GameObject):
    
    def __init__(self, game):
        GameObject.__init__(self, game, obj=None, pos=[10, 15], rotation=0, height=0)
        self.old_pos = list(self.pos)
        self.speed = 0.3
        self.rel_timer = 0
        
        self.gun = Sword(self.game, self)
        self.frame = 0

        self.lives = 3
        self.score = 0
        self.health = 100
        self.attacking=False
        
    def update(self):
        self.gun.update_pos()
        self.frame += 1
        if self.frame > 360:
            self.frame = 0
        self.rel_timer -= 1
        self.old_pos = list(self.pos)

        keys = self.game.event_handler.keyboard.held
        if "w" in keys:
            self.move(self.speed, (0, -self.rotation))
        if "s" in keys:
            self.move(-self.speed, (0, -self.rotation))
        if "a" in keys:
            self.move(-self.speed, (0, -self.rotation-90))
        if "d" in keys:
            self.move(self.speed, (0, -self.rotation-90))
        if "w" in keys or "s" in keys or "a" in keys or "d" in keys:
            self.gun.height = math.sin(math.radians(self.frame)*8)/75 + self.gun.old_y
            self.gun.update_obj()
        else:
            self.gun.height = self.gun.old_y
        
        mb = self.game.event_handler.mouse.held
        if "left" in mb:
            if self.rel_timer <= 0:
              
                shotpos = [self.gun.pos[0], self.gun.height-0.1, self.gun.pos[1]]
                shotpos[0] += math.sin(math.radians(self.rotation+90))*.06
                shotpos[2] += math.cos(math.radians(self.rotation+90))*.06
                shotpos[0] += math.sin(math.radians(self.rotation))*0.75
                shotpos[2] += math.cos(math.radians(self.rotation))*0.75
                self.attacking = True
                self.gun.height+=0.1
                if self.gun.height==1.5:
                    self.gun.height-=1
                    if self.gun.height==1:
                        self.gun.height = self.gun.old_y
        if self.gun.height==self.gun.old_y:
            self.attacking=False
        
        if self.rel_timer > 5:
            self.gun.height = self.gun.old_y + 0.025
        elif self.rel_timer == 5:
            self.gun.height = self.gun.old_y
            self.frame = 0
    
    def collide(self, rect):
        #Collide n' slide.
        if collidepoint(self.pos, rect):
            #print [self.pos[0] - self.old_pos[0], self.pos[1] - self.old_pos[1]]
            if self.old_pos[0] >= rect[0]+rect[2] or self.old_pos[0] <= rect[0]:
                self.pos[0] = self.old_pos[0]
            if self.old_pos[1] >= rect[1]+rect[3] or self.old_pos[1] <= rect[1]:
                self.pos[1] = self.old_pos[1]

class Sword(GameObject):
    
    def __init__(self, game, player):
        height = -0.25
        GameObject.__init__(self, game, obj=pyggel.mesh.OBJ("data/sword.obj", colorize=[0.2, 0.2, 0.2, 1]), 
                            pos=[10, 15], rotation=0, height=height)
        self.player = player
        self.obj.scale = 2.0
        self.rotate_to(0, 0, 0)
        self.scene.add_3d(self.obj)
        self.update_pos()
        self.old_y = height
    
    def update_pos(self):
        self.rotate_to(0, -self.player.rotation, 0)
        self.update_obj()
        self.pos = list(self.player.pos)
        self.move(0.175, (0, -self.player.rotation-90))
        self.move(1.0, (0, -self.player.rotation))
        self.update_obj()

class Enemy(GameObject):
    
    main_obj = None
    
    def __init__(self, game, pos, type):
        if not self.main_obj:
            if type == "Soldier":
                self.main_obj = pyggel.mesh.OBJ("data/enemy_soldier.obj", pos=pos, colorize=[0.3, 0.3, 0.3, 1])
            elif type == "Archer":
                self.main_obj = pyggel.mesh.OBJ("data/enemy_soldier.obj", pos=pos, colorize=[0.3, 0.3, 0.3, 1])
            elif type == "Siege":
                self.main_obj = pyggel.mesh.OBJ("data/enemy_soldier.obj", pos=pos, colorize=[0.3, 0.3, 0.3, 1])

        obj = self.main_obj.copy()
        GameObject.__init__(self, game, obj=obj, pos=pos, rotation=0, height=-2)
        self.obj.scale = 1.25
        self.scene.add_3d(self.obj)
        self.old_pos = list(self.pos)
        self.hit_timer = 0
        self.obj.colorize = [0.3, 0.4, 0.5, 1]
        self.home_in = False
        if type == "Soldier":
            self.hp = 30
            self.maxhp = 30
            self.obj.colorize = [0,0,0,1]
            self.type="Soldier"
            self.ammo=0
        elif type == "Archer":
            self.hp = 15
            self.maxhp = 15
            self.obj.colorize = [0,1,0,1]
            self.type="Archer"
            self.ammo=30
        elif type == "Siege":
            self.hp = 50
            self.maxhp = 50
            self.obj.colorize = [0,0,1,0]
            self.type="Siege"
            self.ammo=50
        self.dead=False
        
    def update(self):
        self.hit_timer -= 1
        if self.hit_timer > 0:
            self.obj.colorize = [1, 0, 0, 1]
        else:
            self.obj.colorize = [140, 140, 140, 255]
        self.rotate_to(0, self.obj.rotation[1]+3, 0)
        self.move(0.1, (0, 180+self.obj.rotation[1]))
        if self.hp<self.maxhp:
            self.hp+=.01
        else:
            pass
        self.update_obj()
            
    
    def kill(self):
        if self.alive():
            GameObject.kill(self)
            self.scene.remove_3d(self.obj)
            for i in range(3):
                pos = list(self.obj.pos)
                pos[0] += random.choice([-0.5, -0.4, -0.3, -0.2, -0.1])*random.choice([1, -1])
                pos[1] += random.choice([-0.3, -0.2, -0.1])*random.choice([1, -1])
                pos[2] += random.choice([-0.5, -0.4, -0.3, -0.2, -0.1])*random.choice([1, -1])
            Killed(self.game, [pos[0], pos[2]], pos[1])
            self.game.enemy_deaths+=1
    
    def collide(self, point):
        r = [self.pos[0] - 1.5, self.pos[1] - 1.5, 3.0, 3.0]
        if collidepoint(point, r) and self.hit_timer <= 0:
            self.hit_timer = 4
            self.hp -= 5
            self.game.player.score += 1
            if self.hp <= 0:
                self.kill()
                self.game.player.score += 15
            return 1

    def wall_collide(self, rect):
        #Collide n' slide.
        if collidepoint(self.pos, rect):
            #print [self.pos[0] - self.old_pos[0], self.pos[1] - self.old_pos[1]]
            if self.old_pos[0] >= rect[0]+rect[2] or self.old_pos[0] <= rect[0]:
                self.pos[0] = self.old_pos[0]
            if self.old_pos[1] >= rect[1]+rect[3] or self.old_pos[1] <= rect[1]:
                self.pos[1] = self.old_pos[1]
    def shoot(self):
        if self.type == "Siege" or self.type == "Archer":
            if self.ammo>0:
                self.rel_timer-=1
                if self.rel_timer<=0 :
               
                    shotpos = [self.pos[0], self.height-0.1, self.pos[1]]
                    if self.type=="Archer":
                        Shot(self.game, [shotpos[0], shotpos[2]],  self.obj.rotation[1]+180, shotpos[1],"Arrow",self)
                        #battlenoise["arrow"].play(0,0,0)
                        self.rel_timer=7
                    elif self.type=="Siege":
                        Shot(self.game, [shotpos[0], shotpos[2]],  self.obj.rotation[1]+180, shotpos[1],"Siege",self)
                        #Fire(self.game, shotpos,"Siege",.001)
                        #battlenoise["siege"].play(0,0,0)
                        self.rel_timer=15
                        
                    self.ammo-=1

class Killed(GameObject):
    
    def __init__(self, game, pos, height):
        GameObject.__init__(self, game, pyggel.image.Image3D("data/dead.png"), pos=pos, height=height+1)
        self.scene.add_3d_blend(self.obj)
        self.alpha = 1.0
        self.obj.scale = 1.5
       
    def kill(self):
        if self.alive():
            Object.kill(self)
            self.scene.remove_3d_blend(self.obj)
        
    def update(self):
        #self.obj.scale += 0.1
        #self.rotate(0, 0, 2)
        #self.alpha -= 0.04
        #if self.alpha < 0:
            #self.kill()
        self.obj.colorize = (1.0, 1.0, 1.0, self.alpha)

class Wall(Object):
    
    def __init__(self, game, pos):
        Object.__init__(self, self.groups)
        self.pos = pos

class Edge(GameObject):
    def __init__(self,game,pos):
        self.type="edge"
        obj=pyggel.image.Image3D("data/edge.png", pos=pos, colorize=[0.3, 0.3, 0.3, 1])
        GameObject.__init__(self,game,obj=obj,pos=pos, rotation=0, height=0)
        self.scene.add_3d(self.obj)
        self.old_pos = list(self.pos)

class Tree(GameObject):
    main_obj=None
    def __init__(self, game, pos):  
        self.type="tree"
        meshes=[pyggel.mesh.OBJ("data/tree1.obj", pos=pos, colorize=[0.3, 0.3, 0.3, 1])]
                #pyggel.mesh.OBJ("data/tree3.obj", pos=pos, colorize=[0.3, 0.3, 0.3, 1]),
                #pyggel.mesh.OBJ("data/tree2.obj", pos=pos, colorize=[0.3, 0.3, 0.3, 1])]
        obj = meshes[random.randint(0,0)].copy()
        GameObject.__init__(self, game, obj=obj, pos=pos, rotation=0, height=0)
        self.scene.add_3d(self.obj)
        self.old_pos = list(self.pos)
        self.obj.scale=.1

class Raindrop(GameObject):
    def __init__(self, game):
        GameObject.__init__(self, game, pyggel.image.Image3D("data/raindrop.png"),
                            pos=[random.randint(0,game.maxes[0]),random.randint(0,game.maxes[1])],
                            height=random.randint(0,40))
        #self.obj.scale = [5, 0.75, 0.75]
        self.scene.add_3d_blend(self.obj)
        self.speed = 3.0
        self.obj.colorize = [.36,0.4,1,.5]
        self.height=random.randint(0,40)
        self.obj.scale=.5
    def kill(self):
        if self.alive():
            GameObject.kill(self)
            self.scene.remove_3d(self.obj)
        
    def fall(self):
        self.height-=1
        if self.height<-10:
            prob=random.choice([True,True,True,False])

class Fire(pyggel.particle.Behavior3D):
    """This very simple class controls how our emitter works and what kind of particles it makes.
       This behavior uses the Image3D particles..."""
    def __init__(self, emitter):
        pyggel.particle.Behavior3D.__init__(self, emitter) #first, we initialize the base Behavior

        self.image = pyggel.image.Image3D("data/fire.png") #here we load our image for the particles
        self.image.scale = .5 #scale the image down a bit
        self.image.pos = self.emitter.pos #set it's starting position
        self.image.colorize = (1,1,1,.5) #starting colorize
        self.particle_lifespan = 20 #this is how long each particle will live
        #considering our emitter_update call generates 5 particles a frame, and they each last 20 frames
        #we will have about 100 particles once the emitter gets going...

    def get_dimensions(self):
        #You can ignore this, basically this calculates the maximum bounds of the emitter effect.
        return 2, 6, 2 #max/abs(min) directions(x,y,z) * particle_lifespan

    def emitter_update(self):
        #this gets called every frame by the emitter, so we can generate new particles
        for i in xrange(5):
            self.emitter.particle_type(self.emitter, self) #self.emitter.particle_type is simply the particle class to use

    def register_particle(self, part):
        #This gets called by every particle when it is created
        #here we set up it's attributes to make it "work" correctly
        dx = randfloat(-.08, .08)
        dy = randfloat(.15, .3)
        dz = randfloat(-.08, .08)

        rot = random.randint(-25, 25)

        #beyond the basic pos, rot, colorize attributes that all Images have
        #each particle also has an extra_data dictionary, where you can put things specific
        #to your particles.
        #here we put things like rot and direction into extra_data
        part.extra_data["dir"] = (dx, dy, dz)
        part.extra_data["rot"] = rot

        x, y, z = self.emitter.pos

        part.image.pos = x+dx*randfloat(1, 2), y, z+dz*randfloat(1, 2)

    def particle_update(self, part):
        #this is called every frame for each particle to update theme
        pyggel.particle.Behavior3D.particle_update(self, part)
        x, y, z = part.image.pos
        #here we move the particle based on it's direction:
        a, b, c = part.extra_data["dir"]
        x += a
        y += b
        z += c

        b -= .015
        part.extra_data["dir"] = a, b, c
        part.image.pos = x, y, z

        x, y, z = part.image.rotation
        #here we rotate the image around...
        z -= part.extra_data["rot"]
        part.image.rotation = x, y, z

        #fade the image
        r, g, b, a = part.image.colorize
        a -= .5/20
        part.image.colorize = r, g, b, a

        part.image.scale -= .025

class Impact(GameObject):
    
    def __init__(self, game, pos, height,type):
        if type=="Arrow":
            GameObject.__init__(self, game, pyggel.image.Image3D("data/arrowimpact.png"), pos=pos, height=height)

        self.scene.add_3d_blend(self.obj)
        self.alpha = 1.0
        self.obj.scale = 0.1
        self.type=type
    def kill(self):
        if self.alive():
            Object.kill(self)
            self.scene.remove_3d_blend(self.obj)
        
    def update(self):
        self.alpha -= 0.04
        if self.alpha < 0:
            self.kill()
        self.obj.colorize = (1.0, 1.0, 1.0, self.alpha)
        
class Shot(GameObject):
    main_obj = None
    def __init__(self, game, pos, angle, height,type,parent):
        if not self.main_obj:
            if type=="Arrow":
                self.main_obj = pyggel.mesh.OBJ("data/arrow.obj",colorize=[1,0,1,.5])
                self.speed = 3.0
            elif type=="Siege":
                self.main_obj = pyggel.mesh.OBJ("data/siege.obj",colorize=[1,0,0,1])
                self.speed = 5.0
                
        obj = self.main_obj.copy()
        GameObject.__init__(self, game, obj=obj, pos=pos, rotation=angle+90, height=height)
        self.scene.add_3d(self.obj)
        self.height=height
        self.parent=parent
        if type=="arrow":
            self.obj.scale = .1
        elif type=="Siege":
            self.scene.add_3d(self.emitter)
        self.type=type
        self.living=True
        self.dead=False
    def kill(self):
        if self.alive():
            GameObject.kill(self)
            self.scene.remove_3d(self.obj)
            
    def move_increment(self):
        self.move(self.speed/5, (0, self.rotation-90))
    def collide(self, rect):
        if collidepoint(self.pos, rect):
            if self.living:
                self.dead=True
                if self.type=="Arrow":
                    Impact(self.game, self.pos, self.height,"Archer")
                    #combatsnds["plashit"].play(0,0,0)
                elif self.type=="Siege":
                    SiegeExplosion(self.game, self.pos, self.height,self.parent)
                    #combatsnds["rockethit"].play(0,0,0)
                self.living=False
            return True

class SiegeExplosion(GameObject):
    
    def __init__(self, game, pos, height,parent):
        img = pyggel.image.GridSpriteSheet3D("data/explosion.png", (3,4), 10)
        img.loop(False)
        GameObject.__init__(self, game, img, pos=pos, height=height)
        self.scene.add_3d_blend(self.obj)
        self.timer=50
        self.game=game
        self.type="burning"
        self.parent=parent
    def kill(self):
        if self.alive():
            Object.kill(self)
            self.scene.remove_3d_blend(self.obj)
        
    def update(self):
        self.timer-=1
        for baddie in self.game.baddies:
            if baddie.collide(self.pos) and self.parent!=baddie:
                self.kill()
                baddie.hit_timer = 4
                baddie.hp -= 10
                print "collide"
        r = [self.pos[0]-2.0, self.pos[1]-2.0, 4.0, 4.0]
        if self.game.player.collide(r) and self.parent!=self.game.player:
            if self.game.player.shields<=0:
                self.game.player.health-=1
                if self.game.player.health==2:
                    self.game.player.scene.remove_2d(self.game.player.hgs[0])
                elif self.game.player.health==1:
                    self.game.player.scene.remove_2d(self.game.player.hgs[1])
                
            else:
                self.game.player.shields-=10
                self.game.player.woundcounter+=.2
          
            self.game.player.shieldtimer=0
        if self.timer<=0:
            self.kill()
