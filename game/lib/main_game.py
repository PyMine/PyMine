import pygame
import sys
import os
from lib import test_game_core

class game(object):
    # small hack thing for the moment so i can do some testing to get
    # a better control registration going
    pass

game.keys_pressed = {
"left" : False,
"right" : False,
"forward" : False,
"backward" : False
}
game.config_keymap = {
"a" : "left",
"d" : "right",
"w" : "forward",
"s" : "backward"
}

def main(launcher_vars):
    
    pygame.init()
    icon_path = os.path.join(launcher_vars["texture"],"icon.png")
    seticon(icon_path)
    screen = pygame.display.set_mode([800, 600], pygame.OPENGL | pygame.DOUBLEBUF)
    print(pygame.display.Info())
    pygame.display.set_caption("PyMine")
    while 1:
        for event in pygame.event.get():
            key=pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.type == pygame.KEYDOWN:
                    current_key = event.key
                    keyname = pygame.key.name(current_key)
                    if keyname in game.config_keymap:
                        gameaction = game.config_keymap[keyname]
                        game.keys_pressed[gameaction] = True
                if event.type == pygame.KEYUP:
                    if keyname in game.config_keymap:
                        gameaction = game.config_keymap[keyname]
                        game.keys_pressed[gameaction] = False
                print(game.keys_pressed)
            
            if event.type == pygame.QUIT:
                    sys.exit()
    print("this is from the maingame file")
    test_game_core.main()

def seticon(iconname):
    """
    give an iconname, a bitmap sized 32x32 pixels, black (0,0,0) will be alpha channel
    
    the windowicon will be set to the bitmap, but the black pixels will be full alpha channel
     
    can only be called once after pygame.init() and before somewindow = pygame.display.set_mode()
    """
    #i borrowed this from the pygame comments on the set icon function, thanks anon!
    icon=pygame.Surface((256,256))
    icon.set_colorkey((0,0,0))
    rawicon=pygame.image.load(iconname)
    for i in range(0,256):
        for j in range(0,256):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)
    