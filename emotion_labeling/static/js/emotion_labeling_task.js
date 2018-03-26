
var stop_padding = 5;
var replay_padding = 3;
var video_url;
if(condition.includes("experiment")){
  video_url = "https://github.com/kixlab/suggestbotData/blob/master/experiment/"+primitive_video_url+".mp4?raw=true"//media/uniform/"+primitive_video_url+".mp4?raw=true"
}



// Below part is for vue app
var vue_app = new Vue({
  el: "#vue_app",
  delimiters: ['[[', ']]'],
  data:{
    step: step,
    state: "watching", // watching, enforced_replay, tagging
    current_marker: -1,
    tagging_max_time: -1,
    collected_data: {},
    submittable: false,
    condition: condition,
    video_url: video_url,
  },
  methods:{
    //add label data to the colleted data-- for label and reason condition!
    add_data: function(message="add"){
      // for the labeling condition
      if(this.step=="label_and_reason"){
        // to prefill the field
        if(condition == "experiment_baseline"){
          $("#reasoning").val("No Reasoning")
        }
        //retrieve values from the interface
        var valence = $("input[name='valence']:checked").val()
        var arousal = $("input[name='arousal']:checked").val()
        var category = $("input[name='ekman']:checked").attr("id")
        var reasoning = $("#reasoning").val()
        if(message=="no_figure"){
          // if worker decided that no character exist, then store string that signify that no figure exists
          this.collected_data[this.current_marker] = "no_figure"
        }else{
          //else,
          if(valence==undefined || arousal==undefined || category==undefined || reasoning.length<8){
            // if values are not filled make workers fill the values properly. (Escape)
            alert("Select values, or write proper reasoning to proceed.")
            return
          }else{
            // if values are filled, stor them
            var dict = {
              'valence' : valence,
              'arousal' : arousal,
              'category' : category,
              'reasoning' : reasoning,
            }
            this.collected_data[this.current_marker] = dict
          }
        }

      }else if(this.step=='sanity_check'){
        // for the sanity check step
        var check_result = $("input[name='check']").prop('checked')
        if(check_result ==undefined){
          alert("Please check whether the reasoning makes sense")
          return
        }else{
          var aid = label_to_check[this.current_marker]['label_aid']
          var wid = label_to_check[this.current_marker]['label_wid']
          var dict = {
            'qualified' : check_result,
            'label_aid' : aid,
            'label_wid' : wid,
          }
          this.collected_data[this.current_marker] = dict

        }
      }
      // reset input fields
      $("input[name='valence']").prop('checked', false)
      $("input[name='arousal']").prop('checked', false)
      if(this.step=='label_and_reason'){
        $("input[name='ekman']").prop('checked', false)
        $("#reasoning").val("")
      }else if(this.step=='sanity_check'){
        $(".emotion_word_check").removeClass('emotion_word_check_highlighted')
        $("#current_reasoning").text("")
        $("input[name='check']").prop('checked', false)
      }



        //change the state to 'watching' state
        this.state='watching'
        //change marker to 'done status'
        $("#stop_marker_"+this.current_marker).removeClass("currentMarker").addClass("doneMarker")
        // reset current marker variable
        this.current_marker = -1;
        // when all the necessary markers are done, enable submit function
        if(Object.keys(this.collected_data).length==Object.keys(prompt_time).length){
          alert("Now you labeled character's emotion for all required moments. If you do not think revision is necessary, return with submit button below.")
          vue_app.submittable = true;
        }
        // play the video
        player.play()

    },
    // return data to the backend-connected input field
    return_data: function(){
      to_return = {}
      to_return['labels'] = this.collected_data
      to_return['condition'] = condition
      $("#to_return").val(JSON.stringify(to_return))
    },
    no_figure_option: function(){
      return (this.step=='label_and_reason' && this.condition=='data_collection')
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
player.src(video_url)
  // when seeking for unseen video parts, return to current point
player.on('seeking', function(){
  //make workers unable to see futher the seen range
  if(this.currentTime()>maximal_time){
    this.currentTime(cur_time)
    alert("You cannot seek to unseen video time.")
  }
})

player.on('timeupdate', function(){
    // when maximal point is updated, update the value
  if(this.seeking()==false){
    cur_time = this.currentTime()
    if(cur_time > maximal_time){
      maximal_time = cur_time;
      $("#playedBar").css("width", (maximal_time/player.duration()*100).toString()+"%")
    }
  }
  // while doing the task, limit the range of the video time that workers can check
  if(vue_app.state == "tagging"){
    if(this.currentTime()>vue_app.tagging_max_time-replay_padding){
      this.pause();
      this.currentTime(vue_app.tagging_max_time-replay_padding)
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
  markerStyle:{
    'width': '5px',
    'border-radius' : '0%',

  },
  onMarkerReached: function(marker){
    // only when the worker did saw the marked time before
    if(marker['time']<maximal_time){
      // when passing through markered time to be labeled
      if(prompt_time[marker['time']]==false || parseFloat(marker['time'])==vue_app.current_marker){
        //make it blink in red
        $("#main_video").css("border-color", "red");
        window.setTimeout(function(){
          $("#main_video").css("border-color", "transparent");
        }, 1000)
        // give the marker id :)
        if($("[data-marker-key='"+marker['key']+"']").attr('id')==undefined){
          $("[data-marker-key='"+marker['key']+"']").attr('id', 'stop_marker_'+marker['time'].toString())
        }
      }else if(prompt_time[marker['time']-stop_padding]==false){
        //if reached blue marker is not done yet
        //make them rewatch!
        player.pause()
        $("#stop_marker_"+(marker['time']-stop_padding).toString()).addClass("currentMarker")
        vue_app.current_marker = marker['time']-stop_padding

        var keys = Object.keys(prompt_time);
        var key_idx = keys.indexOf(vue_app.current_marker.toString())
        if(key_idx<keys.length){
          vue_app.tagging_max_time = parseFloat(keys[key_idx+1])
        }else{
          vue_app.tagging_max_time = player.duration()+replay_padding
        }

        alert("Now You will rewatch the part of the video where you need to label on, and after that you will begin labeling.")
        prompt_time[marker['time']-stop_padding] = true;
        vue_app.state = 'enforced_replay';
        player.currentTime(player.currentTime()-stop_padding-replay_padding)
        player.play()
        player.controls(false)
        console.log(replay_padding*2000)
        window.setTimeout(after_replay, 2000*replay_padding)
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

// after rewatching
function after_replay(){
  if(vue_app.step=="sanity_check"){
    posting_data(label_to_check, vue_app.current_marker)
  }
  player.pause()
  player.controls(true)
  vue_app.state = "tagging";
}

//recast data to the input field, for emotion labeling and reasoning
function recast_data(marker_time){
  player.pause()
  vue_app.state="tagging";
  vue_app.current_marker = parseFloat(marker_time);

  var keys = Object.keys(prompt_time);
  var key_idx = Object.keys(vue_app.collected_data).length;
  if(key_idx<keys.length){
    vue_app.tagging_max_time = parseFloat(keys[key_idx])
  }else{
    vue_app.tagging_max_time = player.duration()+replay_padding
  }

  $("#stop_marker_"+marker_time).removeClass('doneMarker').addClass('currentMarker')
  if(vue_app.step=='label_and_reason'){
    if(vue_app.collected_data[marker_time]!= 'no_figure'){
      posting_data(vue_app.collected_data, marker_time)
    }
  }else if(vue_app.step=='sanity_check'){
    posting_data(label_to_check, marker_time)
    var checked = vue_app.collected_data[marker_time]
    if(checked){
      checked = "check_yes"
    }else{
      checked = "check_no"
    }
    $("#"+checked).prop('checked', true)
  }


}

function posting_data(dict, marker_time){
  var val_val = dict[marker_time]['valence']
  var aro_val = dict[marker_time]['arousal']
  var ekman_val = dict[marker_time]['category']
  var reasoning_val = dict[marker_time]['reasoning']

  $("input[name='valence'][value='"+val_val.toString()+"']").prop('checked', true)
  $("input[name='arousal'][value='"+aro_val.toString()+"']").prop('checked', true)
  if(vue_app.step=="label_and_reason"){
    $("#"+ekman_val).prop('checked', true);
    $("#reasoning").val(reasoning_val)
  }else if(vue_app.step=="sanity_check"){
    $("#"+ekman_val+"_check").addClass("emotion_word_check_highlighted")
    $("#current_reasoning").text(reasoning_val)

  }

}
