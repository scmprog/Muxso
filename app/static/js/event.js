class Event {
  constructor() {
    // this.namespace = "/rt/notify/";
    this.socket = io.connect(
      "http://" + document.domain + ":" + location.port + "/rt/notify/"
    );
  }
  renderTrack(msg) {
    let song = msg.song["name"];
    let min = msg.song["min"];
    let sec = msg.song["sec"];
    let pad = sec <= 9 ? "0" + sec : sec;
    if (min == 0) {
      $("#playing").html(`${song}`);
      $("#time").html(`&nbsp;`)
      $("#state").removeClass("ui-icon-play").removeClass("ui-icon-play");
      $("#state").addClass("ui-icon-stop");
    } else {
      $("#playing").html(`${song}`);
      $("#time").html(`<sub>${min}:${pad}</sub>`)
    }
  }
  like(msg) {
    if (msg.isfav) {
      $("#like").removeClass("ui-icon-heart-o").addClass("ui-icon-heart");
    } else {
      $("#like").removeClass("ui-icon-heart").addClass("ui-icon-heart-o");
    }
  }
  loop() {
    let self = this;
    this.socket.on("event", function (msg) {
      // console.log('Ev',msg.ev);
      if (msg.ev == "player" || msg.ev == "stored_playlist") {
        console.log("player");
        self.renderTrack(msg);
        self.like(msg);
      }
      if (msg.ev == "stored_playlist"){
        // pl.refresh()/
      }
      if (msg.ev == "playlist") {
        console.log("reset", msg.reset);
        if (msg.reset == 1) {
          // queue.refresh()
          console.log("playlist");
          self.renderTrack(msg);
          self.like(msg);
        }
      }
    });
  }
}
e = new Event();
e.loop();
