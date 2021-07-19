
from flask import (
    g, request, session, jsonify
)

# from mdisc.db import get_db
from .api import Playlist, Playlists
from . import playlist_bp

playlist = Playlist()
playlists = Playlists()

@playlist_bp.route("/list") #parent
def listplaylists():
    max = request.args.get('max',type=int)

    session['playlists_page'] = session.get('playlists_page', 1) 
    # session['playlists_pg_start'] = session.get('playlists_pg_start', 0) 
    # session['playlists_pg_end'] = session.get('playlists_pg_end', max)
    playlists_res = playlists.list(max, 
                                session['playlists_page'],'playlists_page')
    return jsonify(playlists_res)

@playlist_bp.route('/enqueue') #parent
def enqueue():
    playlistname = request.args.get('name')
    res = playlists.enqueue(playlistname)
    return jsonify(res)

@playlist_bp.route('/reset')
def reset():
    res = playlists.reset()
    return jsonify(res)

@playlist_bp.route('/cache')
def getcache():
    res = playlists.getcache()
    return jsonify(res)


@playlist_bp.route('/content') #Playlist content
def listrack():
    name = request.args.get('name')
    max = request.args.get('max',type=int)

    session['playlist_page'] = session.get('playlist_page', 1) 
    # session['playlist_pg_start'] = session.get('playlist_pg_start', 0) 
    # session['playlist_pg_end'] = session.get('playlist_pg_end', max)
    session['playlist_name'] = name
    
    playlist_tracks = playlist.list(max, 
                                    session['playlist_page'],'playlist_page')
    return jsonify(playlist_tracks) 

@playlist_bp.route('/name')
def getname():
    name = playlist.getplname()
    return jsonify(name)

@playlist_bp.route('/add') 
def add():
    name = request.args.get('name')
    uri = request.args.get('uri')
    res = playlist.add(name, uri)
    return jsonify(res)

@playlist_bp.route('/fav') 
def fav():
    name = request.args.get('name')
    uri = request.args.get('uri')
    res = playlist.fav(name, uri)
    return jsonify(res)


@playlist_bp.route('/getlog') 
def log():
    res = playlist.getlog()
    return jsonify(res)

@playlist_bp.route('/delete')
def delete():
    name = request.args.get('name')
    uri = request.args.get('uri')
    res = playlist.delete(name, uri)
    return jsonify(res)

@playlist_bp.route('/rm')
def rm():
    name = request.args.get('name')
    res = self.playlist.rm(name)
    return jsonify(res)


@playlist_bp.route('/resetc')
def plreset():
    res = playlist.reset()
    return jsonify(res)
