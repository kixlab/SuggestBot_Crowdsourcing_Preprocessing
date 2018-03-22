//  This code loads the IFrame Player API code asynchronously. /////////////////
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


// directory of the face images
var directory = "/static/face_images/";
// max number of face images to be loaded
var max_num_img_loaded = 20;
//max number of name tag that can be created
var max_num_nametag = 7;


// give character name for each group to distinguish different groups
var character_name = ['Pikachu', 'Eevee', 'Mew', 'Squirtle', 'Raichu', 'Snorlax', 'Ditto', 'Not Sure Which Person', 'Not a Person'];
// nametag name
var namecolor = ['pink', 'green', 'blue', 'brown', 'red', 'skyblue', 'yellow', 'gray', 'gray'];
// the grouping result will be saved below
var grouping_array = [[]];
// marked all grouped images
var grouped_images = [];
// actual numaber of face images loaded
var actual_num_img_loaded = 0;
// current name tag id. that the worker is working on
var cur_name = 0;
// current task id. updated until hitting batch_number
var cur_task = 0;
// total number of names created so far. updated until no image left to select
var num_name = 0;

var to_return = {
  'batch_id' : batch_id,
  'task_result' : {},
}

// vue app starts from here ////////////////////////////////////////////////////
var vue_app_video = new Vue({
  el: "#vueapp-video",
  delimiters: ['[[', ']]'],
  data: {
    url: "eKwAib6LosM"
  },
})

// execute when document is loaded /////////////////////////////////////////////
$(document).ready(function(){

  // read all image files from the pointed directory
  for (var i=1; i<max_num_img_loaded; i++){
    actual_num_img_loaded++;
    url = directory + "" + i + ".png"; // pointed directory
    var img = new Image();
    img.onerror = function(){
      this.remove();
      actual_num_img_loaded--; // actual num of image loaded
    };
    img.src = url;
    img.id = "face" + i;
    $('#face-images').append(img);
  }

  // create a
  for (var i=0; i<actual_num_img_loaded; i++){
    grouping_array[cur_name][i] = false;
    grouped_images[i] = false;
  }

  // create onclick function for each face image
  for (var i=0; i<actual_num_img_loaded; i++){
    var img_id = "face" + (i+1);
    document.getElementById(img_id).onclick = function() {
      var selected_img = this.id;
      selected_img = selected_img.replace(/^face/, '');
      if (grouping_array[cur_name][selected_img-1] == false) {
        grouping_array[cur_name][selected_img-1] = true;
        this.style.border = "10px solid yellow";
      }
      else if (grouping_array[cur_name][selected_img-1] == true) {
        grouping_array[cur_name][selected_img-1] = false;
        this.style.border = "10px solid white";
      }
    };
  }

  // check the first faceimage as selected
  grouping_array[0][0] = true;
  document.getElementById("face1").style.border = "10px solid yellow";

})



// functions ///////////////////////////////////////////////////////////////////
function give_name(){
  if (num_name < max_num_nametag){
    //check/updated list of images that are finished being grouped
    for (i=0; i<num_name; i++){
      for (j=0; j<actual_num_img_loaded; j++){
        if (grouping_array[i][j] == true){
          grouped_images[j] = true;
        }
        else {
          grouped_images[j] = false;
        }
      }
    }
    // apply opacity to all images that are finished being grouped
    for (i=0; i<actual_num_img_loaded; i++){
      var img_id = "face" + (i+1);
      document.getElementById(img_id)
    }

    // the first unselected image is highlighted

    // create a name Tags
    var nametag = document.createElement("button");
    nametag.classList.add(namecolor[num_name]);
    nametag.classList.add("darken-1");
    nametag.classList.add("btn");
    nametag.id = "nametag" + (num_name+1);
    nametag.style.marginBottom = "10px";
    var t = document.createTextNode(character_name[num_name]);
    nametag.appendChild(t);
    var location = document.getElementById("addnametag");
    var br = document.createElement("br");
    location.appendChild(nametag);
    location.appendChild(br);

    // if there is no unselected image, enable NEXT button

    num_name++;
  }
  else {
    alert("sorry, maximum number of name tags that can be generated is reached.");
  }
}

function next_task(event){
  this.cur_task++;
  //v-if="cur_task<batch_number-1"

  //store_data
  // refer to video quality
}
function return_result(event){
  this.cur_task++;
}
