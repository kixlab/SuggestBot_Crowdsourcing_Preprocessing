var vue_app = new Vue({
  el: "#vueapp",
  delimiters: ['[[', ']]'],
  data: {
    //to render name of category
    example: 'video quality',
    //good and bad video example url
    good_url: "",
    bad_url: "",
  },
  methods:{
    example_modal_show: function(event){
      var ex = event.target.parentNode.parentNode.id
      this.example = ex.replace("_", " ");
      if (ex=="video_quality"){
        $("#good_ex").attr("src",  "https://www.youtube.com/embed/RPzf_4dcL28")
        $("#bad_ex").attr("src",  "https://www.youtube.com/embed/RPzf_4dcL28")
      }else if (ex=="sound_quality"){
        $("#good_ex").attr("src",  "https://www.youtube.com/embed/qNYfM0ovwug")
        $("#bad_ex").attr("src",  "https://www.youtube.com/embed/qNYfM0ovwug")
      }else if (ex=="language"){
        $("#good_ex").attr("src",  "https://www.youtube.com/embed/per9Wz0N-QA")
        $("#bad_ex").attr("src",  "https://www.youtube.com/embed/per9Wz0N-QA")
      }else if (ex=="conversation"){
        $("#good_ex").attr("src",  "https://www.youtube.com/embed/JQcp3UWQOmM")
        $("#bad_ex").attr("src",  "https://www.youtube.com/embed/JQcp3UWQOmM")
      }else if (ex=="scene"){
        $("#good_ex").attr("src",  "https://www.youtube.com/embed/yAfAxmhWmcQ")
        $("#bad_ex").attr("src",  "https://www.youtube.com/embed/yAfAxmhWmcQ")
      }
    },
    off_example_video: function(event){
      $("#good_ex").attr("src",  "https://www.youtube.com/embed/")
      $("#bad_ex").attr("src",  "https://www.youtube.com/embed/")
    }
  }

})

$(document).ready(function(){
  $(".modal").modal();
})
