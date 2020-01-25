localFileVideoPlayer();
document.getElementById("snap").addEventListener("click",start);
document.getElementById("snap").disabled = true;

var video=document.getElementById('video');
var canvas=document.getElementById('canvas');

var w,h,ratio,int=0;
var img_arr=[];
var seg_arr=[];
var tp_arr=[];
var w_arr=[];
var i=0;
var start=1;
var kill=0;
var pause=0;

var fps=10;

var cap_time=30;
var play_time=2500/fps;
 //snap.onClick(start);
function init(){
  img_arr=[];
  seg_arr=[];
  tp_arr=[];
  w_arr=[];
  i=0;
  start=1;
  kill=0;
  pause=0;
  clear_w();
  document.getElementById("snap").disabled = true;
  document.getElementById("snap").innerHTML='start';
  Webcam.reset();
}

function localFileVideoPlayer() {
  'use strict'
  console.log("loaded");
  document.getElementById("hide").style.display="none";
  document.getElementById("pbar").style.visibility = "hidden";
  var URL = window.URL || window.webkitURL
  var displayMessage = function(message, isError) {
    var element = document.querySelector('#message')
    element.innerHTML = message
    element.className = isError ? 'error' : 'info'
  }
  var playSelectedFile = function(event) {
    var file = this.files[0]
    var type = file.type
    var videoNode = document.querySelector('video')
    var canPlay = videoNode.canPlayType(type)
    if (canPlay === '') canPlay = 'no'
    var message = 'Can play type "' + type + '": ' + canPlay
    var isError = canPlay === 'no'
    displayMessage(message, isError)
    if (isError) {
      return
    }

    var fileURL = URL.createObjectURL(file)
    videoNode.src = fileURL
  }
  var inputNode = document.querySelector('input')
  inputNode.addEventListener('change', playSelectedFile, false)
}

  //add loadedmetadata which will helps to identify video attributes

video.addEventListener('loadedmetadata', function() {
  if(int!=0){
    console.log(int);
    clearInterval(int)
  }



  console.log("loading");
  init();
  ratio = video.videoWidth/video.videoHeight;
  w = video.videoWidth-100;
  h = parseInt(w/ratio,10);
  canvas.width = w;
  canvas.height = h;
  document.getElementById("video").playbackRate =5;
  document.getElementById("snap").disabled = false;
  document.getElementById("snap").innerHTML='start';
}, false);
  

function start() {
  if(start==2) {
  console.log("display");
  start=3;
  document.getElementById("snap").innerHTML='pause';
  int=setInterval(disp,play_time);
  return;
  }

  if(start==0){
    kill=1;
    return;
  }

  if(start==3){
    pause=1;
    return;
  }

  if(start==10){
    start=11;
    document.getElementById("snap").innerHTML='stop camera';
    snapshot();
    return;
  }

  if(start==11){
    init();
    return;
  }
  
  document.getElementById("pbar").style.visibility = "visible";
  document.getElementById("snap").innerHTML='cancel';
  start=0;
  video.play();
  
  console.log("start");
  int=setInterval(snap,cap_time);
}

function snap() {
  console.log("snapping")
  if(video.ended){
    clearInterval(int);
    console.log("segmenting");
    console.log(img_arr.length);
    seg();
    return;
  }

  if(kill){
    clearInterval(int);
    prog(0);
    init();
    document.getElementById("snap").innerHTML='start';
   document.getElementById("pbar").style.visibility = "hidden";
    
    return;
  }

  canvas.getContext('2d').drawImage(video, 0, 0,w,h);
  img=canvas.toDataURL();
  img_arr.push(img);
  console.log(0);
}

 

function seg() {
  if(i==img_arr.length){
    i=0;
    start=2;
    document.getElementById("pbar").style.visibility = "hidden";
    document.getElementById("snap").innerHTML='play';
    prog(0);
    return;
  }

  if(kill){
    prog(0);
    init();
    document.getElementById("snap").innerHTML='start';
    document.getElementById("pbar").style.visibility = "hidden";
    
    return;
  }
  
  var data={
    'img':img_arr[i]
   };
   url='capture'
   $.post(url,data,function(v,status){
    console.log(i)
    prog(i)
   seg_arr.push(v.img);
   tp_arr.push(v.traffic);
   w_arr.push(v.weather);
   i=i+1;
   seg();
  });

}

 //snap.onClick(start);
 

function disp() {
  if(i==img_arr.length){
    i=0;
    
   // document.getElementById("snap").innerHTML='play';
    return;
  }

  if(pause==1){
    clearInterval(int);
    start=2;
    pause=0;
     document.getElementById("snap").innerHTML='play';
  }

 clear_w();

  console.log(i); 
  document.getElementById("img1").setAttribute("src",img_arr[i]);
  document.getElementById("img2").setAttribute("src","data:image/png;base64,"+seg_arr[i]);
  document.getElementById("img3").setAttribute("src","data:image/png;base64,"+tp_arr[i]);
  document.getElementById(w_arr[i]).style.opacity="1"
  document.getElementById(w_arr[i]).style.color="red"

  i=i+1;
}


function prog(val){
  var ptg=100*val/img_arr.length;
  document.getElementById("prg").style.width=ptg+"%";
}

document.getElementById("cam").addEventListener("click",cam_start);
var prev=0;

function cam_start(){
  init();
  start=10;
  document.getElementById("snap").disabled = false;
  document.getElementById("snap").innerHTML='start camera';
  Webcam.set({
  width: 512,
  height: 512,
  image_format: 'png',
  jpeg_quality: 90
 });
Webcam.attach( '#my_camera' );
}

function snapshot(){
  var d = new Date();
  console.log(d.getTime()-prev);
  prev=d.getTime();
  if(start!=11) {clear_w();return;}
  var bi;
  Webcam.snap( function(data_uri) {
    bi=data_uri;
  const url="capture";
  const data={
    img : bi
  };
  $.post(url,data,function(v,status){
   cam_display(bi,v.img,v.traffic,v.weather);
   snapshot();
  });
} );
}

  function cam_display(img,seg,tp,wt){
  document.getElementById("img1").setAttribute("src",img);
  document.getElementById("img2").setAttribute("src","data:image/png;base64,"+seg);
  document.getElementById("img3").setAttribute("src","data:image/png;base64,"+tp);
  clear_w();
  document.getElementById(wt).style.opacity="1"
  document.getElementById(wt).style.color="red"
  }

function clear_w(){
  document.getElementById("sunny").style.opacity="0.4"
  document.getElementById("sunny").style.color="black"
  document.getElementById("rainy").style.opacity="0.4"
  document.getElementById("rainy").style.color="black"
  document.getElementById("cloudy").style.opacity="0.4"
  document.getElementById("cloudy").style.color="black"
}