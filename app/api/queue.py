
from flask import (
    g, request, session, jsonify
)
import uuid
# from mdisc.db import get_db
from .api import Queue
from . import queue_bp

queue = Queue()

# Queuelist
@queue_bp.route('/list')
def getrack(): 
    max = request.args.get('max',type=int)
    session['q_page'] = session.get('q_page',1)
    # session['q_pg_start'] = 1
    # session['q_pg_end'] = session.get('q_pg_end', max) 
    tracks = queue.list(max,session['q_page'],'q_page')  
    res = jsonify(tracks)
    return res  

# @queue_bp.route('/update')
# def update():
#     res = queue.update()
#     return jsonify(res)

@queue_bp.route('/online')
def online():
    res = queue.online()
    return jsonify(res)

@queue_bp.route('/getvote')
def getvote():
    res = queue.getvote()
    return jsonify(res)

@queue_bp.route('/delete')
def delete():
    # id = request.args.get('id')
    res = queue.delete()
    return jsonify(res)

@queue_bp.route('/resetdel')
def resetdel():
    res = queue.reset_del()
    return jsonify(res)

@queue_bp.route('/save')
def save():
    name = request.args.get('name')
    res = queue.save(name)
    return jsonify(res)

@queue_bp.route('/clear')
def clear():
    res = queue.clear()
    return jsonify(res)

@queue_bp.route('/new')
def move():
    res = queue.new()
    return jsonify(res)

@queue_bp.route('/reset')
def reset():
    # max = request.args.get('max',type=int)
    res = queue.reset()
    return jsonify(res)