// $.get("/library/enqueue",{'uri':'Miaow-01-Tempered-song.mp3'})
// $.get("/playlist/enqueue",{'name':'pll'})
// $.get("/queue/list",{'max':3})
// $.get("/library/list",{'max':'2'})
// $.get("/playlist/content",{'name':'p','max':'5'})
// $.get("/playlist/add",{'name':'pl2','uri':'Miaow-01-Tempered-song2.mp3'})
// $.get("/playback/play",{'id':32})
// $.get("/queue/delete",{'id':1})
// $.get("/queue/reset",{'max':5})

// .done(function(data){
// 		// document.write(data)
// 		console.log(data)
// 		// $('#log').append('<br>' + $('<div/>').text(data[0]['file']))
// 		// sync.play()
// 		// console.log(data['title'])
// })

var socket;
$(document).ready(function(){
	namespace = '/rt/notify/';
    socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

	socket.on('event', function(msg) {
		// $('#log').append('<br>' + $('<div/>').text(msg.ev+msg.status['elapsed']+' '+msg.status['duration']).html());
		console.log(msg.ev)
		if(msg.ev == 'player'){
			if (msg.status['state'] == 'pause'){
				sync.stop()
			} else if(msg.status['state'] == 'play'){
				sync.play()
			}
		}
	});
});

// $(document).ready(function(){
// 	$("#pause").click(function () {
// 		sync.stop()
// 	})
// 	$("#stop").click(function(){
// 		$.get("/settings/offsync")
// 	})

// $.get("/queue/list", { max: 5 }).done(function (data) {
//   data.forEach((element) => {
//     let file = element["file"];
//     $("#songs").append(file);
//   });
// });

// $(document).ready(function () {
//   $("#pause").click(function () {
//     $.get("/playlist/content", { name: "p", max: "5" }).done(function (data) {
//       console.log(data);
//     });
//   });
// });
// 		// sync.play()
// 	})
// })

// $(document).on("pagebeforeshow", "#queue", function () {
//   $.get("/queue/list", { max: 5 }).done(function (data) {
//     data.forEach((element) => {
//       let file = element["file"];
//       $("#songs").append(file);
//     });
//   });
// });
// $(document).on("mobileinit", function () {
//   getListQueue();
//   getListLib();
// });


var custom_event = $.support.touch ? "tap" : "click";

$(document).on(custom_event, "#queue-refresh", function () {
  $(".queue-song").remove();
  getListQueue();
});

$(document).on(custom_event, "#queue-new", function () {
  $.get('/queue/new', (data) => {});
});

function getListQueue() {

  $.get("/queue/list", {
    max: 2,
  }).done(function (data) {
    data.forEach((track) => {
      let file = track["file"];
      let id = track["id"];
      appendToListQueue(file, id);
    });
  });
}

$(document).on(custom_event, ".queue-song", function () {
  var index = $(this).attr("queue-id");
});

var listCreatedQueue = false;

function appendToListQueue(song, id) {

  if (!listCreatedQueue) {
    $("#queue-content").append(
      "<ul id='queue-list' data-role='listview' data-inset='true'></ul>"
    );
    listCreatedQueue = true;
    $("#queue-content").trigger("create");
  }

  let list = `<li data-icon="false" queue-id=${id} class="queue-song" ><a href="#">${song}</a></li>`;
  
  $("#queue-list").append(list);
  $("#queue-list").listview("refresh");
}
export {getListQueue};
