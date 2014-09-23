#!/usr/bin/env python
import os
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import time


global current_dir
current_dir = os.path.abspath('')
game_path = os.path.join(current_dir,"game")

sys.path += ['game']
os.chdir(current_dir)
from lib import main_game
from lib import test_game_core

print("this is from the launcher")
main_game.main(test_game_core)
