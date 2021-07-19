from flask import (
    g, request, session, jsonify
)

# from mdisc.db import get_db
from .api import Library
from . import library_bp

library = Library()

#Library
@library_bp.route('/list')
def list():
    max = request.args.get('max',type=int)
    session['lib_max'] = max
    session['lib_page'] = session.get('lib_page', 1) 
    # session['lib_pg_start'] = session.get('lib_pg_start', 0) 
    # session['lib_pg_end'] = session.get('lib_pg_end', max)
    files = library.list(max,session['lib_page'],'lib_page')
    return jsonify(files)

@library_bp.route('/load') 
def load():
    res = library.load()
    return jsonify(res)

@library_bp.route('/scan')
def scan():
    res = library.scan()
    return jsonify(res)

@library_bp.route('/enqueue') #queue
def queue():
    uri = request.args.get('uri')
    res = library.queuetrack(uri)
    return jsonify(res)

@library_bp.route('/reset')
def reset():
    # max = request.args.get('max',type=int)
    res = library.reset()
    return jsonify(res)