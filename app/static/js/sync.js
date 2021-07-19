
var Sync = function (playlist) {
  var self = this
  self.playlist = playlist;
}

Sync.prototype = {
  play: function () {
    var self = this
    var sound;
    let data = self.playlist[0];
    if (data.howl) {
      console.log("data not null")
      sound = data.howl;

    } else {
      console.log(document.domain);
      console.log("data null")

      sound = data.howl = new Howl({
        src: [`http://${document.domain}:8000/`],
        // src: ['http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_q'],
        html5: true,
      })
    }
    console.log(sound)
    sound.stop()
    sound.play()
  },

  stop: function () {
    var self = this
    var sound = self.playlist[0].howl
    console.log(sound)
    console.log("unload")
    if (sound) {
      sound.unload();
    }
  }
}

var sync = new Sync([
  {
    howl: null,
  }
])