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
      if(param_to_true == 'vue_app'){
        vue_app.nextable = true;
        if(vue_app.max_visited < vue_app.step){
          vue_app.max_visited = vue_app.step;
        }
      }else if(param_to_true == 'vue_exa_modal'){
        vue_exa_modal.nextable = true;
        if(vue_exa_modal.max_visited < vue_exa_modal.cur_ex){
          vue_exa_modal.max_visited = vue_exa_modal.cur_ex;
        }
      }
      video.pause()
    }

  })
  video.currentTime = target_second-5;
  return video
}
