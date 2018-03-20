console.log("heh")
var stop_padding = 5;
var replay_padding = 3;
// Below part is for vue app
var vue_app = new Vue({
  el: "#vue_app",
  delimiters: ['[[', ']]'],
  data:{
    state: "watching", // watching, enforced_replay, tagging
    current_marker: -1,
    collected_data: {},
    submittable: false,
  },
  methods:{
    add_data: function(event){
      var valence = $("input[name='valence']:checked").val()
      var arousal = $("input[name='arousal']:checked").val()
      var category = $("input[name='ekman']:checked").attr("id")
      var reasoning = $("#reasoning").val()
      if(valence==undefined || arousal==undefined || category==undefined || reasoning.length<8){
        alert("Select value, or write proper reasoning to proceed.")
      }else{
        var dict = {
          'valence' : valence,
          'arousal' : arousal,
          'category' : category,
          'reasoning' : reasoning,
        }
        this.collected_data[this.current_marker] = dict
        this.state='watching'
        $("#stop_marker_"+this.current_marker).removeClass("currentMarker").addClass("doneMarker")
        this.current_marker = -1;
        $("input[name='valence']").prop('checked', false)
        $("input[name='arousal']").prop('checked', false)
        $("input[name='ekman']").prop('checked', false)
        $("#reasoning").val("")
        if(Object.keys(this.collected_data).length==Object.keys(prompt_time).length){
          alert("Now you labeled character's emotion for all required moments. If you do not think revision is necessary, return with submit button below.")
          vue_app.submittable = true;
        }
        player.play()
      }
    }
  }
})

var maximal_time = 0;
var maximal_percentage;
var cur_time = 0;

// below is for setting up video functionalities
  //getting the video
var vjs_options = {
  controlBar: {
    volumePanel: {inline: false}
  },
}
var player = videojs('main_video', vjs_options)
  // when seeking for unseen video parts, return to current point
player.on('seeking', function(){
  console.log("seek")
  console.log(this.currentTime())
  if(this.currentTime()>maximal_time){
    this.currentTime(cur_time)
    alert("You cannot seek to unseen video time.")
  }
})
  // when maximal point is updated, update the value
player.on('timeupdate', function(){
  if(this.seeking()==false){
    cur_time = this.currentTime()
    if(cur_time > maximal_time){
      maximal_time = cur_time;
      $("#playedBar").css("width", (maximal_time/player.duration()*100).toString()+"%")
    }
  }
  if(vue_app.state == "tagging"){
    if(this.currentTime()>this.current_marker+replay_padding){
      this.pause();
      this.currentTime(this.current_marker+replay_padding)
    }
  }
})
// make div for signify how much a worker has seen
$(".vjs-progress-holder").prepend("<div id='playedBar' class='cyan lighten-3'></div>");

//generate markers for prompt
  //generate the data structure for markers
var markers=[];
for(var key in prompt_time){
  markers.push({
    time: key,
    text: "Task",
  })
  markers.push({
    time: parseFloat(key) + parseFloat(stop_padding),
    text: "Hidden",
    class: "HiddenMarker",
  })
}

player.markers({
  markerStyles:{
    'width': '3px',
  },
  onMarkerReached: function(marker){
    console.log(marker['key'])
    if(marker['time']<maximal_time){
      if(prompt_time[marker['time']]==false || parseFloat(marker['time'])==vue_app.current_marker){
        $("#main_video").css("border-color", "red");
        window.setTimeout(function(){
          $("#main_video").css("border-color", "transparent");
        }, 1000)
        if($("[data-marker-key='"+marker['key']+"']").attr('id')==undefined){
          $("[data-marker-key='"+marker['key']+"']").attr('id', 'stop_marker_'+marker['time'].toString())
        }
      }else if(prompt_time[marker['time']-stop_padding]==false){
        player.pause()
        $("#stop_marker_"+(marker['time']-stop_padding).toString()).addClass("currentMarker")
        vue_app.current_marker = marker['time']-stop_padding
        alert("Now You will be seen the part of the video (around the marker), and decide the character's emotional status.")
        prompt_time[marker['time']-stop_padding] = true;
        vue_app.state = 'enforced_replay';
        player.currentTime(player.currentTime()-stop_padding-replay_padding)
        player.play()
        player.controls(false)
        console.log(replay_padding*2000)
        window.setTimeout(enforce_replay, 2000*replay_padding)
      }
    }
  },
  onMarkerClick: function(marker){
    if(vue_app.state=="watching"){
      if($("[data-marker-key='"+marker['key']+"']").hasClass("doneMarker")){
        recast_data(marker['time'])
      }
    }
  },
  markers: markers,
})

function enforce_replay(){
  player.pause()
  player.controls(true)
  vue_app.state = "tagging";
}

function recast_data(marker_time){
  player.pause()
  vue_app.state="tagging";
  vue_app.current_marker = marker_time;
  $("#stop_marker_"+marker_time).removeClass('doneMarker').addClass('currentMarker')
  var val_val = vue_app.collected_data[marker_time]['valence']
  var aro_val = vue_app.collected_data[marker_time]['arousal']
  var ekman_val = vue_app.collected_data[marker_time]['category']
  var reasoning_val = vue_app.collected_data[marker_time]['reasoning']

  $("input[name='valence'][value='"+val_val.toString()+"']").prop('checked', true)
  $("input[name='arousal'][value='"+aro_val.toString()+"']").prop('checked', true)
  $("#"+ekman_val).prop('checked', true);
  $("#reasoning").val(reasoning_val)
}
