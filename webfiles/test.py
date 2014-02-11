#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
print sys.path
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime