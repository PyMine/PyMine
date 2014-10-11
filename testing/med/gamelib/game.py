#! /usr/bin/env python

#Python imports
import sys, os
import math, random

#Import le pygame
import pygame
from pygame.locals import *

#Import the best gl library ever :-D
import pyggel
from pyggel import *

#Import local modules
from objects import *

#You're on the GRID! :-O
battle1 =         """
                     bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
                     b+                                                   b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b              w                                     b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                  1                 b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                  1                 b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     b                                                    b
                     bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"""

battle1 = """
             bbbbbbbbbbbbbbbbbbbbbbbbb
             b+                      b
             b                       b
             b                       b
             b                       b
             b                       b
             b              1        b
             b              2        b
             b                       b
             bbbbbbbbbbbbbbbbbbbbbbbbb"""

battle11 = """
wwwwwwwwwwwwwwwwwwww
w           t      +
w                  
w           t       
w                         
        t
                    t
w           t                      
w                                   
w                   
w w     1                              
w w                                   
w1wwwwwwwwww       w                             
w*w1    2      w   w                    
w w        w  2    w
w1w   w            w
w w   2  w   1 w   w 
w w                w
w wwwwwwwwwwwwwwwwww
w w www      1 www   
w www     w      ww 
w1ww              wwwwwww
w ww  1     1   w    1  w      
w w               w1www1w
w w   2   1    1 ww w 31w
w1             www  w   w
wwwwwwwwwwwwwwwwww wwwwww
                 w w
                 w w  
                 w w
                 w wwww 
                 w    w 
                 wwww w"""


battle2 = battle1
battle3 = battle1

#Level parsing function parsing levels
def level_parse(game, scene, map):
    
    #Static objects. Woo woo, built for speeeeeeed
    static = []
    walls = []
    switches=[]
    x = y = 0 #OMGZ!
    if map==battle1:
        height = 75
        width = 54
    elif map==battle2:
        height = 33
        width = 57
    elif map==battle3:
        height = 33
        width = 57
    max_y = height-1
    mx = width/2.0*5
    my = height/2.0*5
    mwh = max((width, height))
    game.maxes=[width*5,height*5]
    game.mins=[-20,-20]
    if map in(battle1):
        quad = pyggel.geometry.Plane(mwh*5,pos=[mx,-2.5,my],texture=pyggel.data.Texture("data/grass1.png"),
                                     tile=mwh,rotation=(90,0,0),hide_faces=["front"])
        static.append(quad)
        rain=False
        if rain==True:
            skyball=pyggel_geometry.Skybox("data/rainy.png")
        else:
            skyball = pyggel.geometry.Skybox("data/daytime.png")
        skyball = pyggel.geometry.Skybox("data/daytime.png")
        scene.add_skybox(skyball)
        pyggel.view.set_fog(True)
        pyggel.view.set_fog_color((0.5,0.5,0.5,1))
        pyggel.view.set_fog_depth(1, 60)
    elif map in(battle2):
        quad = pyggel.geometry.Plane(mwh*5,pos=[mx,-2.5,my],texture=pyggel.data.Texture("data/grass1.png"),
                                     tile=mwh,rotation=(90,0,0), hide_faces=["front"])
        static.append(quad)
        rain=False
        if rain==True:
            skyball=pyggel_geometry.Skybox("data/rainy.png")
        else:
            skyball = pyggel.geometry.Skybox("data/daytime.png")
        skyball = pyggel.geometry.Skybox("data/daytime.png")
        scene.add_skybox(skyball)
        pyggel.view.set_fog(False)
        #pyggel.view.set_fog_color((.01, .01, .01, .05))
        #pyggel.view.set_fog_depth(1, 60)
    elif map in(battle3):
        quad = pyggel.geometry.Plane(mwh*5,pos=[mx,-2.5,my],texture=pyggel.data.Texture("data/grass1.png"),
                                     tile=mwh,rotation=(90,0,0), hide_faces=["front"])
        static.append(quad)
        rain=False
        if rain==True:
            skyball=pyggel_geometry.Skybox("data/rainy.png")
        else:
            skyball = pyggel.geometry.Skybox("data/daytime.png")
        scene.add_skybox(skyball)
        pyggel.view.set_fog(False)
        
    
    
    for line in map.split("\n"):
        for char in line:
            
            #Walls
            if char in("W", "w", "b"):
                if map in(battle1):
                    if char=="w":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone2.png"))
                    elif char=="W":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone1.png"))
                    elif char=="b":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone1.png"))
                elif map in(battle2):
                    if char=="w":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone2.png"))
                    elif char=="W":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone1.png"))
                    elif char=="b":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone1.png"))
                elif map in(battle3):
                    if char=="w":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone2.png"))
                    elif char=="W":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone1.png"))
                    elif char=="b":
                        box = pyggel.geometry.Cube(5, texture=data.Texture("data/stone1.png"))
                box.pos=(x*5,0,y*5)
                static.append(box)
                walls.append(Wall(game, [box.pos[0], box.pos[2]], ))

            enemy_deaths=0
            if char=="+":
                game.player.pos=[x*5,y*5]
            elif char == "1":
                Enemy(game, [x*5, y*5], "Soldier")
                enemy_deaths+1
            elif char == "2":
                Enemy(game, [x*5, y*5], "Archer")
                enemy_deaths+1
            elif char == "3":
                Enemy(game, [x, y], "Siege")
                enemy_deaths+1
            elif char == "t":
                walls.append(Tree(game, [x*5, y*5]))
                
                
        #Positioning
            x += 1
        y += 1
        x = 0
    #if map in (mission2):
     #   for x in range(200):
      #      Raindrop(game)
    #Raindrop(game)
    
    
    return static, walls, enemy_deaths, rain

class Game(object):
    
    def __init__(self):

        #Vee must handle ze FPS for ze FPS!
        self.clock = pygame.time.Clock()
        
        #Disable fog. We ain't in a blasted harbor, RB[0]!
        pyggel.view.set_fog(False)
        pyggel.view.set_fog_color((0, .6, .5, .5))
        pyggel.view.set_fog_depth(1, 60)
        
        #Create a First Person camera
        self.camera = pyggel.camera.LookFromCamera((0,0,-10))
        
        #Create a light. All good little GL apps should have light.
        light = pyggel.light.Light((50,300,50), (0.5,0.5,0.5,1),
                                  (1,1,1,1), (50,50,50,10),
                                  (0,0,0), True)
        
        #Create the scene, and apply the light to it.
        self.scene = pyggel.scene.Scene()
        self.scene.add_light(light)

        #Keep the mouse in the window, and make it disssssappear! Mwahahaha!
        self.grabbed = 1
        pygame.event.set_grab(self.grabbed)
        pygame.mouse.set_visible(0)
        
        #Create starting objects
        self.objects = Group()
        self.shots = Group()
        self.baddies = Group()
        self.walls = Group()
        self.raindrops = Group()
        Player.groups = [self.objects]
        Sword.groups = [self.objects]
        Shot.groups = [self.objects, self.shots]
        Enemy.groups = [self.objects, self.baddies]
        Killed.groups = [self.objects]
        Wall.groups = [self.objects, self.walls]
        Impact.groups = [self.objects]
        Tree.groups = [self.objects]
        Raindrop.groups = [self.objects,self.raindrops]
        SiegeExplosion.groups=[self.objects]
        Edge.groups=[self.objects]
        
        
        self.player = Player(self)
        self.sword = Sword(self, self.player)
        #self.overlay = pyggel.image.Image("data/screen.png", pos=[0, 0])
        #self.overlay.scale = 1.5
        #self.overlay.colorize = [0, 1, 1, 0.1]
        #self.scene.add_2d(self.overlay)
        self.hudmask = pyggel.image.Image("data/helmet.png", pos=[0, 0])
        self.scene.add_2d(self.hudmask)
        #self.targeter = pyggel.image.Image("data/target.png", pos=[400-32, 300-32])
        #self.scene.add_2d(self.targeter)
        self.font = pyggel.font.MEFont("data/font.ttf", 32)
        self.text1 = self.font.make_text_image("", (0, 255, 0))
        self.text1.pos = (50, 10)
        self.scene.add_2d(self.text1)
        self.battle = 1
        
        #self.sky = pyggel.geometry.Skyball(texture=pyggel.image.Texture("data/ceiling.png")) #
        #self.scene.add_skybox(self.sky)
        
        #parse ze level
        if self.battle == 1:
            static, self.walls._objects, self.enemy_deaths_max, self.rain= level_parse(self, self.scene,battle1)
            self.message = self.font.make_text_image("Battle 1",(0,0,0))
            self.info  = self.font.make_text_image("Enemys to the ____",(0,0,0))
        elif self.battle == 2:
            static, self.walls._objects, self.enemy_deaths_max, self.rain = level_parse(self, self.scene,battle1)
            self.message = self.font.make_text_image("Battle 2",(0,0,0))
            self.info  = self.font.make_text_image("Enemys to the ____",(0,0,0))
        elif self.battle == 3:
            static, self.walls._objects, self.enemy_deaths_max, self.rain = level_parse(self, self.scene,battle1)
            self.message = self.font.make_text_image("Battle 3",(0,0,0))
            self.info  = self.font.make_text_image("Enemys to the ____",(0,0,0))
        
        self.message.pos=[50,650]
        self.info.pos= [50,30]
        self.scene.add_3d(pyggel.misc.StaticObjectGroup(static))
        self.scene.add_2d(self.message)
        self.scene.add_2d(self.info)
        self.event_handler = pyggel.event.Handler()
        
        #Used for bobbing up and down. No I will not be less vague.
        self.frame = 0

        self.enemy_deaths=0
    
    def update_camera_pos(self):
        amt = pygame.mouse.get_rel()
        self.player.rotation += amt[0]/8.0
        self.camera.roty = self.player.rotation
        self.camera.rotx +=amt[1]/8.0
        if self.camera.rotx<-100:
            self.camera.rotx -=amt[1]/8.0
        elif self.camera.rotx>62:
            self.camera.rotx -=amt[1]/8.0
        self.camera.posz = self.player.pos[1]
        self.camera.posx = self.player.pos[0]
        self.camera.posy = self.player.height
    
    def do_input(self):
        self.event_handler.update()
        if self.event_handler.quit:
            self.running = False
        if K_ESCAPE in self.event_handler.keyboard.hit:
            self.running = False
        if " " in self.event_handler.keyboard.hit:
            self.grabbed ^= 1
        if K_q in self.event_handler.keyboard.hit:
            pyggel.misc.save_screenshot("screenshot.png")

    def do_update(self):
        
        #Loop the frame at 360.
        self.frame += 1
        if self.frame > 360:
            self.frame = 0
        if self.rain==True:
            Raindrop(self)
        
        self.clock.tick(60)

        s = "Health: %s  Score: %s   Lives: %s  FPS: %s"%(self.player.health, self.player.score,
                                                       self.player.lives, int(self.clock.get_fps()))
        self.text1.text = s
        
        self.update_camera_pos()
        for o in self.objects:
            o.update()

        walls = []
        for w in self.walls:
            r = [w.pos[0]-3.0, w.pos[1]-3.0, 6.0, 6.0]
            self.player.collide(r) 
        for s in self.shots:
            collidables = []
            for w in self.walls:
                area = [s.pos[0]-10, s.pos[1]-10, 20, 20]
                if collidepoint(w.pos, area):
                    collidables.append(w)
            for i in xrange(5):
                s.move_increment()
                for w in collidables:
                    r = [w.pos[0]-3.0, w.pos[1]-3.0, 6.0, 6.0]
                    s.collide(r)
            for b in self.baddies:
                if b.collide(s.pos):
                    s.kill()
        x=0
        for b in self.baddies:
            r = [b.pos[0] - 20, b.pos[1] - 20, 40, 40]
            line = [b.pos[0], b.pos[1]]
            home_in = False
            collidables = []
            wr = [b.pos[0] - 15, b.pos[1] - 15, 30, 30]
            for w in self.walls:
                if collidepoint(w.pos, wr):
                    collidables.append(w)
            line[0] += math.sin(math.radians(b.obj.rotation[1]))*1
            line[1] += math.cos(math.radians(b.obj.rotation[1]))*1
            r2 = [self.player.pos[0] - 5, self.player.pos[1] - 5, 10, 10]
            if collidepoint(line, r2):
                home_in = True
            if collidepoint(self.player.pos, r) or home_in:
                x = self.player.pos[0] - b.pos[0]
                y = self.player.pos[1] - b.pos[1]
                angle = math.atan2(-y, x)
                angle = 90-(angle * 180.0)/math.pi
                b.obj.rotation = (b.obj.rotation[0], angle, b.obj.rotation[2])
            for w in collidables:
                r = [w.pos[0]-3.0, w.pos[1]-3.0, 6.0, 6.0]
                b.wall_collide(r)
            if colliderect(r2, r) and self.player.attacking == False:
                self.player.health-=1
            elif colliderect(r2, r) and self.player.attacking == True:
                b.hp-=1
            else:
                pass

            if b.hp<=0:
                b.hp=0
                b.kill()
            if self.player.health<=0:
                self.player.health=0
                self.died()

            if self.enemy_deaths==self.enemy_deaths_max:
                self.battle+1
    def do_draw(self):
        
        #And pyggel doth draw.
        pyggel.view.clear_screen()
        self.scene.render(self.camera)
        pyggel.view.refresh_screen()

    def main_loop(self):
        
        #Loop de loop
        self.running = True
        while self.running:
            self.do_input()
            self.do_update()
            self.do_draw()

        pygame.event.set_grab(False)

    def run(self):
        self.main_loop()
