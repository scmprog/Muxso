from flask import Blueprint

queue_bp = Blueprint('queue', __name__, url_prefix='/queue')
library_bp = Blueprint('library',__name__,url_prefix='/library')
playlist_bp = Blueprint('playlist',__name__,url_prefix='/playlist')
playback_bp = Blueprint('playback',__name__,url_prefix='/playback')
setting_bp = Blueprint('setting',__name__,url_prefix='/setting')


from . import queue, library, playlist, playback, settings