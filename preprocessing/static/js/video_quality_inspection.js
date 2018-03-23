//  This code loads the IFrame Player API code asynchronously.
      var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);



var good_url, bad_url, instruction_title, instruction, good_example_text, bad_example_text, good_example_title, bad_example_title;

var to_return = {
  'batch_id' : batch_id,
  'criteria' : criteria,
  'task_result' : {},
}

if(criteria == "video_quality"){
  instruction_title = "visual quality of"
  instruction = "you can recognize the behavior of characters with the visual of the video. For instance, if you think you can describe what characters are doing, like 'The character is walking' or 'The character is paying money', you can decide that the video is fair in the visual quality."
  good_example_text = "You can grasp character’s behavior, facial expression, and emotion from the visual of the video."
  bad_example_text = "It is hard to understand what is going on visually, and hard to capture facial expressions."
  good_example_title = "video with fine visual quality"
  bad_example_title = "video with bad visual quality"
  good_url = "/good_example.mp4"
  bad_url = "/bad_visual.mp4"
}else if(criteria == "sound_quality"){
  instruction_title = "audio quality of"
  instruction = "you can recognize utterances of characters with the audio of the video. For instance, if you think you can understand the intention or emotion of characters and can dictate majority of the conversation, you can decide that the video is fair in the audio quality."
  good_example_text = "You can grasp character’s utterance from the audio of the video, and there is no significant background noises such as music or chit-chats."
  bad_example_text = "It is hard to understand what is being said in the video."
  good_example_title = "video with fine audio quality"
  bad_example_title = "video with bad audio quality"
  good_url = "/good_example.mp4"
  bad_url = "/bad_audio.mp4"
}else if(criteria == "language"){
  instruction_title = "language of"
  instruction = "they are majorly composed of conversation in English."
  good_example_text = "Conversation is in English."
  bad_example_text = "Conversation is not in English."
  good_example_title = "video in English"
  bad_example_title = "video not in English"
  good_url = "/good_example.mp4"
  bad_url = "/bad_language.mp4"
}else if(criteria == "conversation"){
  instruction_title = "existence of conversation in"
  instruction = "they are majorly composed of conversational scenes between customers and employees."
  good_example_text = "A video is not monologue or lecture but majorly composed of conversation."
  bad_example_text = "A video is not in conversation, but in other forms like monologue or lecture."
  good_example_title = "conversation video"
  bad_example_title = "video without conversation"
  bad_url = "/bad_conversation.mp4"
  good_url = "/good_example.mp4"

}else if(criteria == "scene"){
  instruction_title = "the consistency of the flow in"
  instruction = "they are consistent videos, not with a compilation of multiple different videos."
  good_example_text = "The story or the flow of the video is consistent, even with angle or scene changes within the video. It is not a compilation of multiple unrelated videos."
  bad_example_text = "It is a concatenation of multiple unrelated videos, and you can spot inconsistency in the flow or the story. The characters and the context of the video might suddenly change. A compilation is one example of such a video."
  good_example_title = "video with a consistent flow"
  bad_example_title = "compilation video"
  good_url = "/good_example.mp4"
  bad_url = "/bad_scene.mp4"
}

console.log(instruction_title)
var vue_app = new Vue({
  el: "#vueapp",
  delimiters: ['[[', ']]'],
  data: {
    //whether the worker saw the tutorial
    //whether the worker is seeing the first page or the second page
    tuto_exp: false, // change below three later. They are for debugging purpose
    tuto_first:false,
    tuto_second: false,
    //to render name of category
    example: criteria,
    //good and bad video example url
    good_url: good_url,
    bad_url: bad_url,
    instruction_title : instruction_title,
    instruction: instruction,
    good_example_text: good_example_text,
    bad_example_text: bad_example_text,
    good_example_title: good_example_title,
    bad_example_title: bad_example_title,
    task_series: task_series,
    cur_task: 0,
    video_seen_second: Array.apply(null, Array(batch_number)).map(Number.prototype.valueOf,0),
    cur_video_seen_second: 0,
    required_seeing_second: 20000,
    was_playing:false,
    batch_number: batch_number,
    item_not_clicked: true,
    example_video_route: example_video_route,
    example_being_played: false,
    debug: debug,
  },
  methods:{
    play_example: function(message){
      document.getElementById(message).play();
      this.example_being_played = true;
    },
    tutorial_next: function(event){
      if(this.tuto_exp==false){
        this.tuto_exp = true;
        $("#modal_next").addClass("disabled")
        this.example_being_played=false;
      }else if(this.tuto_first==false){
        this.tuto_first = true;
        $("#modal_next").addClass("disabled")
        this.example_being_played=false;
      }else if(this.tuto_second==false){
        this.tuto_second = true;
        $(".modal").modal("close")
      }
    },
    next_task: function(event){
      this.was_playing=false;
      this.video_seen_second[this.cur_task]=this.cur_video_seen_second

      //store data
      proceed = store_data(this.task_series, this.cur_task)
      if(!proceed){
        return
      }
      this.cur_task++;
      this.cur_video_seen_second = this.video_seen_second[this.cur_task]
      //show different video
      player.cueVideoById({'videoId': task_series[this.cur_task], 'startSeconds':0, 'suggestedQuality':'large'})
      //enable prev task button
      $("#prev_task").removeClass("disabled")
      //recast data if previously added data exist
      recast_data(this.task_series, this.cur_task)
    },
    prev_task: function(event){
      store_data(this.task_series, this.cur_task)
      this.video_seen_second[this.cur_task]=this.cur_video_seen_second
      this.cur_task--;
      this.cur_video_seen_second = this.video_seen_second[this.cur_task]
      //show different video
      player.cueVideoById({'videoId': task_series[this.cur_task], 'startSeconds':0, 'suggestedQuality':'large'})
      //when it is beginning task
      if(this.cur_task == 0){
        $("#prev_task").addClass("disabled")
      }
      //recast data if previously added data exist
      recast_data(this.task_series, this.cur_task)
    },
    return_result: function(event){
      store_data(this.task_series, this.cur_task)
      //below for testing
      if(Object.keys(to_return['task_result']).length == 0){
        to_return['task_result']['dummy']='dummy'
      }
      $("#to_return").val(JSON.stringify(to_return))
    }

  },
  updated: function(){
    if(this.tuto_exp==true && this.tuto_first==false){
      $("#good_ex").on("ended", function(){
        vue_app.example_being_played=false;
        $("#modal_next").removeClass("disabled")
      })

    }else if(this.tuto_first==true && this.tuto_second==false){
      $("#bad_ex").on("ended", function(){
        vue_app.example_being_played=false;
        $("#modal_next").removeClass("disabled")
      })
    }
  }

})

var player;

function onYouTubeIframeAPIReady(){
  player = new YT.Player('player', {
    height: '270',
    width: '480',
    videoId: task_series[vue_app.cur_task],
    events:{
    }
  });
}

setInterval(timecount,10);

function timecount(){
  if(player){
    if(player.getPlayerState){
      if(player.getPlayerState()==1){
        if(vue_app.was_playing){
          vue_app.cur_video_seen_second += 10
        }else{
          vue_app.was_playing = true;
        }
      }else if(player.getPlayerState()==2 ||player.getPlayerState()==0){
        vue_app.was_playing = false;
      }
    }
  }

}


$(document).ready(function(){
  $(".modal").modal({
    dismissible: false,
  }).modal('open');

  $("input[name='"+criteria+"']").on("click", function(){
    vue_app.item_not_clicked = false;
  })
})

function store_data(tasks, task_id){
  var checked = $("input[name='"+criteria+"']:checked")
  if(checked.length==1){
    if (checked.attr("id").includes("yes")){
      to_return['task_result'][tasks[task_id]] = true;
    }else if(checked.attr("id").includes("no")){
      to_return['task_result'][tasks[task_id]] = false;
    }
    checked.prop("checked", false);
    console.log(to_return['task_result'])
    return true
  }
  else if(checked.length==0){
    return false
  }
}

function recast_data(tasks, task_id){
  if(tasks[task_id] in to_return['task_result']){
    if(to_return['task_result'][tasks[task_id]]){
      $("#"+criteria+"_yes").prop("checked", true);
    }else{
      $("#"+criteria+"_no").prop("checked", true);
    }
    vue_app.item_not_clicked = false;
  }else{
    vue_app.item_not_clicked = true;
  }
}
