
var stop_padding = 5;
var replay_padding = 3;
var video_url;
var times=[];
var emotion_category =[
  'fearful', 'angry', 'sad', 'disgusted', 'happy', 'surprised', 'frustrated', 'depressed', 'excited', 'neutral'
]
/*var motor_expression_dict={
  'smiling' : 'Smiling', 'mouth_opening' : 'Mouth Opening', 'mouth_closing' : 'Mouth Closing', 'mouth_tensing' : "Mouth Tensing",
  'frown' : "Frown", 'tears' : "Tears", 'eyes_opening' : 'Eyes Opening', 'eyes_closing' : 'Eyes Closing',
  'volume_increasing' : 'Volume Increasing', 'volume_decreasing' : "Volume Decreasing", 'v_trembling' : "Voice Trembling", 'v_assertive' : "Voice Being Assertive",
  'g_abrupt' : 'Abrupt Bodily Movements', 'moving_towards' : "Moving Towards People or Things", 'withdrawing' : "Withdrawing From People or Things",
  'against' : "Moving Against People or Things", 'silence' : 'Silence', 'short_utterance' : 'Short Utterance', 'long_utterance' : 'Long Utterance',
  's_melody' : "Speech Melody Change", 's_disturbance' : "Speech Disturbance", 's_tempo' : 'Speech Tempo Change'
}
var physio_expression_dict={
  'shiver': 'Feeling Cold Shivers', 'pale': 'Getting Pale', 'breathing_slow': 'Breathing Slowing Down', 'breathing_faster': 'Breathing Getting Faster',
  'sweating': 'Sweating', 'blushing': 'Blushing'
}*/

for(var key in prompt_time){
  times.push(parseFloat(key))
}
times.sort(function(a, b){return a-b;})
if(condition.includes("experiment")){
  video_url = $.parseHTML(primitive_video_url)[0].textContent;//media/uniform/"+primitive_video_url+".mp4?raw=true"
}

// Below part is for vue app
var vue_app = new Vue({
  el: "#vue_app",
  delimiters: ['[[', ']]'],
  data:{
    state: "watching", // watching, enforced_replay, tagging
    tagging_phase: 0,
    current_marker: -1,
    replay_start_time: -1,
    tagging_max_time: -1,
    collected_data: {},
    submittable: false,
    micro_browser:0,
    condition: condition,
    video_url: video_url,
    proceed_action: "ADD",
    cur_motor_exp: [],
    cur_physio_exp: [],
    cur_cog_motiv_exp: "",
    state_string: 'Video Watching',
    video_started: false,
    silent_checked:{},
    playPromise: undefined,
    questions: [
        {name:'smiling', question: 'The character is smiling.', positive: 'Definitely', negative: 'Not at all', image: true, not_sure: true},
        {name:'mouth_close_open', question: 'The mouth is...', positive: 'Opening', negative: 'Closing', not_sure: true},
        {name:'mouth_tensing', question: 'The mouth is tensing.', positive: 'Definitely', negative: 'Not at all', image:true, not_sure: true},
        {name:'frowning', question: 'The character is frowning.', positive: 'Definitely', negative: 'Not at all', image:true, not_sure: true},
        {name:'tear', question: 'The tear is coming out from the character.', positive: 'Definitely', negative: 'Not at all', not_sure: true},
        {name:'eyes_close_open', question: 'The eyes are....', positive: 'Opened', negative: 'Closed', not_sure: true},
        {name:'utterance_length', question: 'The character is silent / having short utterance / having long utterance.', positive: 'Having long utterance', negative: 'Silent', not_sure: true},
        {name:'body_abrupt', question: 'The body is abruptly moving.', positive: 'Definitely', negative: 'Not at all', not_sure: true},
        {name:'towards', question: 'The character is moving towards people or things.', positive: 'Definitely', negative: 'Not at all', not_sure: true},
        {name:'withdrawing', question: 'The character is withdrawing from people or things.', positive: 'Definitely', negative: 'Not at all', not_sure: true},
        //below special case
        {name:'voice_volume', question: 'The voice volume is....', positive: 'Increased', negative: 'Decreased', not_sure: true, silent_related: true},
        {name:'voice_trembling', question: 'The voice is trembling.', positive: 'Definitely', negative: 'Not at all', not_sure: true, silent_related: true},
        {name:'voice_assertive', question: 'The voice is assertive', positive: 'Assertive', negative: 'Timid', not_sure: true, silent_related: true},
        {name:'against', question: 'The character is moving against people or things.', positive: 'Definitely', negative: 'Not at all', not_sure: true},
        {name:'shiver', question: 'The character is feeling cold shivers.', positive: 'Definitely', negative: 'Not at all', not_sure: true},
        {name:'pale', question: 'The character is getting pale.', positive: 'Definitely', negative: 'Not at all', not_sure: true},
        {name:'speech_melody', question: 'The speech melody is changing.', positive: 'Definitely', negative: 'Not at all', not_sure: true, silent_related: true},
        {name:'speech_disturbed', question: 'The speech is being disturbed.', positive: 'Definitely', negative: 'Not at all', not_sure: true, silent_related: true},
        {name:'speech_tempo', question: 'The speech tempo is...', positive: 'Fast', negative: 'Slow', not_sure: true, silent_related: true},
        {name:'breathing', question: 'The character breathing is...', positive: 'Fast', negative: 'Slow', not_sure: true},
        {name:'sweating', question: 'The character is sweating.', positive: 'Definitely', negative: 'Not at all', not_sure: true},
        {name:'blushing', question: 'The character is blushing.', positive: 'Definitely', negative: 'Not at all', not_sure: true},

        {name:'sudden', question: 'How suddenly or abruptly did the event occur?', positive: 'Very suddenly', negative: 'Not suddenly at all',},
        {name:'probable', question: 'How probable is the occurence of the event in general?', positive: 'Very probable', negative: 'Not probable at all',},
        {name:'pleasant', question: 'How pleasant or unpleasant is the event in general, independent of the current situation?', positive: 'Very pleasant', negative: 'Very unpleasant',},
        {name:'chance', question: 'How likely is it that the event was mostly caused by chance or natural causes?', positive: 'Very likely', negative: 'Very unlikely',},
        {name:'own', question: "How likely is it that the the event was mostly caused by the character's own behavior?", positive: 'Very likely', negative: 'Very unlikely',},
        {name:'other', question: "How likely is it that the event was mostly caused by someone else's behavior?", positive: 'Very likely', negative: 'Very unlikely',},
        // special case below
        {name:'intentionally', question: "If the event is caused by a behavior, how likely is it that the event was caused intentionally?", positive: 'Very likely', negative: 'Very unlikely', info: "If you do think the event is caused by chance or natural causes, select 'Very unlikely'"},
        {name:'norm', question: "How likely is it that the event violated laws or social norms?", positive: 'Very likely', negative: 'Very unlikely',},
        {name:'goal', question: "How important / relevant is the event to the person's current goals or needs?", positive: 'Very important', negative: 'Not important at all',},
        {name:'expected', question: "How different is the event from what the person expected at this moment?", positive: 'Very different', negative: 'Not different at all',},
        {name:'consistency', question: "How likely is it that the event would be consistent with the person's ideal image of him / herself?", positive: 'Very consistent', negative: 'Not consistent at all',},
        {name:'envisaged', question: "Can the potential consequences of the event be clearly predicted and may they occur in the near future?", positive: 'Definitely', negative: 'Not at all',},
        {name:'consequence', question: "How likely will the consequences of the event bring positive / negative, desirable / undesirable outcomes to the person?", positive: 'Very positive', negative: 'Very negative',},
        {name:'immediate', question: "Did the event require the person to react immediately?", positive: 'Definitely', negative: 'Not at all',},
        {name:'avoidable', question: "Could the consequences of the event still be avoided or modified to the person's advantage?", positive: 'Definitely', negative: 'Not at all',},
        {name:'adjustable', question: "Would the person be able to live with, and adjust to, the consequences of the event?", positive: 'Definitely', negative: 'Not at all',},
        {name:'attention_event', question: "Is the character moving attention towards the event, or away from the event?", positive: 'Moving attention towards the event', negative: 'Moving attention away from the event',},
        {name:'searching_info', question: "Is the character searching information?", positive: 'Definitely', negative: 'Not at all',},
        {name:'attention_people', question: "Is the character's attention self-centered or directed towards others?", positive: 'Directed towards others', negative: 'Self-centered',},
        {name:'physical_event', question: "Is the character physically moving towards the event, or physically moving away from the event?", positive: 'Physically moving towards', negative: 'Physically moving away',},
    ],
    question_show_num: [4, 6, 6, 6, 7, 7, 6],
    question_page: 7,
    //cur_motiv_exp: "",
  },
  methods:{
    //add label data to the colleted data-- for label and reason condition!
    add_data: function(message="add"){

        //retrieve values from the interface
        var valence = $("input[name='valence']:checked").val()
        var arousal = $("input[name='arousal']:checked").val()
        var category = $("input[name='ekman']:checked").attr("id")
        var minor_category = []
        var other_check=false;
        var component_process = {}
        minor_category.push(category)
        $("input[name='ekman_mul']:checked").map(function(_, e){
          var topush;
          if($(e).val() != "other"){
            topush=$(e).val()
          }else{
            var other_val = $("#for_other").val()
            if(other_val.length==0){
              alert("Please specify what is 'other' emotion.")
              other_check=true;
            }
            topush=$("#for_other").val()
          }
          if(minor_category.indexOf(topush)<0){
            minor_category.push(topush)
          }

        })
        if(category == 'other'){
          category = $("input[name='for_other']").val()
          if(category.length==0){
            alert("Please specify what is 'other' emotion.")
            other_check=true;
          }
        }
        if(other_check){
          return;
        }
        for(i in this.questions){
          if($("input[name='"+this.questions[i]['name']+"']:checked").val()=="-1"){
            component_process[this.questions[i]['name']] = $("#"+this.questions[i]['name']+"_n_t").val();
          }else if($("input[name='"+this.questions[i]['name']+"']:checked").val() != undefined){
            component_process[this.questions[i]['name']] = $("input[name='"+this.questions[i]['name']+"']:checked").val();
          }else if($("input[name='"+this.questions[i]['name']+"']:checked").val() == undefined){
            alert("There are unmarked questions, based on your changed selection. Please find them and select answers.")
            return
          }

        }
        if(message=="no_figure"){
          // if worker decided that no character exist, then store string that signify that no figure exists
          this.collected_data[this.current_marker] = "no_figure"
        }else{
          //else,
          if(valence==undefined || arousal==undefined || category==undefined || category==""){
            // if values are not filled make workers fill the values properly. (Escape)
            alert("Select values, or write proper reasoning to proceed.")
            return
          }else{
            // if values are filled, stor them
            var dict = {
              'valence' : valence,
              'arousal' : arousal,
              'category' : category,
              'minor_category': minor_category,
              'component_process' : component_process,
              //'motivational' : this.cur_motiv_exp,
            }
            this.collected_data[this.current_marker] = dict
          }
        }


      // reset input fields
      $("input[name='valence']").prop('checked', false)
      $("input[name='arousal']").prop('checked', false)

        $("input[name='ekman']").prop('checked', false)
        $("input[name='ekman_mul']").prop('checked', false)
        $("input[name='for_other']").val("")
        for(i in this.questions){
          $("input[name='"+this.questions[i]['name']+"']").prop('checked', false);
          $("#"+this.questions[i]['name']+"_n_t").val("")
        }

        //change the state to 'watching' state
        this.state='watching'
        this.state_string="Watching Video"
        this.tagging_phase = 0
        $('#replay_btn').css("visibility","hidden")
        //change marker to 'done status'
        $("#maxBar").css("width", "0%");
        $(".emotion_marker").removeClass("HiddenMarker")
        $("#stop_marker_"+this.current_marker).removeClass("currentMarker").addClass("doneMarker")
        // reset current marker variable
        this.current_marker = -1;
        // when all the necessary markers are done, enable submit function
        if(Object.keys(this.collected_data).length==Object.keys(prompt_time).length && vue_app.submittable==false){
          alert("Now you labeled character's emotion for all required moments. If you do not think revision is necessary, return with submit button below.")
          vue_app.submittable = true;
        }
        vue_app.current_action_add()
        // play the video
        this.playPromise = player.play()

    },
    get_q_range_for_index: function(index){
      var min=0;
      var max=this.question_show_num[0];

        for(var i=0; i<this.tagging_phase; i++){
          min = max;
          max = max + this.question_show_num[i+1];
        }

      return [min, max]
    },
    question_hidden: function(index){
      if(this.silent_checked[this.current_marker]!=undefined&&this.questions[index]['silent_related']!=undefined){
        return false
      }

      var min_max = this.get_q_range_for_index(index)
      var min = min_max[0]
      var max = min_max[1]

      if(this.tagging_phase<this.question_page){
      if(index>=min && index<max){
        return true;
      }else{
        return false;
      }}
      else{
        return false;
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
    expression_existence: function(){
      return (this.cur_motor_exp.length==0) && (this.cur_physio_exp.length==0)
    },
    tagging_phase_add: function(){
      //this.state_string="Labeling Step B"
      var min_max = this.get_q_range_for_index(this.tagging_phase)
      var pass = true;
      for(var i=min_max[0]; i<min_max[1]; i++){
        console.log($("input[name='"+this.questions[i]['name']+"']").prop('checked'))
        if($("input[name='"+this.questions[i]['name']+"']:checked").length==0){
          pass=false;
        }else{
          if($("input[name='"+this.questions[i]['name']+"']:checked").val()=="-1"){
            if($("#"+this.questions[i]['name']+"_n_t").val().length<5){
              alert("Write the reason for your 'Not sure / Lack information' option.")
              return;
            }
          }
        }
      }
      if(pass){
        this.tagging_phase++;
        if(this.tagging_phase==4){
          this.state_string = "Labeling Step B"
        }else if(this.tagging_phase==7){
          this.state_string = "Labeling Step C"
        }
      }else{
        alert("Please fill in all questions")
      }
    },
    tagging_phase_substract: function(){
      //this.state_string="Labeling Step A"
      this.tagging_phase--;
      if(this.tagging_phase==6){
        this.state_string = "Labeling Step B"
      }else if(this.tagging_phase==3){
        this.state_string = "Labeling Step A"
      }
    },
    tagging_step_A: function(){
      return (this.tagging_phase<4)&&(this.state=="tagging")
    },
    tagging_step_B: function(){
      return (this.tagging_phase<7) && (this.tagging_phase>=4) &&(this.state=="tagging")
    },
    jump_to_exact_frame: function(){

      player.currentTime(this.current_marker+this.micro_browser/10);
      this.micro_browser= (this.micro_browser+1)%10;
    },
    tagging_done_button_activated: function(){
      if(this.question_page == this.tagging_phase || this.collected_data[this.current_marker]!=undefined){
        return true;
      }else{
        return false;
      }
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
    }
  }
})

var maximal_time = 0;
var maximal_percentage;
var cur_time = 0;

var player;
// below is for setting up video functionalities
  //getting the video
/*var vjs_options = {
  controlBar: {
    volumePanel: {inline: false}
  },
}
document.getElementById('main_video').onloadedmetadata = function(){
//    load_markers()
}
player = videojs('main_video', vjs_options)

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
})*/
$(document).ready(function(){
  // below is for setting up video functionalities
    //getting the video
  document.getElementById('main_video').onloadedmetadata = function(){
  //    load_markers()
  }
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
})

// make div for signify how much a worker has seen, replay button, etc
$(".vjs-control-bar").append("<button id='replay_btn' class='vjs-control vjs-button' onclick='replay()'></button>")
$("#replay_btn").append("<i class='small material-icons' style='margin-top: 5px; font-size:20px;'>replay</i>")
$(".vjs-progress-holder").prepend("<div id='playedBar' class='cyan lighten-3'></div>");
$(".vjs-progress-holder").prepend("<div id='maxBar' style='float:right; height: 100%; background-color: black; width: 0%;'></div>");
//generate markers for prompt
  //generate the data structure for markers
var markers=[];

//load_markers()
// after rewatching
function after_replay(){
  player.pause()
  player.controls(true)
  vue_app.micro_browser = 0;
  vue_app.state = "tagging";
  vue_app.state_string="Labeling Step A"
  $('#replay_btn').css("visibility", "visible")
}

//recast data to the input field, for emotion labeling and reasoning
function recast_data(marker_time){
  if (vue_app.playPromise !== undefined) {
  vue_app.playPromise.then(_ => {
    player.pause();
    vue_app.playPromise = undefined
  })
  .catch(error => {
    player.pause();
    vue_app.playPromise = undefined
  });
}
  vue_app.state="tagging";
  vue_app.state_string="Labeling Step A"
  $('#replay_btn').css("visibility","hidden")
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
  $(".emotion_marker").addClass(function(){
      if(!$(this).hasClass("doneMarker")){
        return "HiddenMarker"
      }else{
        return "HiddenMarker" // TODO decide whether to make this return "" or "HiddenMarker"
      }
  })
  $("#stop_marker_"+marker_time).removeClass('doneMarker').removeClass("HiddenMarker").addClass('currentMarker')
    if(vue_app.collected_data[marker_time]!= 'no_figure'){
      posting_data(vue_app.collected_data, marker_time)
    }

  vue_app.current_action_revise()
}

function posting_data(dict, marker_time){
  var val_val = dict[marker_time]['valence']
  var aro_val = dict[marker_time]['arousal']
  var ekman_val = dict[marker_time]['category']
  var ekman_mul_val = dict[marker_time]['minor_category']
  var component_process = dict[marker_time]['component_process']
  $("input[name='valence'][value='"+val_val.toString()+"']").prop('checked', true)
  $("input[name='arousal'][value='"+aro_val.toString()+"']").prop('checked', true)
    if(emotion_category.indexOf(ekman_val)==-1){
      $("#other").prop('checked', true);
      $("#for_other").val(ekman_val)
    }else{
      $("#"+ekman_val).prop('checked', true);
    }
    for(ek_m_v in ekman_mul_val){
      console.log(ekman_mul_val[ek_m_v])
      if(emotion_category.indexOf(ekman_mul_val[ek_m_v])>=0){
        $("#"+ekman_mul_val[ek_m_v]+"_mul").prop('checked', true);
      }else{
        $("#other_mul").prop('checked', true);
        $("#for_other").val(ekman_mul_val[ek_m_v])
      }
    }
    for(cp in component_process){
      if(component_process[cp].length >4){
        $("#"+cp+"_n").prop('checked', true)
        $("#"+cp+"_n_t").val(component_process[cp])
      }else{
        $("#"+cp+"_"+component_process[cp]).prop('checked', true)
      }
    }


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
      if(vue_app.state=="watching" || vue_app.state=="tagging"){
        if($("[data-marker-key='"+marker['key']+"']").hasClass("doneMarker")){
          if(vue_app.state=="tagging"){
            vue_app.add_data();
          }
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

$("input[name='utterance_length']").on('click', function(){
  if($("input[name='utterance_length']:checked").val()=="1"){
    vue_app.silent_checked[vue_app.current_marker] = true
    $(".silent_not_sure").prop('checked', true)
    $(".silent_not_sure_r").val("silence")
  }else{
    vue_app.silent_checked[vue_app.current_marker] = undefined
    $(".silent_not_sure").prop('checked', false)
    $(".silent_not_sure_r").val("")
  }

})
