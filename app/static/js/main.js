class Queue {
  constructor(page_max) {
    this.listCreated = false;
    this.max = page_max;
    this.createContent = "#queue-content";
    this.createList = "queue-list";
    this.list = `#${this.createList}`;
    this.create_queue_song = "queue-song";
    this.queue_song = `.${this.create_queue_song}`;
    this.current = "queue-current"; //css class listview
    this.playhl = {};
    this.flag = 0;
  }
  setmax(max){
    if(this.max < 0){
      this.max = 10
    }
    this.max = max;
  }
  getmax(){
    return this.max;
  }
  isTimesize(track) {
    let res = track.time ? track.time : track.size;
    return res;
  }
  enable(id) {
    $(`#${id}`).addClass("ui-disabled");
    $(`#${id}`).addClass("ui-btn-icon-right").addClass(" ui-icon-audio");
  }
  disable(id) {
    $(`#${id}`).removeClass("ui-disabled");
    $(`#${id}`).removeClass("ui-btn-icon-right").removeClass(" ui-icon-audio");
  }
  resetplayhl() {
    let id = this.flag === 0 ? this.playhl["prev"] : this.playhl["curr"]; //get current id
    this.disable(id);
  }

  play(id) {
    if (this.flag == 0) {
      this.playhl["curr"] = id;
      this.enable(id);
    } else {
      let prev_id = this.playhl["curr"];
      this.playhl["prev"] = id;
      this.disable(prev_id);
      this.enable(id);
      this.playhl["curr"] = id;
    }
    this.flag = 1;
  }

  disableLoad(el) {
    setTimeout(function () {
      $(el).addClass("ui-disabled");
    }, 200);
  }

  get_attr(res) {
    let track = res.map((track) => {
      let song = track["file"];
      let id = track["id"];
      let loaded = track["loaded"];
      let crypt = track["crypt"];
      // let timeOrsize = this.isTimesize(track);
      return { song, id, loaded, crypt };
    });
    return track;
  }

  set_attr(track, el, index) {
    let uri = track[index]["song"];
    let id = track[index]["id"];
    let load = track[index]["loaded"];
    let crypt = track[index]["crypt"] === undefined ? 0 : 1;
    $(el).attr("id", id);
    $(el).attr("uri", uri);
    $(el).attr("loaded", load);
    $(el).attr("crypt", crypt);
    $(el).html(`${uri}`);
  }
  highlight(id) {
    self = this;
    if (id == this.playhl["curr"]) {
      $("li.queue-current a").each(function (i, el) {
        if (id == $(el).attr("id")) {
          $(el).addClass("ui-disabled");
          $(el).addClass("ui-btn-icon-right").addClass(" ui-icon-audio");
        }
      });
    }
  }

  updateQueue(data) {
    let self = this;
    let track = this.get_attr(data);
    this.resetplayhl();
    //UI LIST-REFILL
    $(self.queue_song).each((index, el) => {
      if (track.length != this.max) {
        if (index < track.length) {
          self.set_attr(track, el, index);
          $(el).removeClass("ui-disabled");
          let id = $(el).attr("id");
          self.highlight(id);
        } else {
          self.disableLoad(el);
          $(el).attr("id", -1);
          $(el).html("&nbsp;");
        }
      } else {
        self.set_attr(track, el, index);
        $(el).removeClass("ui-disabled");
        let uri = $(el).text();
        let id = $(el).attr("id");
        self.highlight(id, uri);
      }
    });
  }

  refresh() {
    let self = this;
    $.get("/queue/list", { max: self.max }).done((track) => {
      self.updateQueue(track);
    });
  }

  initRender(data, max) {
    let tmp = data;
    if (data === undefined || data.length == 0) {
      // init if fully empty
      data = new Array(max);
      data.fill({
        file: "&nbsp;",
        playlist: "&nbsp;",
        length: "",
        loaded: true,
      });
    }
    if (data.length < max) {
      //init IF PARTLY EMPTY
      data = new Array(max);
      data.fill({
        file: "&nbsp;",
        playlist: "&nbsp;",
        length: "",
        loaded: true,
      });
      for (let i = 0; i < tmp.length; i++) {
        data[i] = tmp[i];
      }
    }
    return data;
  }

  renderview(track) {
    let song = track["file"];
    let id = track["id"];
    let state = id === undefined ? "ui-disabled" : "ui-enabled";
    let tracklist = `<li data-theme="b" class="ui-btn ui-mini ${this.current}" >
    <a href="#" id=${id} uri=${song} class="${state} ${this.create_queue_song} ui-mini ui-btn ui-icon-false">${song}</a>
    </li>`;
    return tracklist;
  }

  renderQueue(data) {
    let self = this;
    data = self.initRender(data, self.max);
    data.forEach(function (track) {
      // let timeOrsize = self.isTimesize(track);
      let tracklist = self.renderview(track);
      $(self.list).append(tracklist);
    });
    $(self.list).listview("refresh");
  }

  createQueue() {
    if (!this.listCreated) {
      $(this.createContent).append(
        `<ul id=${this.createList} class="${this.createList}" data-role='listview' data-count-theme="b"></ul>`
      );
      this.listCreated = true;
      $(this.createContent).trigger("create");
    }
  }

  initQueue() {
    let self = this;
    $.get("/queue/reset").done(() => {
      $.get("/queue/list", {
        max: self.max,
      }).done((track) => {
        $(`.queue-current`).remove();
        self.createQueue();
        self.renderQueue(track);
        // self.highlight();
      });
    });
  }
}

// QUEUE CLASS END
class Library extends Queue {
  constructor(page_max) {
    super(page_max);
    this.max = page_max;
    this.listCreated = false;
    this.createContent = "#lib-content";
    this.createList = "lib-list";
    this.list = `#${this.createList}`;
    this.create_queue_song = "lib-song";
    this.queue_song = `.${this.create_queue_song}`;
    this.current = "lib-current"; //css class listview
  }

  hlloaded() {
    let self = this;
    $(this.queue_song).each((i, el) => {
      let loaded = $(el).attr("loaded");
      $(el).addClass("ui-disabled");
      self.enableLoad(el);
      // }
    });
  }
  enableLoad(el) {
    // setTimeout(function () {
    $(el).addClass("ui-disabled");
    // }, 100);
  }
  disableLoad(el) {
    // setTimeout(function () {
    $(el).removeClass("ui-disabled");
    // }, 100);
  }
  toggle(index, track, el) {
    let load = track[index]["loaded"];
    load === true ? this.enableLoad(el) : this.disableLoad(el);
  }

  highlight() {}

  updateLib(data) {
    let self = this;
    let track = this.get_attr(data);
    //UI LIST-REFILL
    console.log("ref", track);
    $(self.queue_song).each((index, el) => {
      if (track.length != this.max) {
        if (index < track.length) {
          self.set_attr(track, el, index);
          self.toggle(index, track, el);
          // self.disableLoad(el)
        } else {
          // self.disableLoad(el);
          super.disableLoad(el);
          $(el).attr("id", -1);
          $(el).html("&nbsp;");
        }
      } else {
        self.set_attr(track, el, index);
        self.toggle(index, track, el);
        // self.disableLoad(el)
      }
    });
  }

  reset() {
    $(this.queue_song).removeClass("ui-disabled");
  }
  refresh() {
    let self = this;
    // self.reset();
    $.get("/library/scan").done((data) => {
      $.get("/library/list", { max: self.max }).done((track) => {
        // console.log(track);
        self.updateLib(track);
      });
    });
  }

  renderview(track) {
    // console.log(track);
    let song = track["file"];
    let isload = track["loaded"];
    let state = isload === true ? "ui-disabled" : "ui-enabled";
    let iscrypt = track["crypt"] === undefined ? 0 : 1; // for encrypt mode
    // loaded=${isload}
    let tracklist = `<li data-theme="b" class="ui-btn ui-mini ${this.current}" >
    <a href="#" uri=${song} crypt=${iscrypt} class="${state} ${this.create_queue_song} ui-mini ui-btn ui-icon-false">${song}</a>
    </li>`;
    return tracklist;
  }

  renderLib(track) {
    super.renderQueue(track);
  }

  createLib() {
    super.createQueue();
  }

  initLib() {
    let self = this;
    $.get("/library/reset").done(() => {
      $.get("/library/list", {
        max: self.max,
      }).done((track) => {
        self.createLib();
        self.renderLib(track);
      });
    });
  }
}

// Lib CLASS END
class Playlist extends Queue {
  constructor(page_max) {
    super(page_max);
    this.max = page_max;
    this.listCreated = false;
    this.createContent = "#playlist-content";
    this.createList = "playlist-list";
    this.list = `#${this.createList}`;
    this.create_queue_song = "playlist-song";
    this.queue_song = `.${this.create_queue_song}`;
    // this.counter = {};
  }
  highlight() {}

  set_attr(index, list, el) {
    let plname = list[index]["playlist"];
    let count = list[index]["count"] >= 10 ? "10+" : list[index]["count"];
    $(el).attr("id", plname);
    $(el).html(`${plname}<span class="ui-li-count">${count}</span>`);
  }

  get_attr(data) {
    let metadata = data.map((metadata) => {
      let name = metadata["playlist"];
      let length = metadata["length"];

      return { playlist: name, count: length };
    });
    return metadata;
  }
  disableLoad(index, list, el) {
    //child
    $(el).removeClass("ui-disabled");
    $(this.list).listview("refresh");
  }
  updatePl(data) {
    let self = this;
    console.log("update");
    let list = self.get_attr(data);
    this.highlight();
    $(self.queue_song).each((index, el) => {
      if (list.length != self.max) {
        if (index < list.length) {
          self.set_attr(index, list, el);
          self.disableLoad(index, list, el);
        } else {
          $(el).attr("id", -1);
          $(el).html("&nbsp;");
          $(el).addClass("ui-disabled");
        }
      } else {
        self.set_attr(index, list, el);
        self.disableLoad(index, list, el);
      }
    });
  }

  refresh() {
    let self = this;
    $.get("/playlist/list", { max: self.max }).done((playlist) => {
      console.log("ref", playlist);
      self.updatePl(playlist);
    });
  }

  renderview(playlist, count) {
    // console.log(count === "");
    let state = count === "" ? "ui-disabled" : "ui-enabled";

    let tracklist = `<li data-theme="b" class="ui-btn ui-mini" >
                    <a href="#playlist-content" id=${playlist} class="${this.create_queue_song} ${state} ui-mini ui-btn ui-icon-false">${playlist}${count}
                    </a>
                    </li>`;
    return tracklist;
  }

  renderPl(playlist) {
    let self = this;
    let list = super.initRender(playlist, self.max); //inherit
    // console.log(playlist);
    list.forEach(function (plname, index) {
      let playlist = plname["playlist"];
      let count = plname["length"] >= 10 ? "10+" : plname["length"];
      if (count !== "") {
        count = `<span class="ui-li-count">${count}</span>`;
      }
      let tracklist = self.renderview(playlist, count);
      $(self.list).append(tracklist);
      $(self.list).listview("refresh");
    });
  }

  createPl() {
    super.createQueue();
  }

  initPlaylist() {
    let self = this;
    $.get("/playlist/reset").done(() => {
      $.get("/playlist/list", { max: self.max }).done((playlist) => {
        self.createPl();
        self.renderPl(playlist);
      });
    });
  }
}

class Content extends Playlist {
  constructor(page_max) {
    super(page_max);
    this.max = page_max;
    this.listCreated = false;
    this.createContent = "#list-content";
    this.createList = "content-list";
    this.list = `#${this.createList}`;
    this.create_queue_song = "content-song";
    this.queue_song = `.${this.create_queue_song}`;
  }
  highlight() {} //sup
  hlloaded() {
    let self = this;
    $(this.queue_song).each((i, el) => {
      let loaded = $(el).attr("loaded");
      $(el).addClass("ui-disabled");
    });
  }
  enqueue() {
    self = this;
    $.get("/playlist/name").done((name) => {
      console.log(name);
      $.get("playlist/enqueue", { name: name }).done((data) => {
        console.log(data);
      });
      self.hlloaded();
    });
  }
  disableLoad(index, list, el) {
    //super
    let load = list[index]["isload"];
    load === 1
      ? $(el).addClass("ui-disabled")
      : $(el).removeClass("ui-disabled");
  }

  get_attr(data) {
    //pipe data to set_attr
    // console.log('m',data)
    let metadata = data.map((content) => {
      let playlist = content["file"];
      let load = content["isload"];
      let crypt = content["iscrypt"];
      return { file: playlist, isload: load, iscrypt: crypt };
    });
    return metadata;
  }
  set_attr(index, list, el) {
    //pipe data from get_attr
    // console.log('a',list)
    let uri = list[index]["file"];
    let crypt = list[index]["iscrypt"] === undefined ? 0 : 1;
    $(el).attr("crypt", crypt);
    $(el).attr("id", uri);
    $(el).html(`${uri}`);
  }

  update(list) {
    super.updatePl(list);
  }
  refresh() {
    let self = this;
    $.get("/playlist/name").done((name) => {
      $.get("playlist/content", { name: name, max: self.max }).done(
        (content) => {
          // console.log('cref',content);
          self.update(content);
        }
      );
    });
  }

  render(content) {
    let self = this;
    content.forEach((track) => {
      let file = track["file"];
      let iscrypt = track["iscrypt"] === undefined ? 0 : 1;
      let state = track["isload"] === 1 ? "ui-disabled" : "ui-enabled";
      let tracklist = `<li data-theme="b" class="ui-btn ui-mini listview-content"><a href="#" id=${file}  crypt=${iscrypt} class="${self.create_queue_song} ${state} ui-mini ui-btn ui-icon-false">${file}</a></li>`;
      $(self.list).append(tracklist);
      $(self.list).listview("refresh");
    });
  }
  create() {
    super.createPl();
  }
  reset() {
    $(`.listview-content`).remove();
  }
  init(plname) {
    let self = this;
    $.get("/playlist/resetc").done(() => {
      $.get("playlist/content", { name: plname, max: self.max }).done(
        (content) => {
          console.log(self.max)
          self.reset();
          self.create();
          self.render(content);
        }
      );
    });
  }
}

let queue = new Queue(15);
let lib = new Library(15);
let pl = new Playlist(15);
let content = new Content(15);


var custom_event = $.support.touch ? "tap" : "click";

// SWIPE EVENT
$(document).on("mobileinit", function () {
  $(document).ready(function () {
    $("#queue-content").on("swipeleft", function (e) {
      queue.refresh();
    });
    $("#lib-content").on("swipeleft", function (e) {
      lib.refresh();
    });
    $("#playlist-content").on("swipeleft", function (e) {
      pl.refresh();
    });
    $("#list-content").on("swipeleft", function (e) {
      content.refresh();
    });
  });
});

// PAGE INIT

$(document).on("pageinit", "#queue", function (event) {
  queue.initQueue();
});

$(document).on("pageinit", "#browse", function (event) {
  console.log("initlib");
  lib.initLib();
});

$(document).on("pageinit", "#playlists", function (event) {
  console.log("initpl");
  pl.initPlaylist();
});

//PLaylist
$(document).on(custom_event, "#playlist-refresh", function () {
  pl.refresh();
});

$(document).on(custom_event, "#playlist-new", function () {
  // pl.refresh();
  $.get("/playlist/reset").done((data) => {
    pl.refresh();
  });
});

$(document).on(custom_event, ".playlist-song", function () {
  let id = $(this).attr("id");
  console.log('initpl')
  content.init(id);
});

$(document).on(custom_event, ".content-song", function () {
  let id = $(this).text();
  let crypt = $(this).attr("crypt");
  if (crypt != 1) {
    $(this).addClass("ui-disabled");
    $.get("/library/enqueue", { uri: id }).done((data) => {
      console.log(data);
    });
  }
});

$(document).on(custom_event, "#content-enqueue", function () {
  content.enqueue();
});

// Playlist End \\

// Library \\

$(document).on(custom_event, "#lib-load", function () {
  $.get("/library/load").done(function (stats) {
    console.log(stats);
    lib.hlloaded();
  });
});

$(document).on(custom_event, "#lib-ref", function () {
  lib.refresh();
});

$(document).on(custom_event, ".lib-song", function () {
  let txt = $(this).text();
  let crypt = $(this).attr("crypt");
  if (crypt != 1) {
    // if encrypt then skip
    $(this).addClass("ui-disabled");
    $.get("/library/enqueue", { uri: txt }).done((data) => {
      console.log(data);
    });
  }
});
// $(document).on(custom_event, "#lib-share", function () {
//   $.get('/library/share').done(function(stats){
//     console.log(stats)
//   })
// });

// Library End \\

// QUEUE \\

$(document).on(custom_event, "#queue-refresh", function () {
  queue.refresh();
});

$(document).on(custom_event, "#queue-new", function () {
  $.get("/queue/new").done(() => {
    queue.refresh();
  });
});

// $(document).on(custom_event, ".queue-song", function () {
//   let id = $(this).attr("id");
//   queue.play(id);
//   $.get("/playback/play", { id: id }).done((id) => {
//     console.log(id["songid"]);
//   });
// });

// QUEEU END \\
