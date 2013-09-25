# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
from flask import abort

config = ConfigParser()

# no exceptions handling, since this crashes on startup
config.readfp(open('config.ini'))
projects = dict(config.items('projects'))

if len(projects) == 0:
    raise Exception('No projects defined')