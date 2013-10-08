# -*- coding: utf-8 -*-
from flask import request, render_template, flash, session, redirect, url_for, abort, Response
from flask.ext.classy import FlaskView, route

from ..config import projects 

class ReposView(FlaskView):
    route_base = '/'

    @route('/')
    def get(self):
        list = []
        for project in projects.keys():
            list.append(project)
            
        return render_template('reposview.html', list=list)