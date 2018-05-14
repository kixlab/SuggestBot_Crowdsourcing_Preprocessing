function video_update_blinking_and_stop(player_id, target_second, param_to_true=undefined){
  // set video
  video = document.getElementById(player_id)
  video_clone = video.cloneNode(true);
  video.parentNode.replaceChild(video_clone, video)
  video.remove()

  video = document.getElementById(player_id)
  video.addEventListener('timeupdate', function(){
    if(video.currentTime> target_second && video.currentTime < target_second+1){
      $("#"+player_id).css("border", "solid 5px red")
    }else{
      $("#"+player_id).css("border", "solid 5px black")
    }
    if(video.currentTime > target_second+4){
      console.log("stopp")
      if(param_to_true != undefined){
        vue_app.nextable = true;
        if(vue_app.max_visited < vue_app.step){
          vue_app.max_visited = vue_app.step;
        }
      }
      video.pause()
    }

  })
  video.currentTime = target_second-5;
  return video
}
