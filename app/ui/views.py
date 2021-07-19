from flask import render_template, session, request, redirect

from . import ui
import uuid
from ..api import api
queue = api.Queue()

@ui.route('/')
def index():
    id = uuid.uuid4().hex
    session['uuid'] = session.get('uuid', id)
    queue.adduser()    
    return render_template('ui/playlist.html')
