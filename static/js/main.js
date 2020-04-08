$(document).ready(function(){
    'use strict';
    var GESTURE_NUMBER;
    var CARDIMAGE;
    var EYE_BLINK_COUNTER = eye_blink_count_generator();
    $("#count").empty();
    $("#count").append(EYE_BLINK_COUNTER);

    get_gesture_pose_image()
    
    // $('#imagemodal').on('show.bs.modal', function () {
    //   $('.modal .modal-body').css('overflow-y', 'auto'); 
    //   $('.modal .modal-body').css('max-height', $(window).height() * 0.5);
    // });

    // $('#imagemodal').on('show.bs.modal', function () {
    //   $('#imagemodal').css('height',$( window ).height()*0.2);
    // });

    $(".contact_nav").click(function() {
      $("html, body").animate({ scrollTop: $(document).height() }, "slow");   
    });

    $("#gesture_pass").click(function() {
      var myDiv = document.getElementById('live_face_section');
      scrollTo(document.body, myDiv.offsetTop-50, 100);   
    });


    /* globals MediaRecorder */
    const canvas = document.getElementById("cv");
    var img = document.getElementById("picture");
    const video = document.getElementById("gum");
    const mediaSource = new MediaSource();
    mediaSource.addEventListener('sourceopen', handleSourceOpen, false);
    let mediaRecorder;
    let recordedBlobs;
    let sourceBuffer;

    const errorMsgElement = document.querySelector('span#errorMsg');
    const recordedVideo = document.querySelector('video#recorded');
    const recordButton = document.querySelector('button#start'); //start on button click
    const stopButton = document.querySelector('button#screenshot'); //start on button click

    document.querySelector('button#start').addEventListener('click', async () => {
    
    $("#live_done_button_show").show()
   $('#picture').attr('src','');
   var video = document.getElementById("gum");
    var screenshot = document.getElementById("screenshot");
    console.log('video',video)
    $("#screenshot").show();
    // if ( video.paused ) {
    //     video.play();
    //     $("#screenshot").show();

    // } 
    // else {
    //     video.pause();
    //     video.load();
    //     $("#screenshot").hide();
    // }
    // width: 640, height: 480
      const constraints = {
        video: {
          width: 1280, height: 720
        }
      };
      console.log('Using media constraints:', constraints);
      await init(constraints);
      startRecording();
    //   *****************
    });


    document.querySelector('button#screenshot').addEventListener('click', async () => {
      $("#live_verify_button_show").show()
//      if (stopButton.textContent === 'ScreenShot') {
        stopRecording();
//      }

    });


    function handleSourceOpen(event) {
      console.log('MediaSource opened');
      sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8"');
      console.log('Source buffer: ', sourceBuffer);
    }

    function handleDataAvailable(event) {
      if (event.data && event.data.size > 0) {
        recordedBlobs.push(event.data);
      }
    }


recordedBlobs = [];

    function startRecording() {
//        var recorder = new window.MediaRecorder(stream);
      let options = {mimeType: 'video/webm;codecs=vp9'};
      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        console.error(`${options.mimeType} is not Supported`);
        errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
        options = {mimeType: 'video/webm;codecs=vp8'};
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
          console.error(`${options.mimeType} is not Supported`);
          errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
          options = {mimeType: 'video/webm'};
          if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            console.error(`${options.mimeType} is not Supported`);
            errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
            options = {mimeType: ''};
          }
        }
      }

      try {
        mediaRecorder = new MediaRecorder(window.stream, options);
      } catch (e) {
        console.error('Exception while creating MediaRecorder:', e);
        errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(e)}`;
        return;
      }

      console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
      mediaRecorder.onstop = (event) => {
        console.log('Recorder stopped: ', event);
      };
      mediaRecorder.ondataavailable = handleDataAvailable;
      mediaRecorder.start(); // collect 10ms of data
      console.log('MediaRecorder started', mediaRecorder);
    }

    function stopRecording() {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        img.src = canvas.toDataURL('img/png');
        img.style.display = 'none';
        video.pause()

      mediaRecorder.stop();
      stream.getTracks().forEach(function(track) {
        track.stop();
      });
      console.log('Recorded Blobs: ', recordedBlobs);
    }


    function handleSuccess(stream) {
      console.log('getUserMedia() got stream:', stream);
      window.stream = stream;

      let gumVideo = document.querySelector('video#gum');
      gumVideo.srcObject = stream;
      video.play();
    }

    async function init(constraints) {
      try {
        
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        // alert("stream created")
        console.log("STREAM " , stream)
        console.log("CONSTRAINTS " , constraints)
        handleSuccess(stream);
      } catch (e) {
        console.error('navigator.getUserMedia error:', e);
        errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
      }
    }





    function b64toBlob(dataURI) {

    var byteString = atob(dataURI.split(',')[1]);
        var ab = new ArrayBuffer(byteString.length);
        var ia = new Uint8Array(ab);

        for (var i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: 'image/jpeg' });
    }
    function pose_random_generator()
    {
      
      var maximum = 4;
      var minimum = 1;
      var randomnumber = Math.floor(Math.random() * (maximum - minimum + 1)) + minimum;
      GESTURE_NUMBER = randomnumber
      return randomnumber
    }

    function eye_blink_count_generator()
    {
    
      var maximum = 9;
      var minimum = 3;
      var eye_blink_number = Math.floor(Math.random() * (maximum - minimum + 1)) + minimum;
      EYE_BLINK_COUNTER = eye_blink_number
      return eye_blink_number
    }

    $("#gesture").on("click", function() {
      var pose_randomNumber = pose_random_generator();
      $('#imagepreview').attr('src', '/estatic/gestures/'+pose_randomNumber+'.jpeg'); 
      $('#imagemodal').modal('show'); 
   });




$("#test_button").on("click", function() {
  $('#name').val('');
  $('#fatherName').val('');
  $('#dob').val('');
  $('#cardNumber').val('');
  
  $('#formModel').modal('show'); 
});
$("#text_cancel").on("click", function() {
  $('#formModel').modal('hide'); 
});
var TEST_CARD;


$("#text_validate").on("click", function() {
  $('#formModel').modal('hide');
  $('#ocr_processid').show()
  
  let name = $('#name').val().toUpperCase();
  let fname = $('#fatherName').val().toUpperCase();
  let dob = $('#dob').val();
  let pan = $('#cardNumber').val().toUpperCase();
  let image = $('#form_image').val();
  console.log(name)
  console.log(fname)
  console.log(dob)
  console.log(pan)
  console.log(image)

  var formdata = new FormData();

  formdata.append("name",name)
  formdata.append("fname",fname)
  formdata.append("dob",dob)
  formdata.append("pan",pan)

  jQuery.ajax({
    url: '/eKYC/validate',
    type: "POST",
    data: formdata,
    processData: false,
    contentType: false,
    beforeSend: function() {
         $("#processid").addClass("fa-pulse");
         $('#output-img').empty();

    },
    success: function (result) {
      console.log(result.status);
      
      var ocr_details_json = result.details
      
      var ocr_name = ocr_details_json["Name"]
      var ocr_fname = ocr_details_json["Father Name"]
      var ocr_dob = ocr_details_json["Date of Birth"]
      var ocr_pan = ocr_details_json["PAN"]
      if(name != ocr_name){
        
        $('#name_wrong_tick_mark').show()
        $('#name_correct_tick_mark').hide()
        
      }
      else
      {
        $('#name_wrong_tick_mark').hide()
        $('#name_correct_tick_mark').show()
        
        
      }
      
      if(fname != ocr_fname){
        $('#fname_wrong_tick_mark').show()
        $('#fname_correct_tick_mark').hide()
       
      }
      else
      {
        $('#fname_wrong_tick_mark').hide()
        $('#fname_correct_tick_mark').show()
        
      }
      
      if(dob != ocr_dob){
        $('#dob_wrong_tick_mark').show()
        $('#bod_correct_tick_mark').hide()
        
      }
      else
      {
        $('#dob_wrong_tick_mark').hide()
        $('#dob_correct_tick_mark').show()
        
      }
      
      if(pan != ocr_pan){
        $('#pan_wrong_tick_mark').show()
        $('#pan_correct_tick_mark').hide()
        
      }
      else
      {
        $('#pan_wrong_tick_mark').hide()
        $('#pan_correct_tick_mark').show()
        
      }
      
      $('#ocr_cardNumber').val(pan)
      $('#ocr_fatherName').val(fname)
      $('#ocr_dob').val(dob)
      $('#ocr_name').val(name)
      $('#ocr_processid').hide()
    },
    complete: function () {
      
      $('#ocr_processid').hide()
    },
    fail: function(){
      $('#ocr_processid').hide()
    }
});


});


$("#verify_gesture").on("click", function() {
  $("#photo_processid").show()
  var liveImage = document.getElementById("photo_img").src;
  var formdata = new FormData();

  var blob = b64toBlob(liveImage);

  console.log("liveImage : ",blob)
  formdata.append("liveImage", blob);
  
  formdata.append("gesture",GESTURE_NUMBER)

  jQuery.ajax({
    url: '/eKYC/photo',
    type: "POST",
    data: formdata,
    processData: false,
    contentType: false,
    beforeSend: function() {
       

    },
    success: function (result) {
      let status= result.status
      // let eye_blink_status = result.eye_blink_status
      let gesture_status = result.gesture_status
      console.log(" status : ",result.status)
      // console.log(" eye_blink_status : ",result.eye_blink_status)
      console.log(" gesture_status : ",result.gesture_status)
      $("#photo_processid").hide()
      if(status == true &&  gesture_status == true)
      {
        $('#gesture_verify_success').modal('show');
        $("#start").attr("disabled", false);
        $("#screenshot").attr("disabled", false);
        $("#verify_live").attr("disabled", false);
      }
      else{
        $('#gesture_verify_failure').modal('show');
      }
    },
    complete: function () {
      
      $("#photo_processid").hide()
    },
    fail: function(){
      $("#photo_processid").hide()
    }
});

});


$("#verify_live").on("click", function() {
    $("#live_processid").show()
    var liveImage = document.getElementById("picture").src;
    var formdata = new FormData();

    var blob = b64toBlob(liveImage);

    console.log("liveImage : ",blob)
    formdata.append("liveImage", blob);
    var recorded = new Blob(recordedBlobs, {type: 'video/webm'});
    formdata.append("recodedVideo", recorded);
    // formdata.append("gesture",GESTURE_NUMBER)
    formdata.append("blinks",EYE_BLINK_COUNTER)
  
    jQuery.ajax({
      url: '/eKYC/live',
      type: "POST",
      data: formdata,
      processData: false,
      contentType: false,
      beforeSend: function() {
         

      },
      success: function (result) {
        let status= result.status
        let eye_blink_status = result.eye_blink_status
        // let gesture_status = result.gesture_status
        console.log(" status : ",result.status)
        console.log(" eye_blink_status : ",result.eye_blink_status)
        // console.log(" gesture_status : ",result.gesture_status)
        $("#live_processid").hide()
        if(status == true && eye_blink_status == true )
        {
          $('#face_verify_success').modal('show');
        }
        else{
          $('#face_verify_failure').modal('show');
        }
      },
      complete: function () {
        
        $("#live_processid").hide()
      },
      fail: function(){
        $("#live_processid").hide()
      }
  });

});

$("#success_page").on("click", function(obj) {
  location.href = "/eKYC/success";
});

document.querySelector('button#camera').addEventListener('click', async () => {
  // width: 640, height: 480
  // width: 1280, height: 720
// $("#camera").on("click", function(obj) {
  $('#box').show()
  $("#photo").show();
  let video_gesture = document.querySelector("#video_photo");
  let constraints_photo = {
    video_gesture: true,
    deviceId: { exact: 'video_photo' },
    video_gesture: {
      width: 1280, height: 720
    }
  };
  
  // await init(constraints_photo);
  let stream_photo = navigator.mediaDevices.getUserMedia({
    video: {
      deviceId: { exact: 'video_photo' },
      width: 1280,
      height:720
    },
    video: {
      width: 1280, height: 720
    }
  });
  // video_gesture.play();
  
  
  if(hasMedia()){
    stream_photo.then((stream) => {video_gesture.srcObject = stream,video_gesture.play()});
  }
  
});

function hasMedia(){
  return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}


$("#photo").on("click", function() {
  // let video_photo = document.querySelector("#video_photo");
  // let canvas_photo = document.getElementById("photo_canvas");
  // let img_photo = document.getElementById("photo_img");
  // canvas_photo.width = video_photo.videoWidth;
  // canvas_photo.height = video_photo.videoHeight;
  // canvas_photo.getContext('2d').drawImage(video_photo, 0, 0);
  // img_photo.src = canvas_photo.toDataURL('img/png');
  // img_photo.style.display = 'none';
  // // img_photo.style.display = 'show';
  // video_photo.pause()

  get_gesture_pose_image()

  
});

$("#gesture_btn_close").on("click", function() {
  $("#camera_button_show").show()
});
$("#camera").on("click", function() {
  $("#photo_button_show").show()
});
$("#photo").on("click", function() {
  $("#verify_button_show").show()
});
$("#gesture_failure_close_btn").on("click", function() {
  $("#photo_button_show").hide()
  $("#camera_button_show").hide()
  $("#verify_button_show").hide()
});

$("#live_failure_close_btn").on("click", function() {
  $("#live_done_button_show").hide()
  $("#live_verify_button_show").hide()
  
});

$("#logout").on("click", function() {
  location.href = "/eKYC/login";
})





})

function get_gesture_pose_image()
{
  let video_photo = document.querySelector("#video_photo");
  let canvas_photo = document.getElementById("photo_canvas");
  let img_photo = document.getElementById("photo_img");
  canvas_photo.width = video_photo.videoWidth;
  canvas_photo.height = video_photo.videoHeight;
  canvas_photo.getContext('2d').drawImage(video_photo, 0, 0);
  img_photo.src = canvas_photo.toDataURL('img/png');
  img_photo.style.display = 'none';
  // img_photo.style.display = 'show';
  video_photo.pause()
}
