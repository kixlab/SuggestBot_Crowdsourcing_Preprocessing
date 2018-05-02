
var stop_padding = 5;
var replay_padding = 3;
var video_url;
var times=[];
var emotion_category =[
  'fearful', 'angry', 'sad', 'disgusted', 'happy', 'surprised', 'frustrated', 'depressed', 'excited', 'neutral'
]
var motor_expression_dict={
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
}

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
    step: step,
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
    cur_motor_exp: [],
    cur_physio_exp: [],
    cur_cog_motiv_exp: "",
    state_string: 'Video Watching'
    //cur_motiv_exp: "",
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
        var minor_category = []
        var other_check=false;
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
        var reasoning = $("#reasoning").val()
        if(message=="no_figure"){
          // if worker decided that no character exist, then store string that signify that no figure exists
          this.collected_data[this.current_marker] = "no_figure"
        }else{
          //else,
          if(valence==undefined || arousal==undefined || category==undefined || reasoning.length<8 || category==""){
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
              'reasoning' : reasoning,
              'motor' : this.cur_motor_exp,
              'physio' : this.cur_physio_exp,
              'cog_motiv' : this.cur_cog_motiv_exp,
              //'motivational' : this.cur_motiv_exp,
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
        $("input[name='ekman_mul']").prop('checked', false)
        $("input[name='for_other']").val("")
        $("#reasoning").val("")
      }else if(this.step=='sanity_check'){
        $(".emotion_word_check").removeClass('emotion_word_check_highlighted')
        $("#current_reasoning").text("")
        $("input[name='check']").prop('checked', false)
      }
        //for component process
      $("input[name='motor']").prop('checked', false)
      $("input[name='physio']").prop('checked', false)
      $("#cog_motiv").val("")
      //$("#motivational").val("")



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
        if(Object.keys(this.collected_data).length==Object.keys(prompt_time).length){
          alert("Now you labeled character's emotion for all required moments. If you do not think revision is necessary, return with submit button below.")
          vue_app.submittable = true;
        }
        vue_app.current_action_add()
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
      //post component analysis results
      this.cur_motor_exp =[]

      $("input[name='motor']:checked").map(function(_, e){
        vue_app.cur_motor_exp.push($(e).val())
      })
      this.cur_physio_exp = []
      $("input[name='physio']:checked").map(function(_, e){
        vue_app.cur_physio_exp.push($(e).val())
      })
      this.cur_cog_motiv_exp = $("#cog_motiv").val()
      //this.cur_motiv_exp = $("#motivational").val()

      if(this.cur_cog_motiv_exp.length <8){
        alert('Please write your analysis about the event and the character.')
        return;
      }
      $("#motor_display").empty()
      $("#physiological_display").empty()
      $("#cog_motiv_display").empty()
      //$("#motivational_display").empty()
      for(i in this.cur_motor_exp){
        if(i%3==0){
          $("#motor_display").append("<tr id='motor_row_"+i.toString()+"'></tr>")
          $("#motor_row_"+i.toString()).append("<td style='font-size: 12px'>"+motor_expression_dict[this.cur_motor_exp[i]]+"</td>")
        }else{
          $("#motor_row_"+(parseInt(i/3)*3).toString()).append("<td style='font-size: 12px'>"+motor_expression_dict[this.cur_motor_exp[i]]+"</td>")
        }
      }
      for(i in this.cur_physio_exp){
        if(i%3==0){
          $("#physiological_display").append("<tr id='physio_row_"+i.toString()+"'></tr>")
          $("#physio_row_"+i.toString()).append("<td style='font-size: 12px'>"+physio_expression_dict[this.cur_physio_exp[i]]+"</td>")
        }else{
          $("#physio_row_"+(parseInt(i/3)*3).toString()).append("<td style='font-size: 12px'>"+physio_expression_dict[this.cur_physio_exp[i]]+"</td>")
        }
      }
      $("#cog_motiv_display").text(this.cur_cog_motiv_exp)
      //$("#motivational_display").text(this.cur_motiv_exp)
      this.state_string="Labeling Step B"
      this.tagging_phase++;
    },
    tagging_phase_substract: function(){
      this.state_string="Labeling Step A"
      this.tagging_phase--;

    },
    tagging_step_A: function(){
      return (this.tagging_phase==0)&&(this.state=="tagging")
    },
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
document.getElementById('main_video').onloadedmetadata = function(){
    load_markers()
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


// make div for signify how much a worker has seen, replay button, etc
$(".vjs-control-bar").append("<button id='replay_btn' class='vjs-control vjs-button' onclick='replay()'></button>")
$("#replay_btn").append("<i class='small material-icons' style='margin-top: 5px; font-size:20px;'>replay</i>")
$(".vjs-progress-holder").prepend("<div id='playedBar' class='cyan lighten-3'></div>");
$(".vjs-progress-holder").prepend("<div id='maxBar' style='float:right; height: 100%; background-color: black; width: 0%;'></div>");
//generate markers for prompt
  //generate the data structure for markers
var markers=[];


// after rewatching
function after_replay(){
  if(vue_app.step=="sanity_check"){
    posting_data(label_to_check, vue_app.current_marker)
  }
  player.pause()
  player.controls(true)
  vue_app.state = "tagging";
  vue_app.state_string="Labeling Step A"
  $('#replay_btn').css("visibility", "visible")
}

//recast data to the input field, for emotion labeling and reasoning
function recast_data(marker_time){
  player.pause()
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
  $(".emotion_marker").addClass("HiddenMarker")
  $("#stop_marker_"+marker_time).removeClass('doneMarker').removeClass("HiddenMarker").addClass('currentMarker')
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
  vue_app.current_action_revise()

}

function posting_data(dict, marker_time){
  var val_val = dict[marker_time]['valence']
  var aro_val = dict[marker_time]['arousal']
  var ekman_val = dict[marker_time]['category']
  var ekman_mul_val = dict[marker_time]['minor_category']
  var reasoning_val = dict[marker_time]['reasoning']
  var motor_exp = dict[marker_time]['motor']
  var physio_exp = dict[marker_time]['physio']
  //var motiv_exp = dict[marker_time]['motivational']
  var cog_motiv_exp = dict[marker_time]['cog_motiv']

  $("input[name='valence'][value='"+val_val.toString()+"']").prop('checked', true)
  $("input[name='arousal'][value='"+aro_val.toString()+"']").prop('checked', true)
  if(vue_app.step=="label_and_reason"){
    if(emotion_category.indexOf(ekman_val)==-1){
      $("#other").prop('checked', true);
      $("#for_other").val(ekman_val)
    }else{
      $("#"+ekman_val).prop('checked', true);
    }
    $("#reasoning").val(reasoning_val)
    for(ek_m_v in ekman_mul_val){
      console.log(ekman_mul_val[ek_m_v])
      if(emotion_category.indexOf(ekman_mul_val[ek_m_v])>=0){
        $("#"+ekman_mul_val[ek_m_v]+"_mul").prop('checked', true);
      }else{
        $("#other_mul").prop('checked', true);
        $("#for_other").val(ekman_mul_val[ek_m_v])
      }
    }

    for(i in motor_exp){
      $("#"+motor_exp[i]).prop('checked', true);
    }
    for(i in physio_exp){
      $("#"+physio_exp[i]).prop('checked', true);
    }
    $("#cog_motiv").val(cog_motiv_exp)
    //$("#motivational").val(motiv_exp)
  }else if(vue_app.step=="sanity_check"){
    $("#"+ekman_val+"_check").addClass("emotion_word_check_highlighted")
    $("#current_reasoning").text(reasoning_val)

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
    console.log(t)
    console.log(player)
    console.log(player.duration())
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

function exclusive_checkbox(checkboxes){
  for(var i=0; i<checkboxes.length; i++){
    $("#"+checkboxes[i]).on('click', function(){
      if($(this).prop('checked')){
        console.log(checkboxes)
        for(var j=0; j<checkboxes.length; j++){
          console.log($(this))
          console.log($("#"+checkboxes[j]))
          if($(this).attr('id')!=checkboxes[j]){
            console.log("in here")
            $("#"+checkboxes[j]).prop('checked', false)
          }
        }
      }
    })
  }
}

exclusive_checkbox(['mouth_opening', 'mouth_closing'])
exclusive_checkbox(['eyes_opening', 'eyes_closing'])
exclusive_checkbox(['volume_increasing', 'volume_decreasing'])
exclusive_checkbox(['moving_towards', 'withdrawing', 'against'])
exclusive_checkbox(['silence', 'short_utterance', 'long_utterance'])
$("a").on('mouseover', function(){
  $(this).css("color", "#d50000")
}).on('mouseout', function(){
  $(this).css("color","")
})
