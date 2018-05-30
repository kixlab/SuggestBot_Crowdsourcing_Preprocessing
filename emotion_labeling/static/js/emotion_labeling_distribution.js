
var stop_padding = 5;
var replay_padding = 3;
//var video_url;
var times=[];
var emotion_category =[
  'fearful', 'angry', 'sad', 'disgusted', 'happy', 'surprised', 'frustrated', 'depressed', 'excited', 'neutral'
]
for(var key in prompt_time){
  times.push(parseFloat(key))
}
times.sort(function(a, b){return a-b;})

//below is used for adaptive example condition
var cur_phase = undefined;

// Below part is for vue app
var vue_app = new Vue({
  el: "#vue_app",
  mixins: [additive_vue_app],
  delimiters: ['[[', ']]'],
  data:{
    state: "watching", // watching, enforced_replay, tagging
    tagging_phase: 0,
    current_marker: -1,
    replay_start_time: -1,
    tagging_max_time: -1,
    collected_data: {},
    submittable: false,
    condition: condition,
    video_url: video_url,
    proceed_action: "ADD",
    state_string: 'Video Watching',
    video_started: false,
    micro_browser: 0,
    likert_scale: likert_scale,
    likert_range1: Array.apply(null, Array(likert_scale)).map(function (_, i) {return i+1;}),
    likert_range2: Array.apply(null, Array(likert_scale)).map(function (_, i) {return i+1;}),
    total_distribution_token: 50,
    current_distribution_token: 0,
    old_input_value: -1,
    target_second: [],
    target_video_source: [],
    target_video_distribution: [],
    example_condition: 'distribution_video',// distribution, video, distribution_video
    cur_ex: 0,
  },
  methods:{
    //add label data to the colleted data-- for label and reason condition!
    add_data: function(message="add"){
      if(this.current_distribution_token != this.total_distribution_token){
        // if values are not filled make workers fill the values properly. (Escape)
        alert("Assign all tokens to the distribution.")
        return
      }else{
        // if values are filled, store them
        var av_array=[]
        for(i in this.likert_range1){
          v_array = []
          for(j in this.likert_range2){
            v_array.push(parseInt($("#a"+(parseInt(i)+1).toString()+"_v"+(parseInt(j)+1).toString()).val()))
          }
          av_array.push(v_array)
        }
        this.collected_data[this.current_marker] = av_array
      }


      // reset input fields

        $(".distribution_input").val(0)
        this.current_distribution_token = 0;
        this.old_input_value = -1;



        //change the state to 'watching' state

        this.calculate_current_distribution_token()
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
        vue_app.current_action_add()
        // play the video
        player.play()
        if(cur_phase!=undefined){
          clear_example()
        }
    },
    // return data to the backend-connected input field
    return_data: function(){
      to_return = {}
      to_return['labels'] = this.collected_data
      to_return['condition'] = condition
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
    grid_height: function(){
      return 313/likert_range1.length;
    },
    distribution_token_num_color: function(){
      if(this.current_distribution_token==this.total_distribution_token){
        return 'green'
      }else{
        return 'red'
      }
    },
    calculate_current_distribution_token: function(){
      var addition =0
      var av_array =[]
      if(cur_phase!=undefined){
        for(i in this.likert_range1){
          v_array = []
          for(j in this.likert_range2){
            v_array.push(parseInt($("#a"+(parseInt(i)+1).toString()+"_v"+(parseInt(j)+1).toString()).val()))
          }
          av_array.push(v_array)
        }
      }
      $(".distribution_input").map(function(_, e){
        addition += parseInt($(this).val())
        var th_=this
        $(this).parent().css('background-color', mapAColor($(th_).val()/vue_app.total_distribution_token))
      })
      if(addition<=this.total_distribution_token){
        if(cur_phase!=undefined){
          if(phase_info[cur_phase]==addition && phase_info[cur_phase]!=0){
            update_example_from_backend(av_array);

          }
        }

        this.current_distribution_token = addition;
        return true;
      }else{
        return false;
      }

    },
    h_axis_border: function(i, j){
      if(i==(this.likert_scale+1)/2 && j!=(this.likert_scale+1)/2){
        return true;
      }else{
        return false;
      }
    },
    v_axis_border: function(i, j){
      if(j==(this.likert_scale+1)/2 && i!=(this.likert_scale+1)/2){
        return true;
      }else{
        return false;
      }
    },
    color_distribution: function(av_array, grid_class='.distribution_input', prepend="", number=false){
      if(av_array==false){
        $(grid_class).css('background-color', 'transparent')
      }else{
      var tot = 0;
      for(i in av_array){
        for(j in av_array[i]){
          tot += av_array[i][j]
        }
      }
      console.log(tot)
      for(i in av_array){
        for(j in av_array[i]){
          if(number){
            if(Math.round(50*av_array[i][j]/tot)!=0){
                $("#ex_"+prepend+"a"+(parseInt(i)+1).toString()+"_v"+(parseInt(j)+1).toString()).text(Math.round(50*av_array[i][j]/tot))
            }
          }
          $("#"+prepend+"a"+(parseInt(i)+1).toString()+"_v"+(parseInt(j)+1).toString()).parent().css('background-color', mapAColor(av_array[i][j]/tot))

        }
      }
    }
    },
    a_v_pic_width: function(){
      return ($("#table_row").width()/12).toString()+'px';
    },
    a_v_pic_top: function(){
      return (313/2 - $("#table_row").width()/24).toString() + 'px';
    },
    mouse_over_example: function(idx){
      if(this.example_condition.includes("distribution")){
          //$(".distribution_input").css("visibility","hidden")
          $(".distribution_ex_combined").css("display","")
          console.log(idx)
          this.color_distribution(av_array=this.target_video_distribution[idx], grid_class='.distribution_input_case', prepend="", number=true)
      }
    },
    mouse_out_example: function(){
      if(this.example_condition.includes("distribution")){
        //$(".distribution_input").css("visibility","visible")
        $(".distribution_ex_combined").css("display","none")
        $(".distribution_ex_combined").text("")
          this.calculate_current_distribution_token()
      }
    },
    click_example: function(idx){
      if(this.example_condition.includes("video")){
        this.cur_ex = idx
        player.pause()
        //init video
        //turn on modal
        video_update_blinking_and_stop('example_video', this.target_second[idx])
        $("#single_video").modal('open')
      }
    },
    video_source: function(){
      if(example_video != undefined){
        example_video.src = this.target_video_source[this.cur_ex]
      }

      return this.target_video_source[this.cur_ex]
    }
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
  $(".distribution_input").on('focusin', function(){
    console.log($(this).val())
    vue_app.old_input_value = $(this).val()
  }).on('input', function(){
    console.log($(this).val())
    if(vue_app.calculate_current_distribution_token()){
      vue_app.old_input_value = $(this).val()
    }else{
      $(this).val(vue_app.old_input_value);
    }

  })
  vue_app.calculate_current_distribution_token()

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
  $(".vjs-control-bar").append("<button id='replay_btn' class='vjs-control vjs-button' onclick='replay()'></button>")
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
  if(cur_phase != undefined){
    if(phase_info[cur_phase]==0){
      update_example_from_backend()
    }
  }
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

function replay(){
  if(vue_app.current_marker != -1){
    player.currentTime(vue_app.current_marker - replay_padding)
    vue_app.state = 'enforced_replay';
    player.play()
    player.controls(false)
    console.log(replay_padding*2000)
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
          replay()
          vue_app.current_action_add()
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
}

$("a").on('mouseover', function(){
  $(this).css("color", "#d50000")
}).on('mouseout', function(){
  $(this).css("color","")
})

  color_mapper_gradient_color('color_legend')


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
