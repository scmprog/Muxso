# Muxso

Muxso is a web based Music Player with special focus on sharing and discovering of music on LAN.

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
- now the app can be access using [YourIP]:[PORT] for example 192.168.43.1:8080

# Screenshot
![127 0 0 1_5000_(iPhone 4) (1)](https://user-images.githubusercontent.com/87179125/127267384-c5a42a4d-64c2-482b-8b67-cf5e30e53e06.png)

![127 0 0 1_5000_(iPhone 4)](https://user-images.githubusercontent.com/87179125/127267394-3825be91-280c-400e-8309-18beabb55788.png)

