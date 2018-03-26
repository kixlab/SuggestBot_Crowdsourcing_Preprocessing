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
var max_num_nametag = 9;


// give character name for each group to distinguish different groups
var character_name = ['Not Sure Which Person', 'Not a Person', 'Pikachu', 'Eevee', 'Mew', 'Squirtle', 'Raichu', 'Snorlax', 'Ditto'];
// nametag name
var namecolor = ['gray', 'gray', 'pink', 'green', 'blue', 'brown', 'red', 'skyblue', 'yellow'];
// the grouping result will be saved below
var grouping_array = [];
var temp_grouping_array = [];
var min_unselected = [];

// actual numaber of face images loaded
var actual_num_img_loaded = 0;
// current name tag id. that the worker is working on
var cur_name = 0;
// current task id. updated until hitting batch_number
var cur_task = 0;
// total number of names created so far. updated until no image left to select
var num_name = 0;
// flag for nametag onclick
var flag_nametag = undefined;

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

  // create onclick function for each face image
  for (var i=0; i<actual_num_img_loaded; i++){
    var img_id = "face" + (i+1);
    document.getElementById(img_id).onclick = function() {
      var selected_img = this.id;
      selected_img = selected_img.replace(/^face/, '');
      if (flag_nametag != undefined){
        if (grouping_array[cur_name][selected_img-1] == false) {
          grouping_array[cur_name][selected_img-1] = true;
          console.log("grouping_array[cur_name]", cur_name, grouping_array[cur_name]);
          this.style.border = "10px solid yellow";
        }
        else if (grouping_array[cur_name][selected_img-1] == true) {
          grouping_array[cur_name][selected_img-1] = false;
          this.style.border = "10px solid white";
        }
        for (var i=0; i<num_name+1; i++){
          if (i!=cur_name){
            if (grouping_array[i][selected_img-1] == true) {
              grouping_array[i][selected_img-1] = false;
              if (i == cur_name){
                this.style.border = "10px solid white";
              }
            }
          }
        }
      }
      else {
        if (grouping_array[num_name][selected_img-1] == false) {
          grouping_array[num_name][selected_img-1] = true;
          console.log("grouping_array[num_name]", num_name, grouping_array[num_name]);
          this.style.border = "10px solid yellow";
        }
        else if (grouping_array[num_name][selected_img-1] == true) {
          grouping_array[num_name][selected_img-1] = false;
          this.style.border = "10px solid white";
        }
      }
    };
    // create onclick function for each face image [end]
  }
})

window.onload = function() {
  // create the first group array
  for (var i=0; i<actual_num_img_loaded; i++){
    temp_grouping_array[i] = false;
  }

  // display NOT SURE WHICH PERSON and NOT A PERSON button
  grouping_array[cur_name] = temp_grouping_array.slice(0);
  create_nametag();
  cur_name++;
  num_name++;
  grouping_array[cur_name] = temp_grouping_array.slice(0);
  min_unselected = temp_grouping_array.slice(0);
  // the first unselected image is highlighted
  highlight_min_unselected();
  create_nametag();
  cur_name++;
  num_name++;
  grouping_array[cur_name] = temp_grouping_array.slice(0);

  // check the first faceimage as selected
  grouping_array[2][0] = true;
  console.log("grouping_array[2]", grouping_array[2]);
  document.getElementById("face1").style.border = "10px solid yellow";
}



// functions ///////////////////////////////////////////////////////////////////
function give_name(){
  if (num_name < max_num_nametag){

    // get number of images that are finished being grouped
    get_num_grouped_images();

    // apply opacity to all images that are finished being grouped
    apply_opacity();

    // create a name Tags
    create_nametag();

    num_name++;
    cur_name++;

    // create another group array
    grouping_array[num_name] = temp_grouping_array.slice(0);
    min_unselected = temp_grouping_array.slice(0);

    // the first unselected image is highlighted
    highlight_min_unselected();
  }
  else {
    alert("sorry, you reached the maximum number of name tags that can be generated is reached.");
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





// create a name Tags
function create_nametag(){
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
  // add onclick button to the name tags
  nametag.onclick = function() {
    if (flag_nametag == undefined){
      var selected_nametag = this.id;
      cur_name = selected_nametag.replace(/^nametag/, '');
      cur_name--;

      // disable other buttons
      document.getElementById('give_name').disabled = true;
      document.getElementById('next_task').disabled = true;
      for (var i=0; i<num_name; i++){
        if (i != cur_name){
          var nametag_id = "nametag" + (i+1);
          document.getElementById(nametag_id).disabled = true;
        }
      }
      for (var i=0; i<actual_num_img_loaded; i++){
        var img_id = "face" + (i+1);
        document.getElementById(img_id).style.opacity = "1";
        document.getElementById(img_id).style.pointerEvents = "auto";
        document.getElementById(img_id).style.border = "10px solid white";
        if (grouping_array[cur_name][i] == true){
          document.getElementById(img_id).style.border = "10px solid yellow";
        }
      }
      flag_nametag = cur_name;
    }
    else {
      document.getElementById('give_name').disabled = false;
      for (var i=0; i<num_name; i++){
        if (i != cur_name){
          var nametag_id = "nametag" + (i+1);
          document.getElementById(nametag_id).disabled = false;
        }
      }
      // get number of images that are finished being grouped
      get_num_grouped_images();
      // apply opacity to all images that are finished being grouped
      apply_opacity();
      // the first unselected image is highlighted
      highlight_min_unselected();

      flag_nametag = undefined;
      cur_name = num_name;
    }
  };
  // add onclick button to the name tags [end]
}


// the first unselected image is highlighted
function highlight_min_unselected(){
  // the first unselected image is highlighted
  for (var i=0; i<actual_num_img_loaded; i++){
    for (var j=0; j<num_name; j++){
      min_unselected[i] =  min_unselected[i] + grouping_array[j][i];
    }
  }
  min_unselected_idx = actual_num_img_loaded;
  for (var i=0; i<actual_num_img_loaded; i++){
    if (min_unselected[i] == false || min_unselected[i] == 0){
      min_unselected_idx = i;
      break;
    }
  }
  // ....but only when there are images left
  if (min_unselected_idx!=actual_num_img_loaded){
    var img_id = "face" + (min_unselected_idx+1);
    grouping_array[num_name][min_unselected_idx] = true;
    console.log("grouping_array[num_name], num_name", grouping_array[num_name], num_name)
    document.getElementById(img_id).style.border = "10px solid yellow";
  }
  min_unselected = temp_grouping_array.slice(0);
}

// get number of images that are finished being grouped
function get_num_grouped_images(){
  var num_grouped_images = 0;
  for (var i=0; i<num_name+1; i++){
    for (var j=0; j<actual_num_img_loaded; j++){
      if (grouping_array[i][j] == true){
        num_grouped_images++;
      }
    }
  }
  // if there is no unselected image, enable NEXT button
  if (num_grouped_images == actual_num_img_loaded){
    document.getElementById('next_task').disabled = false;
    document.getElementById('give_name').disabled = true;
  }
}

// apply opacity to all images that are finished being grouped
function apply_opacity(){
  if (flag_nametag == undefined){
    var temp_num_name = num_name + 1;
  }
  else {
    var temp_num_name = num_name;
  }
  for (var i=0; i<temp_num_name; i++){
    for (var j=0; j<actual_num_img_loaded; j++){
      if (grouping_array[i][j] == true){
        var img_id = "face" + (j+1);
        document.getElementById(img_id).style.opacity = "0.2";
        document.getElementById(img_id).style.border = "10px solid white";
        document.getElementById(img_id).style.pointerEvents = "none";
      }
    }
  }
}
