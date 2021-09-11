# Muxso (Share and Listen together)

# Introduction
Muxso is a web based Music Multiplexer with special focus on sharing and discovering of music.

There’s nothing like listening to your favorite playlist together with friends. That's why Muxso was created to allowed groups of users to listen and control their music with others in real time. It provides shared opportunities for collaboration among all the listeners, you and the members can each share and listen to the same content at the same time on a single ouput devices (Speaker) or stream it on your own devices. Users can pause, play, skip, and select tracks on the queue as well as add their own. If one person makes a change, it will immediately be reflected on all connected devices.

The software has three components: A centralized music server daemon, a Flask/Python based backend which route a client's request to the music server and a jQuery web framework for the client's User Interface.

# Features
- Mobile friendly user interface
- Remote control playback
- Synchronization of playback
- Radio streaming
- Private mode
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

