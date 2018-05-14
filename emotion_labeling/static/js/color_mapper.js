function mapAColor(p){
            rComponent = 0;
            gComponent = 0;
            bComponent = 0;

            pressureVal = Math.round(p*511);
            if (pressureVal < 128){
                rComponent = 127;
                gComponent = pressureVal +127;
                bComponent = 255;
            } else if (pressureVal < 256) {
                rComponent = 127;
                gComponent = 255;
                bComponent = (255 - pressureVal) + 128;
            } else if (pressureVal < 384) {
                rComponent = (pressureVal - 256)+127;
                gComponent = 255;
                bComponent = 127;
            } else if (pressureVal < 512) {
                rComponent = 255;
                gComponent = (511 - pressureVal) + 128;
                bComponent = 0;
            }

            var s = "rgba(" + rComponent + "," + gComponent + "," + bComponent + ", 127)";
            return s;
        }

function color_mapper_gradient_color(canvas_id){
  var canvas = document.getElementById(canvas_id)
  var ctx = canvas.getContext("2d")

  var grd = ctx.createLinearGradient(0,0,0,canvas.height)
  grd.addColorStop(0, mapAColor(1))
  grd.addColorStop(1/4, mapAColor(3/4))
  grd.addColorStop(1/2, mapAColor(1/2))
  grd.addColorStop(3/4, mapAColor(1/4))
  grd.addColorStop(1, mapAColor(0))
  ctx.fillStyle = grd;
  ctx.fillRect(0,0,canvas.width/3, canvas.height)
  ctx.fillStyle= "black"
  for(var i=0; i<10; i++){
    ctx.fillText((1-i*0.1).toFixed(1), canvas.width/3, i*canvas.height/10+10);
  }
  ctx.fillText(0, canvas.width/3, canvas.height);
}
