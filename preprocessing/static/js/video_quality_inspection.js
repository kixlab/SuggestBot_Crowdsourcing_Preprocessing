
var good_url, bad_url, instruction, good_example_text, bad_example_text;

if(criteria == "video_quality"){
  good_url = "https://github.com/athakur36/SuggestbotVideoRepo/blob/master/videos/good_video.mp4?raw=true"
  bad_url = "https://github.com/athakur36/SuggestbotVideoRepo/blob/master/videos/bad_picture_quality.mp4?raw=true"
}else if(criteria == "sound_quality"){
  good_url = "https://www.youtube.com/embed/qNYfM0ovwug"
  bad_url = "https://www.youtube.com/embed/qNYfM0ovwug"
}else if(criteria == "language"){
  good_url = "https://www.youtube.com/embed/per9Wz0N-QA"
  bad_url = "https://www.youtube.com/embed/per9Wz0N-QA"
}else if(criteria == "conversation"){
  good_url = "https://www.youtube.com/embed/JQcp3UWQOmM"
  bad_url = "https://www.youtube.com/embed/JQcp3UWQOmM"
}else if(criteria == "scene"){
  good_url = "https://www.youtube.com/embed/yAfAxmhWmcQ"
  bad_url = "https://www.youtube.com/embed/yAfAxmhWmcQ"
}


var vue_app = new Vue({
  el: "#vueapp",
  delimiters: ['[[', ']]'],
  data: {
    //whether the worker saw the tutorial
    //whether the worker is seeing the first page or the second page
    tuto_exp: false,
    tuto_first:false,
    tuto_second: false,
    //to render name of category
    example: criteria,
    //good and bad video example url
    good_url: good_url,
    bad_url: bad_url,
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
})
