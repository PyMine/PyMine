#!/usr/bin/env python
import os
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import time


global current_dir
current_dir = os.path.abspath('')
game_path = os.path.join(current_dir,"game")
texture_path = os.path.join(game_path,"textures")
save_path = os.path.join(game_path,"saves")
mod_path = os.path.join(game_path,"mods")
config_path = os.path.join(game_path,"config.conf")

sys.path += ['game']
os.chdir(current_dir)
from lib import main_game

print("this is from the launcher")
launcher_vars = {
"game" : game_path,
"texture" : texture_path,
"save" : save_path,
"mod" : mod_path,
"config" : config_path
}
main_game.main(launcher_vars)
