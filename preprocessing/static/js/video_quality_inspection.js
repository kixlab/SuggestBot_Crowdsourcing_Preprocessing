
var good_url, bad_url, instruction, good_example_text, bad_example_text;

var to_return = {
  'batch_id' : batch_id,
  'criteria' : criteria,
  'task_result' : {},
}

if(criteria == "video_quality"){
  good_url = "https://github.com/athakur36/SuggestbotVideoRepo/blob/master/videos/good_video.mp4?raw=true"
  bad_url = "https://github.com/athakur36/SuggestbotVideoRepo/blob/master/videos/bad_picture_quality.mp4?raw=true"
}else if(criteria == "sound_quality"){
  good_url = "https://github.com/athakur36/SuggestbotVideoRepo/blob/master/videos/good_video.mp4?raw=true"
  bad_url = "https://www.youtube.com/embed/qNYfM0ovwug"
}else if(criteria == "language"){
  good_url = "https://github.com/athakur36/SuggestbotVideoRepo/blob/master/videos/good_video.mp4?raw=true"
  bad_url = "https://www.youtube.com/embed/per9Wz0N-QA"
}else if(criteria == "conversation"){
  good_url = "https://github.com/athakur36/SuggestbotVideoRepo/blob/master/videos/good_video.mp4?raw=true"
  bad_url = "https://www.youtube.com/embed/JQcp3UWQOmM"
}else if(criteria == "scene"){
  good_url = "https://github.com/athakur36/SuggestbotVideoRepo/blob/master/videos/good_video.mp4?raw=true"
  bad_url = "https://www.youtube.com/embed/yAfAxmhWmcQ"
}


var vue_app = new Vue({
  el: "#vueapp",
  delimiters: ['[[', ']]'],
  data: {
    //whether the worker saw the tutorial
    //whether the worker is seeing the first page or the second page
    tuto_exp: true,//false, // change below three later. They are for debugging purpose
    tuto_first:true,//false,
    tuto_second: true,//false,
    //to render name of category
    example: criteria,
    //good and bad video example url
    good_url: good_url,
    bad_url: bad_url,
    task_series: task_series,
    cur_task: 0,
    batch_number: batch_number,
    item_not_clicked: true,
  },
  methods:{
    tutorial_next: function(event){
      if(this.tuto_exp==false){
        this.tuto_exp = true;
        $("#modal_next").addClass("disabled")
      }else if(this.tuto_first==false){
        this.tuto_first = true;
        $("#modal_next").addClass("disabled")
      }else if(this.tuto_second==false){
        this.tuto_second = true;
        $(".modal").modal("close")
      }
    },
    next_task: function(event){
      //store data
      proceed = store_data(this.task_series, this.cur_task)
      if(!proceed){
        return
      }
      this.cur_task++;
      //enable prev task button
      $("#prev_task").removeClass("disabled")
      //recast data if previously added data exist
      recast_data(this.task_series, this.cur_task)
    },
    prev_task: function(event){
      store_data(this.task_series, this.cur_task)
      this.cur_task--;
      //when it is beginning task
      if(this.cur_task == 0){
        $("#prev_task").addClass("disabled")
      }
      //recast data if previously added data exist
      recast_data(this.task_series, this.cur_task)
    },
    return_result: function(event){
      store_data(this.task_series, this.cur_task)
      $("#to_return").val(JSON.stringify(to_return))
    }

  },
  updated: function(){
    if(this.tuto_exp==true && this.tuto_first==false){
      $("#good_ex").on("ended", function(){
        $("#modal_next").removeClass("disabled")
      })

    }else if(this.tuto_first==true && this.tuto_second==false){
      $("#bad_ex").on("ended", function(){
        $("#modal_next").removeClass("disabled")
      })
    }
  }

})

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
