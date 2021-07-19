# import functools

from flask import (
    g, json, request, session, jsonify,redirect
)
from flask.templating import render_template
from werkzeug import secure_filename
# from mdisc.db import get_db
from .api import Playback
from . import playback_bp

playback = Playback()


@playback_bp.route('/play')
def play():
    id = request.args.get('id')
    res = playback.play(id)
    return jsonify(res)


@playback_bp.route('/onplay')
def onplay():
    res = playback.onplay()
    return jsonify(res)


@playback_bp.route('/pause')
def pause():
    res = playback.pause()
    return jsonify(res)


@playback_bp.route('/stop')
def stop():
    res = playback.stop()
    return jsonify(res)


@playback_bp.route('/next')
def next():
    res = playback.next()
    return jsonify(res)


@playback_bp.route('/prev')
def prev():
    res = playback.prev()
    return jsonify(res)


@playback_bp.route('/consume')
def consume():
    state = request.args.get('state')
    res = playback.consume(state)
    return jsonify(res)


@playback_bp.route('/playnext')
def playnext():
    id = request.args.get('id')
    res = playback.playnext(id)
    return jsonify(res)


@playback_bp.route('/repeat')
def repeat():
    # state = request.args.get('state')
    res = playback.repeat()
    return jsonify(res)


@playback_bp.route('/setvol')
def setvol():
    vol = request.args.get('vol')
    res = playback.setvol(vol)
    return jsonify(res)


@playback_bp.route('/onloop')
def onloop():
    rtime = request.args.get('rtime', type=int)
    res = playback.onloop(rtime)
    return jsonify(res)


@playback_bp.route('/offloop')
def offloop():
    res = playback.offloop()
    return jsonify(res)


@playback_bp.route('/loop')
def loop():
    res = playback.loop()
    return jsonify(res)


@playback_bp.route('/repeatn')
def repeatn():
    time = request.args.get('time', type=int)
    res = playback.repeatn(time)
    return jsonify(res)


@playback_bp.route('/currentsong')
def currentsong():
    res = playback.currentsong()
    return jsonify(res)


@playback_bp.route('/status')
def status():
    res = playback.status()
    return jsonify(res)


@playback_bp.route('/render')
def render():
    res = playback.renderPlayer()
    return jsonify(res)


@playback_bp.route('/resloop')
def resetloop():
    res = playback.resetloop()
    return jsonify(res)

    # return 
    # return 
ALLOWED_EXTENSIONS ={'mp3'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import os
@playback_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('/home/sqmbhq/', filename))
            return redirect("#queue")
    return render_template('ui/upload.html')
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''