# Muxso

Muxso is a web based Music Player with special focus on sharing and discovering of music on a LAN.

The software has three components: A centralized music server daemon, a Flask/Python based backend which proxy a client's http request to the music server and a jQuery web framework for the user interface.

# Features
- Mobile friendly user interface
- Remote control playback
- Synchronization of playback
- Radio streaming
- Privacy mode
- RepeatX

# Installation
- Install MPD latest version (0.21.16)
- Install Python 3.7+
- Make sure pip is installed and run *pip install requirement.txt*
- then start the application by running *python run.py*
- By default the app can be access on localhost only to allow other to connect to the app
- Install gunicorn by running the command *pip install gunicorn*
- then run *gunicorn -b 0.0.0.0:8080 --worker-class eventlet -w 1 run:app*
- now you can access the app using [yourIP]:[PORT] for example 192.168.43.1:8080
