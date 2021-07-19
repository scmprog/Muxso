from ..api import api
from mpd import MPDClient
from threading import Lock

from flask import current_app, session

from .. import socketio

thread = None
thread_lock = Lock()
playback = api.Playback()
queue = api.Queue()
c = MPDClient()


def notifications_job(app):
    count = 0
    with app.app_context():
        step = int(app.config.get('STEP', 1))
        while True:
            socketio.sleep(0.3)
            c.connect('localhost', 6600)
            ev = c.idle()
            status = c.status()
            currentsong = c.currentsong()
            song = currentsong.get('file', 'Unknown')
            min = int(int(currentsong.get('time', 0))/60)
            sec = int(currentsong.get('time', 0)) % 60
            playlist_len = len(c.playlistid())
            http = [o for o in c.outputs() if o['outputname'] == 'My HTTP Stream']
            reset = 0
            cast = 0
            c.close()
            c.disconnect()
            print(ev)
            if ev[0] == 'player':
                # print('plyerLOOP')
                log = playback.loop()
                # print(log)

            if ev[0] == 'playlist':
                if playlist_len == 0:
                    reset = 1
                else:
                    reset = 0
            # count += 1
            if ev[0] == 'output':
                cast = http[0]['outputenabled']

            isfav = playback.isfav()
            # print(isfav)
            print('cast',cast)
            socketio.emit('event', {'ev': ev[0], 'status': status, 'song': {
                          'name': song, 'min': min, 'sec': sec}, 'isfav': isfav, 'reset': reset, 'cast': cast}, namespace='/rt/notify/')


@socketio.on('connect', namespace='/rt/notify/')
def start_notifications_thread():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(
                notifications_job, current_app._get_current_object())
