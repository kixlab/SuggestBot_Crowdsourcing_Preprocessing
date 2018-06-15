var tuto_vue = new Vue({
  el: "#tutorial",
  delimiters: ['[[', ']]'],
  data: {
    cur_tuto: 0,
    max_tuto: max_tuto,
    tuto_array: Array.apply(null, Array(max_tuto+1)).map(function (_, i) {return i;}),
    tuto_done: false,
    loaded:true,
    tuto_img:[],
    tuto_text:[],
    on_load_use:true,
  },
  methods:{
    disabled_prev: function(){
      return (this.cur_tuto==0)||(!this.loaded && this.on_load_use);
    },
    disabled_next: function(){
      return (this.cur_tuto>=this.max_tuto)||(!this.loaded && this.on_load_use);
    },
    disabled_task: function(){
      return (!this.dismissible())||(!this.loaded && this.on_load_use);
    },
    dismissible: function(){
      if(this.cur_tuto>=this.max_tuto || this.tuto_done){
        return true
      }else{
        return false
      }
    },
    next_step: function(){
      if(this.cur_tuto<this.max_tuto){
        this.cur_tuto++;

        this.loaded = false;
      }
    },
    previous_step: function(){
      if(this.cur_tuto>0){
        this.cur_tuto--;
        this.loaded = false;
      }
    },
    tuto_close: function(message=false){
      if(this.tuto_done==false){
        this.tuto_done = true
        console.log(message)
        if(message){
          console.log('inhere')
          $(message).css('visibility', 'visible')
        }
      }
      this.cur_tuto=0

    },
    jump_to_page: function(message){
      this.cur_tuto = message
      this.loaded = false;
    }
  },
  updated: function(){
    //this.loaded = true;

  }
})

$(document).ready(function(){
  $(".modal").modal({
    dismissible: false,
    startingTop: '2.5%',
    endingTop: '2.5%',
  })
  $("#tutorial").modal('open')

  console.log(tuto_vue)
  if(document.getElementById('tuto_img')!=undefined){
    document.getElementById('tuto_img').onload = function(){
      tuto_vue.loaded = true;
    }
  }


  $(".tooltipped").tooltip({html: true, enterDelay: 50,});

})
