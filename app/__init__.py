from flask import Flask
from flask_socketio import SocketIO

async_mode = 'eventlet'
socketio = SocketIO(async_mode=async_mode)

def create_app(debug=False):
    # create and configure the app
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'dev'
    app.config['UPLOAD_FOLDER'] = '~/'

    # app.config.from_object('config')
 
    from app.api import queue_bp
    from app.api import library_bp
    from app.api import playlist_bp  
    from app.api import playback_bp
    from app.api import setting_bp
    from app.ui import ui
    
    app.register_blueprint(ui)
    app.register_blueprint(queue_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(playlist_bp)
    app.register_blueprint(playback_bp)
    app.register_blueprint(setting_bp)
    
    from app.event import events
    socketio.init_app(app)
    return app
