# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, g, flash, session, abort

from pygweb.views import ProjectView

import random, string

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    abort(404)

ProjectView.register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)