/*var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;

function onYouTubeIframeAPIReady(){
  player = new YT.Player('player', {
    height: '270',
    width: '480',
    videoId: url_id,
    events:{
    }
  });
  player.loadVideoById(url_id, 0, 'medium');
}*/
var vjs_options = {
  controlBar: {
    volumePanel: {inline: false}
  },
}


//player.src("https://firebasestorage.googleapis.com/v0/b/suggestbot-preprocessing.appspot.com/o/A%20Man%20Like%20You%20%20%20%20A%20Short%20Film%20from%20Harry%E2%80%99s.mp4?alt=media&token=8f79cbc2-ca80-498e-a262")
var vue_app = new Vue({
  el: "#vue_app",
  delimiters: ['[[', ']]'],
  data:{
    figure_time_data: [],//[[[10,20],[40,70]],[[12, 22],[30,40]]],
    state: 'not_adding',
    figure_on_work: 0,
    cur_figure: undefined,
    cur_time_range: undefined,
    cur_possible_add_limit_max: undefined,
    cur_possible_add_limit_min: undefined,
    fig_image_source: [],
  },
  methods:{
    add_figure: function(){
      // get the frame
      player.pause()
      var player_jq = $("#main_video").get(0);
      var canvas = document.getElementById("canvas");
      canvas.width = player_jq.videoWidth *0.5*0.75;
      canvas.height = player_jq.videoHeight*0.5*0.75;
      canvas.getContext('2d').drawImage(player_jq, 0,0,canvas.width, canvas.height);
      var img = document.createElement("img");
      img.src = canvas.toDataURL('image/png');
      $("#modal_img_cont").empty().prepend(img);
      $("#modal1").modal('open')

      //this.figure_time_data.push([])
    },
    add_figure2: function(){
      var fig_num = this.figure_time_data.length
      this.figure_time_data.push([])
      vue_app.$forceUpdate();
      var player_jq = $("#main_video").get(0);
      var canvas = document.getElementById("canvas");
      canvas.width = $("#bounding_box").width()*8/3//player_jq.videoWidth *0.5*0.75;
      canvas.height = $("#bounding_box").height()*8/3//player_jq.videoHeight*0.5*0.75;
      var l_offset = ($("#bounding_box").offset().left - $("#modal_img").offset().left)*8/3
      var t_offset = ($("#bounding_box").offset().top - $("#modal_img").offset().top)*8/3
      canvas.getContext('2d').drawImage(player_jq, l_offset,t_offset,canvas.width, canvas.height,0,0,canvas.width, canvas.height);
      this.fig_image_source.push(canvas.toDataURL('image/png'))
      //var img = document.createElement("img");
      //img.src = canvas.toDataURL('image/png');
      //img.style.height = "30px";
      //this.cur_figure_img = img;
      //this.cur_figure_img_num = fig_num
    },
    delete_figure: function(fig_num){
      console.log(fig_num)
      this.fig_image_source.splice(fig_num, 1)
      this.figure_time_data.splice(fig_num, 1)
      if(this.figure_on_work == this.figure_time_data.length && this.figure_time_data.length!=0){
        this.figure_on_work -= 1
      }
    },
    add_time: function(fig_num){
      if(this.state=="not_adding"){
        this.state = "adding"
        this.cur_figure = fig_num
        player.seekable = false;

        this.cur_time_range = this.figure_time_data[fig_num].length
        this.cur_possible_add_limit_max = player.duration;
        this.cur_possible_add_limit_min = player.currentTime;
        //find range of playable times
        for(i in this.figure_time_data[fig_num]){
          if(this.cur_possible_add_limit_max>this.figure_time_data[fig_num][i][0] && this.figure_time_data[fig_num][i][0]>player.currentTime){
            this.cur_possible_add_limit_max = this.figure_time_data[fig_num][i][0]
          }
        }
        this.figure_time_data[fig_num].push([])
        this.figure_time_data[fig_num][this.cur_time_range].push(player.currentTime)
        this.figure_time_data[fig_num][this.cur_time_range].push(player.currentTime)

      }else if(this.state=="adding"){
        this.cur_figure = undefined
        this.cur_time_range = undefined
        this.cur_possible_add_limit_max = undefined
        this.state = "not_adding"
        player.seekable = true;
      }
    },
    delete_time: function(fig_num, time_range_num){
      console.log("tool-")
      this.state="not_adding"
      this.cur_possible_add_limit_max=undefined
      this.cur_possible_add_limit_min=undefined
      this.cur_figure = undefined
      this.cur_time_range = undefined
      this.figure_time_data[fig_num].splice(time_range_num, 1)
    },
    revise: function(fig_num, time_range_num){
      if(this.state=="not_adding"){
        if(this.figure_time_data[fig_num][time_range_num]==undefined){
          return
        }
        player.currentTime = this.figure_time_data[fig_num][time_range_num][1]
        player.pause()
        this.state = "adding"
        this.cur_figure = fig_num
        player.seekable = false;

        this.cur_time_range = time_range_num
        this.cur_possible_add_limit_max = player.duration;
        this.cur_possible_add_limit_min = this.figure_time_data[fig_num][time_range_num][0];
        //find range of playable times
        for(i in this.figure_time_data[fig_num]){
          if(this.cur_possible_add_limit_max>this.figure_time_data[fig_num][i][0] && this.figure_time_data[fig_num][i][0]>player.cur_possible_add_limit_min){
            this.cur_possible_add_limit_max = this.figure_time_data[fig_num][i][0]
          }
        }

      }
    },
    return_left: function(item){
      return (800 * item[0]/player.duration).toString() + "px";
    },
    return_right: function(item){
      var width = (800 * (item[1]-item[0])/player.duration).toString()
      if(width<1){
        width = 1
      }
      return width.toString()+ "px";
    },
    time_block_color:function(fig_num, time_range_num){
      if(this.cur_figure == fig_num && this.cur_time_range == time_range_num){
        return "green"
      }else{
        return "orange"
      }
    },
    return_icon: function(param){
      if(param == 'not_adding'){
        return "add"
      }else{
        return "pause"
      }
    },
    figure_disabler: function(index){
      console.log(index==this.cur_figure)
      if(this.state=="not_adding"){
        for(i in this.figure_time_data[index]){
          if(player.currentTime>=this.figure_time_data[index][i][0] && player.currentTime<=this.figure_time_data[index][i][1]){
            return true;
          }
        }
        return false
      }else{
        return !(this.cur_figure==index)
      }
    },
    work_on_next_fig: function(){
      if(this.figure_time_data.length != 0 && this.state !="adding"){
        this.figure_on_work = (this.figure_on_work+1)%this.figure_time_data.length
      }
    },
    work_on_prev_fig: function(){
      if(this.figure_time_data.length != 0  && this.state !="adding"){
        this.figure_on_work = (this.figure_on_work-1+this.figure_time_data.length)%this.figure_time_data.length
      }
    },
    working_on_figure_color: function(index){
      if(index == this.figure_on_work){
        return "white"
      }else{
        return "#cccccc"
      }
    },
    submit: function(){
      dict={
        'figure_images': this.fig_image_source,
        'figure_time_data': this.figure_time_data,
      }
      $("#return_json").val(JSON.stringify(dict))
    }
  },
})
var bar_clicked = false
$("#bar_container").on("mousedown", function(e){
  var relX = (e.pageX - $(this).offset().left)/($(this).width());
  //player.currentTime = player.duration * relX
  //bar_clicked = true
  //console.log(relX);
}).on("mousemove", function(e){
  if(bar_clicked){
    var relX = (e.pageX - $(this).offset().left)/($(this).width());
    //player.currentTime = player.duration * relX
  }
}).on("mouseup", function(e){
  //bar_clicked = false
})
var player
var dragging_object = undefined
$(document).ready(function(){
  $(".modal").modal()
  player = document.getElementById('main_video')
  player.ontimeupdate = function(){
    $("#time_indicator").css('left', (player.currentTime/player.duration* 800).toString()+"px")
    if(vue_app.cur_time_range!=undefined && vue_app.cur_figure!=undefined){
      if(vue_app.cur_possible_add_limit_max <player.currentTime || player.currentTime<vue_app.cur_possible_add_limit_min){
        console.log("need to stop")
        player.pause()
        return;
      }
      vue_app.figure_time_data[vue_app.cur_figure][vue_app.cur_time_range][1] = player.currentTime
    }
    vue_app.$forceUpdate();
    console.log("update time")
  }

  $("body").keydown(function(event){
    if(event.which == 32){
      if(player.paused){
        player.play()
      }else{
        player.pause()
      }
    }
    if(event.which == 90){
      vue_app.add_figure();
    }
    if(event.which == 40){
      vue_app.work_on_next_fig()
    }
    if(event.which== 38){
      vue_app.work_on_prev_fig()
    }
    if(event.which == 88){
      if(vue_app.state=="not_adding"){
        for(i in vue_app.figure_time_data[vue_app.figure_on_work]){
          if(player.currentTime>=vue_app.figure_time_data[vue_app.figure_on_work][i][0] && player.currentTime<=vue_app.figure_time_data[vue_app.figure_on_work][i][1]){
            return;
          }
        }
      }
      vue_app.add_time(vue_app.figure_on_work)
    }

    if($("#browse_interval").val()==""){
      return
    }
    console.log("being_pressed")
    if(event.which == 39){
      console.log("right")
      player.currentTime = player.currentTime + parseFloat($("#browse_interval").val())
    }else if(event.which == 37){
      player.currentTime = player.currentTime - parseFloat($("#browse_interval").val())
    }
  })

  $(".handle").on("mousedown", function(){
    if(dragging_object==undefined){
      dragging_object = $(this)
    }
  })
  $("#modal_img").on("mousemove", function(e){
    if(dragging_object!=undefined){
      console.log("hey")
      var new_posX = (e.pageX - $(this).offset().left)-7
      var new_posY = (e.pageY - $(this).offset().top)-7
      dragging_object.css("left", new_posX.toString()+"px")
      dragging_object.css("top", new_posY.toString()+"px")
      var other_object
      if(dragging_object.attr("id")=="bbox_handle_1"){
        other_object = $("#bbox_handle_2")
      }else{
        other_object = $("#bbox_handle_1")
      }
      // redraw the box
      var x1 = new_posX+7
      var x2 = other_object.offset().left-$(this).offset().left+7
      var y1 = new_posY+7
      var y2 = other_object.offset().top-$(this).offset().top+7
      var new_left, new_width, new_top, new_height;
      if(x1>x2){
        new_left = x2;
        new_width = x1-x2;
      }else{
        new_left = x1;
        new_width = x2-x1;
      }
      if(y1>y2){
        new_top = y2
        new_height = y1-y2
      }else{
        new_top = y1
        new_height = y2-y1
      }
      $("#bounding_box").css("left", new_left.toString()+"px")
        .css("top", new_top.toString()+"px")
        .css("width", new_width.toString()+"px")
        .css("height", new_height.toString()+"px")

      console.log(x1, x2)
    }
  }).on("mouseup", function(e){
    if(dragging_object!=undefined){
      dragging_object = undefined
    }
  })
})
