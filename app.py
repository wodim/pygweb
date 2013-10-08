# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, g, flash, session, abort

from pygweb.views import *

import random, string

app = Flask(__name__)
app.debug = True

ReposView.register(app)
ProjectView.register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)