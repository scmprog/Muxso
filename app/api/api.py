from flask import session, request, jsonify
from mpd import MPDClient
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


class Queue():
    users = []

    def __init__(self):
        self.client = MPDClient()
        self.queue = self.__class__
        self.client.timeout = 30
        self.client.idletimeout = None
        # Playback
        self.delqueue = []  # for delvote
        # self.
        # Playlist
        # self.enqueue_cache = [] --->1
        # self.log = {} --->2
        # Queue
        # self.add_cache_privacy = []
        # init encrypt page
        # self.privacy = Setting.privacy
        self.skip = 0
        self.encrypt = []
        self.isencrypted = []
        # init Decrypt page
        # self.decrypt = []
        # self.isdecrypted = []

    def connect(self):
        self.client.connect('127.0.0.1', 6600)

    def disconnect(self):
        self.client.close()
        self.client.disconnect()

    # START Normal List
    def getlist(self):
        self.connect()
        tracks = self.client.playlistid()
        self.disconnect()
        return tracks

    def ash(self, id):
        encode = id.encode('utf-8')
        hash = md5(encode).hexdigest()
        return hash

    def hash(self, id):
        hash = generate_password_hash(id, 'md5')
        chash = hash[hash.index('$')+1:]
        return chash

    # Protected List
    def compress(self):
        precrypt = []
        tmp = {}
        for track in self.getlist():
            tmp['file'] = track['file']
            tmp['time'] = track['time']
            tmp['duration'] = track['duration']
            tmp['id'] = track['id']
            precrypt.append(tmp)
            tmp = {}
        return precrypt

    def encrypt_track(self):  # for displaying only
        decompress = self.compress()
        print('crypt', self.skip)
        # print('enc1',[x['file'] for x in self.encrypt],len(self.encrypt))
        if self.skip == 1:
            return self.getlist()
        for i in range(len(decompress)):
            print(decompress[i]['id'], self.isencrypted)
            if decompress[i]['id'] not in self.isencrypted:
                id = session['uuid']
                hash = self.hash(id)
                # proxy
                decompress[i]['file'] = hash
                id = decompress[i]['id']
                self.encrypt.append(decompress[i])
                self.isencrypted.append(id)
        print('+++', [{x['id']} for x in self.encrypt])
        return self.encrypt

    # def decrypt_track(self):
    #     etrack = self.encrypt
    #     for i in range(len(etrack)):
    #         if etrack[i]['id'] not in self.isdecrypted:
    #             decrypted = 'free'
    #             id = etrack[i]['id']
    #             self.decrypt.append(etrack[i])
    #             self.isdecrypted.append(id)
    #     return self.decrypt

    def reset(self):
        session['q_page'] = 1
        print('reset', session['q_page'])
        return session['q_page']

    # Paging
    def list(self, max, page, pagename):
        # global privacy
        print(Setting.privacy)
        if Setting.privacy:
            tracks = self.encrypt_track()
        else:
            tracks = self.getlist()
        self.tracklength = len(tracks)  # Total
        self.max = max  # Per Page
        self.last_page = int(self.tracklength / self.max)  # no. of pages
        self.page_left = int(self.tracklength % max)  # no. page left
        self.page = page
        # self.page_flip =  ((self.page-1) * self.max) + 1
        self.pg_start = ((self.page-1) * self.max) + 1  # from
        self.pg_end = self.page*self.max  # offset
        if self.tracklength == 0:
            print('empty')
            self.page = []
            return []

        if self.page_left != 0:
            self.last_page += 1

        print('max', max,)
        print('cp', page, 'lp', self.last_page)
        print('st', self.pg_start, 'end', self.pg_end)
        print('left', self.page_left)

        is_lastpage = self.page == self.last_page
        if is_lastpage:
            print('last')
            self.page = tracks[self.pg_start-1:self.pg_end]
            session[pagename] = 1
            # page = 1
        else:
            print('contd')
            session[pagename] = self.page+1
            self.page = tracks[self.pg_start-1:self.pg_end]
        # print('page',self.page)
        return self.page
    # END

    # START
    def adduser(self):
        id = session['uuid']
        if id not in self.queue.users:
            self.queue.users.append(id)
        # print(self.users)

    def online(self):
        print(self.queue.users)
        return self.queue.users

    def getvote(self):
        return self.delqueue

    def reset_del(self):  # EVENT
        self.delqueue = []
        return {'Sucess': self.delqueue}

    def checkdel(self):
        id = session['uuid']
        if id not in self.delqueue:
            self.delqueue.append(id)

    def okdelete(self):
        self.checkdel()
        users = len(self.online())
        vote = len(self.delqueue)
        print(users, 'ok')
        if users <= 2:
            return True
        elif users-1 == vote:
            return True
        else:
            return False

    # Delete OPS
    def delete(self):
        try:
            if self.okdelete():
                self.connect()
                id = self.client.currentsong()['id']
                self.client.next()
                self.client.deleteid(id)
                self.reset_del()
                self.disconnect()
                return ({"OKDelete": id})
            else:
                return {"Error": "Not Allowed"}
        except Exception as del_err:
            print(del_err)
            self.disconnect()
            return ({"Error": "No such song"})
    # END

    def save(self, name):
        try:
            self.connect()
            self.client.save(name)
            self.disconnect()
            return ({"OKSaved": name})
        except Exception as save_err:
            self.disconnect()
            error = repr(save_err)
            res = self.generate_err(error)
            return res

    # ERROR FUNCTION
    def generate_err(self, error):
        error = repr(error)
        return ({"Error": error})

    def clear(self):
        self.connect()
        self.client.clear()
        self.disconnect()
        return {"Queue": "OKClear"}

    def new(self):
        try:
            self.reset()
            return {"OKReset": self.page}
        except:
            return {"Error": "EmptyList"}


class Library(Queue):
    add_cache = []

    def __init__(self):
        Queue.__init__(self)
        self.proxy_uri = {}
        self.lib = self.__class__

    def queuetrack(self, uri):
        try:
            print('added', self.lib.add_cache)
            if uri not in self.lib.add_cache:
                self.connect()
                print(repr(uri), 'test')
                self.client.update()
                id = self.client.addid(uri)
                self.client.moveid(id, '0')
                self.lib.add_cache.append(uri)
                self.disconnect()
            else:
                id = "Already added"
            return ({uri: id})
        except Exception as add_err:
            print(add_err)
            self.disconnect()
            return ({"Error": "No such song"})

    # START CONFIG
    def reset(self):
        session['lib_page'] = 1
        return session['lib_page']

    def getfiles(self):
        self.connect()
        files = self.client.listfiles()
        self.disconnect()
        return files

    def filter_size(self):
        filter = []
        for uri in self.getfiles():
            if uri['size'] != '0':
                filter.append(uri)
        file = [files['file'] for files in filter]
        print('list', len(file))
        return filter

    # SETUP GETLIST FUNC TO DISPLAY UNLOADED TRACK NON-PRIVACY
    def filter_not_loaded(self):
        loaded = self.lib.add_cache  # addinqueue
        filter = []
        for uri in self.filter_size():
            if uri['file'] in loaded:
                uri['loaded'] = True
            else:
                uri['loaded'] = False
            filter.insert(0, uri)
        return filter

    # LIST
    def getlist(self):
        display = self.filter_not_loaded()
        print('afilter', len(display))
        return display  # to list

    def compress(self):  # Encrypt List for page
        precrypt = []
        tmp = {}
        getlist = self.getlist()
        for track in self.getlist():
            tmp['file'] = track['file']
            tmp['size'] = track['size']
            tmp['id'] = self.ash(tmp['file'])
            tmp['loaded'] = track['loaded']
            tmp['crypt'] = 1
            precrypt.append(tmp)
            tmp = {}
        return precrypt

    def encrypt_track(self):
        decompress = self.compress()
        for i in range(len(decompress)):
            id = session['uuid']
            hash = self.hash(id)
            # proxy mapping
            plaintext = decompress[i]['file']
            if plaintext not in self.proxy_uri.values():
                self.proxy_uri[hash] = plaintext
                self.proxy_id = {file[1]: file[0]
                                 for file in self.proxy_uri.items()}
            id = self.proxy_id[plaintext]
            print(id, len(self.proxy_id))
            decompress[i]['file'] = id

        return decompress

    # Config Page for Loading
    def filter_from_page(self):
        loaded = self.lib.add_cache
        # print('load',loaded,len(loaded))
        filter = []
        # print('page',self.page)
        if not Setting.privacy:
            for uri in self.page:
                if uri['file'] not in loaded:
                    filter.append(uri)
        elif Setting.privacy:
            for uri in self.page:
                uri_id = uri['file']
                uri_name = self.proxy_uri[uri_id]
                print(uri_name)
                if uri_name not in loaded:
                    filter.append({'file': uri_name})
        print('CURPAGE', [filter['file'] for filter in self.page])
        return filter

    def zip_page(self):  # ZIP PAGE TO PLAYLIST and LOAD
        pageload_empty = self.filter_from_page()
        # print(pageload_empty)
        is_empty = 0
        if pageload_empty:
            for uri in pageload_empty:
                # print('uri',uri)
                self.connect()
                self.client.update()
                self.client.playlistadd('tmp', uri['file'])
                self.disconnect()
                self.lib.add_cache.append(uri['file'])
            is_empty = 1
            return is_empty
        else:
            is_empty = 0
            return is_empty

    def unzip(self):
        self.client.rm('tmp')

    def setup_load(self):
        ziped = self.zip_page()
        if ziped:
            self.connect()
            self.client.load('tmp')
            self.unzip()
            self.disconnect()
        return ({"OKLoaded": self.page})

    def load(self):
        # try:
        # self.scan()
        return self.setup_load()
        # except Exception as e: #'Library' object has no attribute 'page'
        # self.disconnect()
        # print(e,'err_Load')
        # return ({"Error":'EmptyList'})
    # END

    def scan(self):
        self.connect()
        self.client.update()
        self.disconnect()
        return ({"OK": "updated"})


class Playlists(Queue):

    # START
    def __init__(self):
        Queue.__init__(self)
        self.enqueue_cache = []

    def reset(self):
        session['playlists_page'] = 1
        return session['playlists_page']

    def getcache(self):
        return self.enqueue_cache

    def getpl(self):
        self.connect()
        playlists = self.client.listplaylists()
        plname = list(map(lambda x: x['playlist'], playlists))
        name_len = list(map(lambda x: {'length': len(
            self.client.listplaylistinfo(x)), 'playlist': x}, plname))
        self.disconnect()
        return name_len

    def getlist(self):
        sortnew = self.getpl()
        return sortnew
    # END

    def skip_pl(self):
        print('press', self.skip)
        self.skip = 1

    def compress(self):  # Protected List
        self.skip_pl()

    def add_to_loadcache(self, name):
        pl = self.client.listplaylistinfo(name)
        for i in pl:
            if i['file'] not in Library.add_cache:
                Library.add_cache.append(i['file'])

    def enqueue(self, name):
        try:
            # self.enqueue_cache = enqueue_cache
            if name not in self.enqueue_cache:
                self.connect()
                self.client.update()
                self.client.load(name)
                self.add_to_loadcache(name)
                self.disconnect()
                self.enqueue_cache.append(name)
                print(self.enqueue_cache)
                return ({"OKEnqueue": name})
            else:
                print('qd', self.enqueue_cache)
                return ({name: "Already enqueue"})
        except Exception as enqueue_err:
            print(enqueue_err)
            self.disconnect()
            return ({"Error": "No such playlist"})


class Playlist(Playlists):
    def __init__(self):
        Queue.__init__(self)
        self.log = {}
    # SETUP LIST

    def reset(self):
        session['playlist_page'] = 1

    def getplname(self):
        name = session['playlist_name']
        return name

    def playlist(self, name):
        try:
            self.connect()
            tracks = self.client.listplaylistinfo(name)  # list playlist
            self.disconnect()
            return tracks
        except Exception as e:
            print(e)
            return []
            self.disconnect()

    def isload(self, track):
        if track['file'] in Library.add_cache:
            track['isload'] = 1
        else:
            track['isload'] = 0
        return track

    def getlist(self):
        name = self.getplname()
        tracks = self.playlist(name)
        is_loaded = list(map(self.isload, tracks))
        return tracks
    # END

    # SETUP PRIVACY
    def compress(self):  # Protected List
        precrypt = []
        tmp = {}
        tracks = self.getlist()
        for track in tracks:
            # print(len(track),track)
            tmp['file'] = track['file']
            tmp['id'] = self.ash(track['file'])
            tmp['iscrypt'] = 1
            tmp['isload'] = track['isload']
            lost = len(track) > 2
            if lost:
                tmp['time'] = track['time']
                tmp['duration'] = track['duration']
            else:
                tmp['lost'] = 1
            precrypt.append(tmp)
            tmp = {}
        print(precrypt)
        return precrypt
    # END

    def encrypt_track(self):
        decompress = self.compress()
        for i in range(len(decompress)):
            id = decompress[i]['file']
            hash = self.hash(id)
            decompress[i]['file'] = hash
        return decompress
    # SETUP add() LOGGER

    def logger(self, name, uri):
        # {'playlist:[track1,track2,....]]}
        self.log[name] = self.log.get(name, [])
        if uri not in self.log[name]:
            self.log[name].append(uri)

    def getlog(self):
        return self.log
    # END

    def fav(self, name, uri):
        try:
            self.connect()
            pl = self.client.listplaylist(name)
            self.disconnect()
            if uri not in pl:
                self.connect()
                self.client.playlistadd(name, uri)
                self.disconnect()
                return {"add": True}
            else:
                self.delete(name, uri)
                return {"add": False}
        except Exception as add_err:
            self.disconnect()
            error = repr(add_err)
            res = self.generate_err(error)
            return res

    def add(self, name, uri):
        try:
            self.connect()
            self.client.playlistadd(name, uri)
            self.disconnect()
            self.logger(name, uri)  # LOG IF ADD (OPTIMIZE)
            return {name: uri}
        except Exception as add_err:
            self.disconnect()
            error = repr(add_err)
            res = self.generate_err(error)
            return res

    def delete(self, name, uri):
        try:
            self.connect()
            tracks = self.client.listplaylist(name)
            print(tracks)
            pos = tracks.index(uri)
            self.client.playlistdelete(name, pos)
            self.disconnect()
            return {"OKdelete": name}
        except Exception as del_err:
            self.disconnect()
            error = repr(del_err)
            res = self.generate_err(error)
            return res

    def clear(self, name):
        try:
            self.connect()
            self.client.playlistclear(name)
            self.disconnect()
            return {name: 'OKClear'}
        except Exception as clear_err:
            self.disconnect()
            error = repr(clear_err)
            res = self.generate_err(error)
            return res

    def rename(self, name, new_name):
        try:
            self.connect()
            self.rename(name, new_name)
            self.disconnect()
            return {name: new_name}
        except Exception as mverr:
            self.disconnect()
            error = repr(mverr)
            res = self.playlist_err(error)
            return res

    def rm(self, name):
        try:
            self.connect()
            self.rm(name)
            self.disconnect()
            return {'rm': name}
        except Exception as rm_err:
            self.disconnect()


class Playback(Queue):
    looptrack = True
    ntime = 0
    new_rtime = 1
    reset = 0

    def __init__(self):
        Queue.__init__(self)
        # self.looptrack = False
        # self.new_rtime = 2
        self.playback = self.__class__

    # Options
    def status(self):
        try:
            self.connect()
            status = self.client.status()
            self.disconnect()
            return status
        except Exception as e:
            print(e)
            self.disconnect()

    def consume(self, state):
        try:
            self.connect()
            self.client.consume(state)
            self.disconnect()
            return {'consume': self.status()['consume']}
        except Exception as error:
            self.disconnect()
            return self.generate_err(error)

    def playnext(self, id):
        try:
            self.connect()
            self.client.random(1)
            self.client.prioid(255, id)
            self.disconnect()
            return self.status()
        except Exception as error:
            self.disconnect()
            return self.generate_err(error)

    def setvol(self, vol):
        try:
            self.connect()
            self.client.setvol(vol)
            self.disconnect()
            return self.status()['volume']
        except Exception as error:
            self.disconnect()
            return self.generate_err(error)

    def single(self, state):
        try:
            self.connect()
            self.client.single(state)
            self.disconnect()
            return {'Single': self.status()['single']}
        except Exception as error:
            self.disconnect()
            return self.generate_err(error)

    def repeat(self, state):
        try:
            self.connect()
            self.client.repeat(state)
            self.disconnect()
            return {'Repeat': self.status()['repeat']}
        except Exception as error:
            self.disconnect()
            return self.generate_err(error)
    # Controller

    def next(self):
        try:
            self.connect()
            self.client.next()
            self.disconnect()
            return 'ok'
        except Exception as e:
            self.disconnect()
            return "not playing"

    def prev(self):
        try:
            self.connect()
            self.client.previous()
            self.disconnect()
            return 'ok'
        except Exception as e:
            self.disconnect()
            return "not playing"

    def pause(self):
        state = self.status()['state']
        if(state == 'play'):
            self.connect()
            self.client.pause(1)
            self.disconnect()
        elif state == 'pause':
            self.connect()
            self.client.pause(0)
            self.disconnect()
        return self.status()['state']

    def play(self, id):
        try:
            self.connect()
            self.client.playid(id)
            self.disconnect()
            return self.status()
        except Exception as play_err:
            print(play_err, 'id', id)
            self.disconnect()
            return {'Error': 'No such song'}

    def onplay(self):
        self.connect()
        song = self.client.currentsong()
        self.disconnect()
        print(song.get('id', '-1'))
        active = song.get('id', None)
        if active:
            self.connect()
            self.client.pause()
            self.disconnect()
            return self.status()['state']
        else:
            return 'Not Playing'

    def stop(self):
        self.connect()
        self.client.stop()
        self.disconnect()
        return self.status()

    # START 2x Repeat

    def onloop(self):
        # self.playback.ntime = rtime
        self.playback.looptrack = True
        print('onloop')
        if self.status()['state'] != 'stop':
            self.loop_id = self.status().get('songid')
            # self.single('1')
            return {"loop": "on"}
        else:
            return {'Error': 'Not playing'}

    def offloop(self):
        self.looptrack = False
        self.single('0')
        return {'loop': 'off'}

    def repeatn(self, r_time):
        self.playback.new_rtime = r_time
        return self.playback.new_rtime

    def resetloop(self):
        self.playback.ntime = self.playback.new_rtime
        self.playback.reset = 1
        print('resetloop')
        return self.playback.ntime

    def toggle(self, state):
        # if(self.playback.ntime != 0):
        #     self.playback.ntime -= 1
        # else:
        #     self.playback.ntime = 0
        self.playback.ntime -= 1

        print('left', self.playback.ntime)
        if(self.playback.ntime != 0):
            if(state == 'play'):
                print('on')
                self.single('1')
        else:
            print('reset', self.playback.new_rtime)
            self.single('0')
            self.playback.ntime = self.playback.new_rtime

    def setloop(self):
        state = self.status().get('state')
        if state != 'stop':
            elapsed = float(self.status()['elapsed'])
            isnext = (int(elapsed) == 0)
            if isnext:
                self.toggle(state)
            return {"Counter": self.playback.ntime}
        else:
            return {'Error': 'Not playing'}

    def loop(self):  # EVENT
        print(self.playback.looptrack, 'LOOP')
        if self.playback.looptrack == True:
            return self.setloop()
        else:
            return {'Error': "Loop is off"}
    # END

    def currentsong(self):  # Privacy
        try:
            print('***********************************')
            self.connect()
            song = self.client.currentsong()
            self.disconnect()
            # id = song.get('id',0)
            # print('id',id)
            return song
        except Exception as e:
            print('cs', e)
            self.disconnect()

    def isfav(self):
        self.connect()
        pl = self.client.listplaylist('f')
        song = self.client.currentsong().get('file', 'Unknown')
        self.disconnect()
        if (song in pl):
            return True
        else:
            return False

    def renderPlayer(self):
        self.connect()
        currentsong = self.client.currentsong()
        song = currentsong.get('file', 'Unknown')
        min = int(int(currentsong.get('time', 0))/60)
        sec = int(currentsong.get('time', 0)) % 60
        self.disconnect()
        isfav = self.isfav()
        return {'name': song, 'time': [min, sec], 'isfav': isfav}


class Setting(Queue):
    privacy = False
    # sync

    def __init__(self):
        Queue.__init__(self)
        self.setting = self.__class__
    
    def stream(self):
        self.connect()
        http = [o for o in self.client.outputs() if o['outputname']
                == 'My HTTP Stream']
        self.disconnect()
        return http

    def out_id(self):
        return int(self.stream()[0]['outputid'])

    def sync(self):
        id = self.out_id()
        self.connect()
        self.client.enableoutput(id)
        self.disconnect()
        return self.stream()[0]['outputenabled']

    def offsync(self):
        id = self.out_id()
        self.connect()
        self.client.disableoutput(id)
        self.disconnect()
        return self.stream()[0]['outputenabled']

    def toggleprivacy(self):
        # global privacy
        if self.setting.privacy:
            print('it', self.setting.privacy)

            self.setting.privacy = False
            return self.setting.privacy
        else:
            print('if', self.setting.privacy)

            self.setting.privacy = True
            return self.setting.privacy

    def reset(self):
        from os import system
        session['lib_page'] = 1
        system('rm /sdcard/Music/*')
        return session['lib_page']
