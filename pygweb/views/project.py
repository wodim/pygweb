# -*- coding: utf-8 -*-
import random, string
import os, magic
from datetime import datetime

from flask import request, render_template, flash, session, redirect, url_for, abort, Response
from flask.ext.classy import FlaskView, route

from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter

from ..config import projects 

class ProjectView(FlaskView):
    route_base = '/'

    @route('/<path:fullurl>')
    def get(self, fullurl):
        params = fullurl.strip('/').split('/')

        # i don't check for IndexError: if params[0] wasn't set already, we would not be in this view
        project = params[0]
        if len(params) < 2:
            return redirect(url_for('ProjectView:get', fullurl='%s/%s' % (params[0], 'blob')))
        
        if not project in projects:
            abort(404)
        
        # i don't check for IndexError: i already trapped this in the "if" above
        method = params[1]
        if method not in ['blob', 'raw']:
            abort(404)
        
        path = os.path.normpath('/'.join(params[2:]))
        full_path = os.path.normpath('%s%s' % (projects[project], path))
        
        # directory escaping
        if '..' in full_path:
            abort(403)
        
        # !TODO links may be a security problem. but this should be fixed
        if not os.path.exists(full_path) or os.path.islink(full_path):
            abort(404)
            
        output = self._discerner(project, method, path, full_path)
        if output is None:
            abort(500)
        
        return output
        
    def _discerner(self, project, method, path, full_path):            
        if method == 'blob':
            if os.path.isdir(full_path):
                dirs = [{'name': '..', 'href': '..', 'type': 'dir'}]
                files = []
                
                entries = os.listdir(full_path)
                entries.sort()
                for entry in entries:
                    this_path = os.path.normpath('%s/%s' % (full_path, entry))
                    try:
                        mimetype = magic.from_file(this_path, mime=True)
                        size = os.path.getsize(this_path)
                        unit = 'bytes'
                        if size > 2048: # 2kb min
                            size /= 1024
                            unit = 'KB'
                            if size > 1024:
                                size /= 1024
                                unit = 'MB'
                        size = '%s %s' % (size, unit)
                        mtime = datetime.fromtimestamp(os.path.getmtime(this_path))
                    except IOError:
                        mimetype = None
                    if os.path.isdir(this_path):
                        dirs.append({'icon': url_for('static', filename='folder.png'), 'name': entry, 'href': '/%s/blob/%s/%s/' % (project, path, entry), 'type': 'dir', 'mimetype': mimetype, 'size': size, 'mtime': mtime})
                    elif os.path.isfile(this_path):
                        files.append({'icon': url_for('static', filename='file.png'), 'name': entry, 'href': '/%s/blob/%s/%s' % (project, path, entry), 'type': 'file', 'mimetype': mimetype, 'size': size, 'mtime': mtime})

                list = dirs + files

                return render_template('listview.html', list=list, path=path)
            elif os.path.isfile(full_path):
                with open(full_path, 'r') as file:
                    content = file.read()
                
                mimetype = magic.from_buffer(content, mime=True)
                src = '/%s/raw/%s' % (project, path)
                if mimetype.startswith('text/') or mimetype == 'application/xml':
                    code = highlight(content, guess_lexer(content), HtmlFormatter(noclasses=True))
                    return render_template('htmlview.html', content=code, path=path)
                elif mimetype.startswith('image/'):
                    return render_template('imageview.html', src=src, path=path)
                else:
                    return render_template('rawview.html', src=src, path=path)
        elif method == 'raw':
            if os.path.isfile(full_path):
                with open(full_path, 'r') as file:
                    content = file.read()
                
                mimetype = magic.from_buffer(content, mime=True)
                if mimetype.startswith('text/'): # this is an exception
                    mimetype = 'text/plain'
                    
                return Response(content, mimetype=mimetype)