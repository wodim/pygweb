# -*- coding: utf-8 -*-
from flask import request, render_template, flash, session, redirect, url_for, abort, Response
from flask_classy import FlaskView, route

from ..config import projects

class ReposView(FlaskView):
    route_base = '/'

    @route('/')
    def get(self):
        my_projects = [project for project in projects.keys()]

        return render_template('reposview.html', list=my_projects)