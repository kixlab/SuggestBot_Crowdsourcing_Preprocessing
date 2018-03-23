var tuto_vue = new Vue({
  el: "#tutorial",
  delimiters: ['[[', ']]'],
  data: {
    cur_tuto: 0,
    max_tuto: max_tuto,
    tuto_done: false,
  },
  methods:{
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
      }
    },
    previous_step: function(){
      if(this.cur_tuto>0){
        this.cur_tuto--;
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
    }
  }
})

$(document).ready(function(){
  $(".modal").modal({
    dismissible: false,
    startingTop: '2.5%',
    endingTop: '2.5%',
  })
  $("#tutorial").modal('open')
  console.log($("#tutorial").css("top"))
})
