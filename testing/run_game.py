#! /usr/bin/env python

import sys, os

sys.path.insert(0, os.path.split(sys.path[0])[0])

import pyggel
from pyggel import *

from gamelib import main
main.main()

