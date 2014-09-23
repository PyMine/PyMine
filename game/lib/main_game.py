import pygame
import sys
from lib import test_game_core

class game(object):
    # small hack thing for the moment so i can do some testing to get
    # a better control registration going
    pass

game.keys_pressed = {
"left" : False,
"right" : False,
"forwards" : False,
"backwards" : False
}
game.config_keymap = {
"a" : "left",
"d" : "right",
"w" : "forwards",
"s" : "backwards"
}

def main():
    
    pygame.init()
    screen = pygame.display.set_mode([800, 600], pygame.OPENGL | pygame.DOUBLEBUF)
    print(pygame.display.Info())
    #pygame.display.set_icon() #sets the icon for the game
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
