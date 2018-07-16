
var stop_padding = 5;
var replay_padding = 3;
//var video_url;
var times=[];
var emotion_categories =[
  'fearful', 'angry', 'sad', 'disgusted', 'happy', 'surprised', 'frustrated', 'depressed', 'excited', 'neutral', 'other'
]
for(var key in prompt_time){
  times.push(parseFloat(key))
}
times.sort(function(a, b){return a-b;})

//below is used for adaptive example condition
var cur_phase = undefined;


var emo_checked = {}
for(idx in emotion_categories){
  emo_checked[emotion_categories[idx]] =false
}

// Below part is for vue app
var vue_app = new Vue({
  el: "#vue_app",
  mixins: [additive_vue_app],
  delimiters: ['[[', ']]'],
  data:{
    state: "watching", // watching, enforced_replay, tagging
    tagging_phase: 0,
    final_phase: 1,
    current_marker: -1,
    replay_start_time: -1,
    tagging_max_time: -1,
    collected_data: {},
    submittable: false,
    video_url: video_url,
    proceed_action: "ADD",
    state_string: 'Video Watching',
    video_started: false,
    micro_browser: 0,
    total_distribution_token: 50,
    current_distribution_token: 0,
    old_input_value: -1,
    target_second: [],
    target_video_source: [],
    target_video_distribution: [],
    example_condition: 'distribution_video',
    emotion_categories: emotion_categories,// distribution, video, distribution_video
    cur_ex: 0,
    NASA_questions: {
      'mental_demand': {
        'name' : 'Mental Demand',
        'question' : "How mentally demanding was the task?",
        'low_end' : 'Very Low',
        'high_end' : 'Very High'
      },
      'physical_demand': {
        'name' : 'Physical Demand',
        'question' : "How physically demanding was the task?",
        'low_end' : 'Very Low',
        'high_end' : 'Very High'
      },
      'temporal_demand': {
        'name' : 'Temporal Demand',
        'question' : "How hurried or rushed was the pace of the task?",
        'low_end' : 'Very Low',
        'high_end' : 'Very High'
      },
      'performance': {
        'name' : 'Performance',
        'question' : "How successful were you in accomplishing what you were asked to do?",
        'low_end' : 'Perfect',
        'high_end' : 'Failure'
      },
      'effort': {
        'name' : 'Effort',
        'question' : "How hard did you have to work to accomplish your level of performance?",
        'low_end' : 'Very Low',
        'high_end' : 'Very High'
      },
      'frustration': {
        'name' : 'Frustration',
        'question' : "How insecure, discouraged, irritated, stressed, and annoyed were you?",
        'low_end' : 'Very Low',
        'high_end' : 'Very High'
      }
    },
    emo_checked : emo_checked,
    task_start_time: undefined,
    task_end_time: undefined,
    cur_other: "",
  },
  methods:{
    //add label data to the colleted data-- for label and reason condition!
    add_data: function(message="add"){
      // add data into data structure
      this.collected_data[this.current_marker] = {}
      vue_app.task_end_time = new Date();
      /*nasa_dict = {}
      for(key in this.NASA_questions){
        nasa_dict[key] = parseInt($("input[name='"+key+"']:checked").attr('val'))
      }
      this.collected_data[this.current_marker]['survey_result'] = nasa_dict
      */
      emo_dict = {}
      for(key in emo_checked){
        if(key=='other' && this.emo_checked[key]){
          this.collected_data[this.current_marker]['other'] = $("#other_text").val()
        }
        if(this.emo_checked[key]){
          emo_dict[key] = parseInt($("input[name='"+key+"_confidence']:checked").attr('val'))
        }else{
          emo_dict[key] = 0
        }
      }
      this.collected_data[this.current_marker]['emotion_confidence'] = emo_dict

      this.collected_data[this.current_marker]['start_time'] = this.task_start_time.toUTCString()
      this.collected_data[this.current_marker]['end_time'] = this.task_end_time.toUTCString()
      // reset input fields

        $("input[type='radio']").prop('checked', false);
        $("input[type='checkbox']").prop('checked', false);
        $("#other_text").val("")

        //change the state to 'watching' state

        this.state='watching'
        $('#replay_btn').css("visibility","hidden")
        //change marker to 'done status'
        $("#maxBar").css("width", "0%");
        $(".emotion_marker").removeClass("HiddenMarker")
        $("#stop_marker_"+this.current_marker).removeClass("currentMarker").addClass("doneMarker")
        // reset current marker variable
        this.current_marker = -1;
        // when all the necessary markers are done, enable submit function
        if(Object.keys(this.collected_data).length==Object.keys(prompt_time).length){
          alert("Now you labeled character's emotion for all required moments. If you do not think revision is necessary, return with submit button below.")
          vue_app.submittable = true;
        }
        for(key in this.emo_checked){
          this.emo_checked[key] = false;
        }
        vue_app.task_start_time = undefined
        vue_app.task_end_time = undefined
        this.tagging_phase = 0
        vue_app.current_action_add()
        // play the video
        player.play()
        if(cur_phase!=undefined){
          clear_example()
        }
    },
    // return data to the backend-connected input field
    return_data: function(){
      to_return = this.collected_data
      $("#to_return").val(JSON.stringify(to_return))
    },
    no_figure_option: function(){
      return (this.condition=='data_collection')
    },
    current_action_add: function(){
      this.proceed_action = "ADD"
    },
    current_action_revise: function(){
      this.proceed_action = "REVISE"
    },
    jump_to_exact_frame: function(){

      player.currentTime(this.current_marker+this.micro_browser/10);
      this.micro_browser= (this.micro_browser+1)%10;
    },
    revision_description_enabled: function(){
      if(this.proceed_action=="REVISE"){
        if(!this.submittable){
          return "proceed"
        }else{
          return "submit"
        }
      }
    },
    is_submittable: function(){
      if(this.submittable && this.state=='watching'){
        return true;
      }else{
        return false;
      }
    },
    Task_end: function(){
      vue_app.task_end_time = new Date();
      this.tagging_phase += 1;
    },
    phase_change: function(num){
      this.tagging_phase += num;
    },
    Radio_Checked_Exists: function(){
      pass = false
      other = true
      if($("input[name='emotion_category']").is(":checked")){
        $("input[name='emotion_category']:checked").map(function(_,e){
          if($(e).attr("id")=="other"){
            if($("#other_text").val().length >0){
              pass = true
            }else{
              other = false
            }
          }
          pass=true
        })
      }
      return (pass && other)
    },
    Confidence_Done: function(){
      pass = true
      for(key in this.emo_checked){
        if(this.emo_checked[key]){
          if(!$("input[name='"+key+"_confidence']").is(":checked")){
            pass=false
          }
        }
      }
      return pass
    },
    NASA_TLX_Done: function(){
      for(key in this.NASA_questions){
        if(!$("input[name='"+key+"']").is(":checked")){
          return false;
        }
      }
      return true;
    },
    input_change: function(key){
      if($("#"+key).is(":checked")){
        this.emo_checked[key] = true
      }else{
        this.emo_checked[key] = false
      }

    },


  }
})

var maximal_time = 0;
var maximal_percentage;
var cur_time = 0;

var player;
// below is for setting up video functionalities
  //getting the video

$(document).ready(function(){
//  document.getElementById('main_video').onloadedmetadata = function(){
      //load_markers()
//  }
  initialize_main_video()

})

function initialize_main_video(){
  $("#start_time").val(localDateTime)
  player = videojs('main_video')

  player.src(video_url)
    // when seeking for unseen video parts, return to current point
  player.on('seeking', function(){
    //make workers unable to see futher the seen range
    if(this.currentTime()>maximal_time){
      this.currentTime(cur_time)
      alert("You cannot seek to unseen video time.")
    }
  })
  player.on('play', function(){
    if(!vue_app.video_started){
      vue_app.video_started = true;
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
  load_markers()

  // make div for signify how much a worker has seen, replay button, etc
  $(".vjs-control-bar").append("<button id='replay_btn' class='vjs-control vjs-button' onclick='replay(false)'></button>")
  $("#replay_btn").append("<i class='small material-icons' style='margin-top: 5px; font-size:20px;'>replay</i>")
  $(".vjs-progress-holder").prepend("<div id='playedBar' class='cyan lighten-3'></div>");
  $(".vjs-progress-holder").prepend("<div id='maxBar' style='float:right; height: 100%; background-color: black; width: 0%;'></div>");

}

//generate markers for prompt
  //generate the data structure for markers
var markers=[];

// after rewatching
function after_replay(){
  player.pause()
  player.controls(true)
  vue_app.micro_browser = 0;
  vue_app.state = "tagging";
  vue_app.state_string = "Labeling Emotion"
  $('#replay_btn').css("visibility","visible")
  // for adaptive example
}

//recast data to the input field, for emotion labeling and reasoning
function recast_data(marker_time){
  player.pause()
  vue_app.state="tagging";
  $('#replay_btn').css("visibility","visible")
  vue_app.current_marker = parseFloat(marker_time);
  vue_app.replay_start_time = vue_app.current_marker-replay_padding
  var keys = Object.keys(prompt_time);
  var key_idx = Object.keys(vue_app.collected_data).length;
  if(key_idx<keys.length){
    vue_app.tagging_max_time = parseFloat(keys[key_idx])
  }else{
    vue_app.tagging_max_time = player.duration()+replay_padding
  }
  var stopper_percentage = (1-vue_app.tagging_max_time/player.duration())*100
  $("#maxBar").css("width", stopper_percentage.toString()+"%")
  $(".emotion_marker").addClass("HiddenMarker")
  $("#stop_marker_"+marker_time).removeClass('doneMarker').removeClass("HiddenMarker").addClass('currentMarker')

    if(vue_app.collected_data[marker_time]!= 'no_figure'){
      posting_data(vue_app.collected_data, marker_time)
    }

  vue_app.current_action_revise()

  // for adaptive example condition
  if(cur_phase != undefined){
    cur_phase = phase_info.length
  }
}

function posting_data(dict, marker_time){
  var av_array = dict[marker_time]

  for(i in av_array){
    for(j in av_array[i]){
      $("#a"+(parseInt(i)+1).toString()+"_v"+(parseInt(j)+1).toString()).val(av_array[i][j])
    }
  }
  vue_app.calculate_current_distribution_token();


}

function replay(is_initial){
  if(vue_app.current_marker != -1){
    player.currentTime(vue_app.current_marker - replay_padding)
    vue_app.state = 'enforced_replay';
    player.play()
    player.controls(false)
    console.log(replay_padding*2000)
    if(is_initial){
      vue_app.task_start_time = new Date();
      vue_app.task_start_time.setSeconds(vue_app.task_start_time.getSeconds() + 2*replay_padding);
    }
    window.setTimeout(after_replay, 2000*replay_padding)
  }
}

function load_markers(){
  for(var key in prompt_time){
    markers.push({
      time: parseFloat(key),
      text: "Task",
      class: "emotion_marker",
    })
    var t = parseFloat(key) + parseFloat(stop_padding)
    if(t>player.duration()){
      t = player.duration()-1
      console.log('overflow')
      markers.push({
        time: t,
        text: "Hidden",
        class: "HiddenMarker",
        last: parseFloat(key),
      })
    }else{
      markers.push({
        time: t,
        text: "Hidden",
        class: "HiddenMarker",
      })
    }

  }

  player.markers({
    markerStyle:{
      'width': '5px',
      'border-radius' : '0%',
    },
    onMarkerReached: function(marker){
      console.log('reached')
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
        }else if(prompt_time[marker['time']-stop_padding]==false || prompt_time[marker['last']]==false){
          //if reached blue marker is not done yet
          //make them rewatch!
          player.pause()

          $(".emotion_marker").addClass("HiddenMarker")
          $("#stop_marker_"+(marker['time']-stop_padding).toString()).removeClass("HiddenMarker").addClass("currentMarker")
          if(marker['time']==player.duration()-1){
            vue_app.current_marker = marker['last'];
          }else{
            vue_app.current_marker = marker['time']-stop_padding
          }


          var keys = Object.keys(prompt_time);
          var key_idx = keys.indexOf(vue_app.current_marker.toString())
          if(key_idx<keys.length-1){
            vue_app.tagging_max_time = parseFloat(keys[key_idx+1])
          }else{
            vue_app.tagging_max_time = player.duration()+replay_padding
          }

          var stopper_percentage = (1-vue_app.tagging_max_time/player.duration())*100
          $("#maxBar").css("width", stopper_percentage.toString()+"%")

          alert("Now You will rewatch the part of the video where you need to label on, and after that you will begin labeling.")
          vue_app.replay_start_time = vue_app.current_marker-replay_padding
          prompt_time[vue_app.current_marker] = true;

          /*if(marker['time']==player.duration()-1){
            player.currentTime(player.duration()-1-replay_padding)
            prompt_time[marker['last']] = true;
          }else{
            player.currentTime(player.currentTime()-stop_padding-replay_padding)
            prompt_time[marker['time']-stop_padding] = true;
          }*/
          replay(true)
          vue_app.current_action_add()
        }
      }
    },
    onMarkerClick: function(marker){
      if(vue_app.state=="watching"){
        if($("[data-marker-key='"+marker['key']+"']").hasClass("doneMarker")){
          //recast_data(marker['time'])
        }
      }
    },
    markers: markers,
  })
}

$("a").on('mouseover', function(){
  $(this).css("color", "#d50000")
}).on('mouseout', function(){
  $(this).css("color","")
})


function reinitialize_main_video(){
  markers =[]
  if(player!=undefined){
    if(player.markers!=undefined){
      player.markers.destroy()
    }
    player.dispose()
  }

  $("#main_video").remove()
  $("#main_video_container").append('<video id="main_video" class="video-js" style="margin:auto;"></video>')
  $("#main_video").attr('data-setup', '{ "width": 560, "height": 315, "controls": true, "preload": "auto","inactivityTimeout": 0, "controlBar":{"volumePanel":{"inline":false}} }')
  initialize_main_video();
}

$("input").on('input' ,function(){
  vue_app.$forceUpdate()
}).on('keypress', function(){
  vue_app.$forceUpdate()
}).on('keyup', function(){
  vue_app.cur_other = $("#other_text").val()
}).on('click', function(){
  vue_app.$forceUpdate()
})
