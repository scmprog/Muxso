class Playback {
  constructor() {
    this.listCreated = false;
    this.createContent = ".ui-controlgroup-controls ";
    this.socket = io.connect(
      "http://" + document.domain + ":" + location.port + "/rt/notify/"
    );
  }
  onloop(set_rtime) {
    $.get("/playback/onloop", { rtime: set_rtime }).done((data) => {
      console.log("loop", data);
    });
  }
  onplay() {
    $("#state")
      .removeClass("ui-icon-play")
      .removeClass("ui-icon-stop")
      .addClass("ui-icon-pause");
  }
  onpause() {
    $("#state").removeClass("ui-icon-pause").addClass("ui-icon-play");
    console.log(document.domain,location.port)
  }
  onstop() {
    $("#state").removeClass("ui-icon-play").removeClass("ui-icon-play");
    $("#state").addClass("ui-icon-stop");
  }
  event() {
    let self = this;
    this.socket.on("event", function (msg) {
      if (msg.ev == "player") {
        let state = msg.status;
        self.toggle(state);
      }
    });
    // this.socket.on("event", function (msg) {
    //   console.log(msg.ev);
    //   if (msg.ev == "output" || msg.ev == "player") {
    //     console.log("mc", msg.cast == 1);
    //     if (msg.cast == 1) {
    //       sync.play();
    //     } else if (msg.cast == 0) {
    //       sync.stop();
    //     }
    //   }
    // });
  }

  toggle(stats) {
    let self = this;
    let play = stats["state"] == "play";
    let pause = stats["state"] == "pause";
    let stop = stats["state"] == "stop";
    if (play) {
      self.onplay();
    } else if (pause) {
      self.onpause();
    } else if (stop) {
      self.onstop();
    }
  }
  rm() {
    $.get("/queue/delete").done((state) => {
      console.log(state);
    });
  }
  play() {
    let self = this;
    $.get("/playback/onplay").done((state) => {
      state == "play" ? self.onplay() : self.onpause();
    });
  }
  next() {
    let self = this;
    $.get("/playback/resloop").done((state) => {
      $.get("/playback/next").done((state) => {});
    });
  }
  prev() {
    let self = this;
    $.get("/playback/resloop").done((state) => {
      console.log(state);
      $.get("/playback/prev").done((state) => {
        console.log(state);
      });
    });
  }

  like(isfav) {
    //duplicated
    if (isfav) {
      $("#like").removeClass("ui-icon-heart-o").addClass("ui-icon-heart");
    } else {
      $("#like").removeClass("ui-icon-heart").addClass("ui-icon-heart-o");
    }
  }

  render() {
    let self = this;
    $.get("/playback/render", (song) => {
      // console.log(song);
      let track = song["name"];
      let min = song["time"][0];
      let sec = song["time"][1];
      let isfav = song["isfav"];
      let pad = sec <= 9 ? "0" + sec : sec;
      $("#playing").html(track);
      $("#time").html(`<sub>${min}:${pad}</sub>`);
      self.like(isfav);
    }).done(() => {
      // self.onloop(0);
    });
  }

  init() {
    let self = this;
    $.get("/playback/status", (stats) => {
      // console.log(stats)
      self.toggle(stats);
    }).done(() => {
      self.render();
    });
  }
}

playback = new Playback();
playback.event();

var custom_event = $.support.touch ? "tap" : "click";

$(document).on("pageinit", "#playback", function (event) {
  playback.init();
});

$(document).on(custom_event, "#state", function () {
  playback.play();
});

$(document).on(custom_event, "#prev", function () {
  console.log("p");
  playback.prev();
});
$(document).on(custom_event, "#next", function () {
  playback.next();
  settings.rmclear();
});

$(document).on(custom_event, "#rm", function () {
  playback.rm();
});

// $(document).on(custom_event, ".queue-current", function () {});
// $(document).on(custom_event, "#repeat", function () {
//   $(this).addClass("repeat");
// });

$(document).on(custom_event, "#like", function () {
  $.get("/playback/currentsong").done((song) => {
    $.get("/playlist/fav", { name: "f", uri: song["file"] }).done((data) => {
      console.log(data);
      data["add"] === true
        ? $("#like").removeClass("ui-icon-heart-o").addClass("ui-icon-heart")
        : $("#like").addClass("ui-icon-heart-o").removeClass("ui-icon-heart");
    });
  });
});

class Settings {
  save(name) {
    $.get("/queue/save", { name: name }).done((state) => {
      console.log(state);
    });
  }
  clear() {
    $.get("/queue/clear").done((state) => {
      console.log(state);
    });
  }
  okclear() {
    $("#clear").addClass("ui-disabled");
  }
  rmclear() {
    $("#clear").removeClass("ui-disabled"); //okclear
  }
  reset() {
    $.get("/setting/reset").done((state) => {
      console.log(state);
    });
  }
  okreset(){
    $("#reset").addClass("ui-disabled"); //okclear
  }
  volChange() {
    $("#vol").on("change", function () {
      console.log($(this).val());
      let vol = $(this).val();
      $.get("/playback/setvol", { vol: vol });
    });
  }
  privacy() {
    $(document).on("slidestop", "#flip-1", function (event, ui) {
      let isprivacy = $("#flip-1").val();
      if (isprivacy) {
        $.get("/setting/privacy").done((data) => {
          console.log(data);
        });
      }
    });
  }
  cast() {
    $(document).on("slidestop", "#flip-2", function (event, ui) {
      let cast = $("#flip-2").val();
      console.log("cast", cast);
      if (cast == 1) {
        sync.play()
        // $.get("/setting/sync").done((data) => {
        //   return data;
        // });
      }
      if (cast == 0) {
        // $.get("/setting/offsync").done((data) => {
        //   return data;
        // });
        sync.stop()
      }
    });
  }
}
settings = new Settings();

$(document).on("pageinit", "#settings", function (event) {
  settings.volChange();
  settings.privacy();
  settings.cast();
  // Privacy

  //
});

$(document).ready(function () {
  // var $form = $("form");
  $("#save-form").submit(function () {
    let name = $("#plname").val();
    settings.save(name);
    $("#plname").val("");
    return false;
  });
  // $('#slider').kendoSlider();

  $("#per_page").submit(function () {
    let max = $("#paging").val();
    // console.log(max)
    queue.setmax(max);
    lib.setmax(max);
    pl.setmax(max);
    content.setmax(max);
    $("#paging").val('')
    return false;
  });
  $("#repeat").submit(function () {
    let max = $("#repeatx").val();
    console.log("rx", max);
    $.get("/playback/repeatn", { time: max }).done((data) => {
      console.log(data);
      $.get("/playback/resloop");
    });
    $("#repeatx").val('')
    return false;
  });
  // $("#per_page").on('click',() => {
  //   let value = $("#paging").val();
  //   console.log(value)
  // });
});

$(document).on(custom_event, "#clear", function () {
  settings.clear();
  settings.okclear();
});

$(document).on(custom_event, "#reset", function () {
  settings.reset();
  settings.okreset();
});

$(document).on(custom_event, "#upload", function () {
  window.location.href = `/playback/upload`
})

$(document).on(custom_event, ".queue-song", function () {
  let id = $(this).attr("id");
  queue.play(id);
  $.get("/playback/resloop").done(() => {
    $.get("/playback/play", { id: id }).done((id) => {
      console.log(id["songid"]);
    });
  });
});
