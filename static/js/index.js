$(document).ready(function(){
  
    // $('#ocr_dob').DatePicker({
    //   flat: true,
    //   date: '2008-07-31',
    //   current: '2008-07-31',
    //   calendars: 1,
    //   starts: 1
    // });
    
    $("#ocr_dob").datepicker(
    {
      changeMonth: true,
      changeYear: true,
      yearRange: '1900:' + new Date().getFullYear().toString(),
      dateFormat: "dd/mm/yy",
      
    });
    
    $(".contact_nav").click(function() {
        $("html, body").animate({ scrollTop: $(document).height() }, "slow");   
    });
   

    $("#scoll_down").click(function() {
      var myDiv = document.getElementById('e-KYC_form');
      scrollTo(document.body, myDiv.offsetTop-50, 100);   
    });
    

    var imageLoader = document.getElementById('document');
    imageLoader.addEventListener('change', handleImage, false);
    var CARDIMAGE;
    function handleImage(e)
    {
        CARDIMAGE = event.target.files[0];
        console.log(CARDIMAGE)
    }

    var imageLoader_aadhar = document.getElementById('aadhar');
    imageLoader_aadhar.addEventListener('change', handleImage_aadhar, false);
    var CARDIMAGE_AADHAR;
    function handleImage_aadhar(e)
    {
      CARDIMAGE_AADHAR = event.target.files[0];
        console.log(CARDIMAGE_AADHAR)
    }

    
    
    $("#verify_details").on("click", function() {
      let name = $('#ocr_name').val().trim();
      let fname = $('#ocr_fatherName').val().trim();
      // let dob = $('#ocr_dob').val().trim();
      let pan = $('#ocr_cardNumber').val().trim();
      var file = $("#document").val();
      var aadhar_file = $("#aadhar").val();
      let selected_value = $("#document_type_select option:selected").val()


      // date=new Date(document.getElementById("ocr_dob").value);
      // dt=date.getDate();
      // mn=date.getMonth();
      // mn++;
      // yy=date.getFullYear();
      // dob=dt+"/"+mn+"/"+yy
      // dob = $("#ocr_dob").datepicker.parseDate( element.value );
      // $("ocr_dob").datepicker({ dateFormat: 'dd, mm, yy' });
      let dob = $("#ocr_dob").datepicker({dateFormat: 'dd/mm/yy'}).val();

      let panNumber_status = validatePAN(pan)
      let phoneNumber = $('#number').val().trim();
      let phoneNumber_status = validatePhone(phoneNumber)
      let email = $('#email').val().trim();
      let email_status = validateEmail(email)
      // var address = $("textarea#message").val();
      if(phoneNumber == "" )
      {
        phoneNumber_status = true
      }
      if(email == "" )
      {
        email_status = true
      }
      if (selected_value == 'pan')
       {
          if(aadhar_file == "")
          {
            $('#mandatory_details_check').modal('show');
          }
       }

      console.log("panNumber_status : ",panNumber_status)
      console.log("email_status : ",email_status)
      console.log("phoneNumber_status : ",phoneNumber_status)
      address_fileds = check_address_fileds()

       if(name == "" || fname == "" || dob == "" || pan == "" || file == "" || phoneNumber == "" || email == "" || address_fileds == false)
       {
        $('#mandatory_details_check').modal('show'); 
       }
       
       else if (phoneNumber_status == false)
       {
        $('#phone_number_validate').modal('show');
       }
       else if (email_status == false)
       {
        $('#email_validate').modal('show');
       }
       else if (panNumber_status == false)
       {
        $('#pan_number_validate').modal('show');
       }
       
       else{
        process_form_details()
       }
      
      
      });


      function process_form_details()
      {
        $('#ocr_processid').show()
        let name = $('#ocr_name').val().trim();
        let name_upper = name.toUpperCase()
        let fname = $('#ocr_fatherName').val().trim();
        let fname_upper = fname.toUpperCase();
        let dob = $("#ocr_dob").datepicker({dateFormat: 'dd/mm/yy'}).val();
        let pan = $('#ocr_cardNumber').val().trim();
        let pan_upper = pan.toUpperCase()
        let document_type_value = $("#document_type_select option:selected").val()

        // date=new Date(document.getElementById("ocr_dob").value);
        // dt=("0" + date.getDate()).slice(-2)
        // mn=("0" + (date.getMonth() + 1)).slice(-2);
        
        // yy=date.getFullYear();
        // dob=dt+"/"+mn+"/"+yy


        let mobile = $('#number').val().trim();
        let email = $('#email').val().trim();
        // let address = $("textarea#message").val().toUpperCase().trim();

        let house_number = $('#house_number').val().trim();
        let street_locality = $('#street_locality').val().trim();
        let vtc = $('#vtc').val().trim();
        let district = $('#district').val().trim();
        let state = $('#state').val().trim();
        let pincode = $('#pincode').val().trim();



        console.log(name_upper)
        console.log(fname_upper)
        console.log(dob)
        console.log(pan_upper)


      
        var formdata = new FormData();
      
        formdata.append("name",name_upper)
        formdata.append("fname",fname_upper)
        formdata.append("dob",dob)
        formdata.append("pan",pan_upper)
        formdata.append("document_type_value",document_type_value)
        formdata.append("cardImage", CARDIMAGE);
        formdata.append("aadhar", CARDIMAGE_AADHAR);
        formdata.append("mobile",mobile)
        formdata.append("email",email)
        formdata.append("house_number", house_number);
        formdata.append("street_locality", street_locality);
        formdata.append("vtc", vtc);
        formdata.append("district", district);
        formdata.append("state", state);
        formdata.append("pincode", pincode);
      
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
            var status = true
            // var ocr_details_json = result.details
            // var status = result.status
            // var address_status = result.address_status
            // var address_fileds_status = result.address_fileds_status
            // console.log(" address_fileds_status ",address_fileds_status)
            // console.log(" address_fileds_status ",address_fileds_status['house'])
            // console.log(" address_fileds_status ",address_fileds_status['state'])
            // var ocr_name = ocr_details_json["Name"]
            // ocr_name = ocr_name.trim()
            // var ocr_fname = ocr_details_json["Father Name"]
            // ocr_fname = ocr_fname.trim()
            // var ocr_dob = ocr_details_json["Date of Birth"]
            // ocr_dob = ocr_dob.trim()
            // var ocr_pan = ocr_details_json["Number"]
            // ocr_pan = ocr_pan.trim()
            
            // var address_status = result.address_status
            // console.log(ocr_name)
            // console.log(ocr_fname)
            // console.log(ocr_dob)
            // console.log(ocr_pan)

            // showing_address_fileds_status(address_fileds_status)
            // // if (address_status == true)
            // // {
            // //   $('#address_match_true').show()
            // //   $('#address_match_false').hide()
            // // }
            // // else
            // // {
            // //   $('#address_match_true').hide()
            // //   $('#address_match_false').show()

            // // }
            // if(name_upper != ocr_name){
              
            //   $('#name_wrong_tick_mark').show()
            //   $('#name_correct_tick_mark').hide()
              
            // }
            // else
            // {
            //   $('#name_wrong_tick_mark').hide()
            //   $('#name_correct_tick_mark').show()
              
              
            // }
            
            // if(fname_upper != ocr_fname){
            //   $('#fname_wrong_tick_mark').show()
            //   $('#fname_correct_tick_mark').hide()
             
            // }
            // else
            // {
            //   $('#fname_wrong_tick_mark').hide()
            //   $('#fname_correct_tick_mark').show()
              
            // }
            
            // if(dob != ocr_dob){
            //   $('#dob_correct_tick_mark').hide()
            //   $('#dob_wrong_tick_mark').show()
              
              
            // }
            // else
            // {
            //   $('#dob_wrong_tick_mark').hide()
            //   $('#dob_correct_tick_mark').show()
              
            // }
            
            // if(pan_upper != ocr_pan){
            //   $('#pan_wrong_tick_mark').show()
            //   $('#pan_correct_tick_mark').hide()
              
            // }
            // else
            // {
            //   $('#pan_wrong_tick_mark').hide()
            //   $('#pan_correct_tick_mark').show()
              
            // }
            
            // $('#ocr_cardNumber').val(pan)
            // $('#ocr_fatherName').val(fname)
            // $('#ocr_dob').val(dob)
            // $('#ocr_name').val(name)
            // $('#ocr_processid').hide()

            if(status == true)
            {
                $('#myModal_success').modal('show'); 
            }
            else
            {
                $('#myModal_failure').modal('show');
            }
            $("#details_matched").show()
            $("#details_not_matched").show()
          },
          complete: function () {
            
            $('#ocr_processid').hide()
          },
          fail: function(){
            $('#ocr_processid').hide()
          }
      });
      }

      
      $("#faceValidatePage").on("click", function() {
        location.href = "/eKYC/face";
      })

      $('select').on('change', function() {

        let selected_text = $("#document_type_select option:selected").text()
        let selected_value = $("#document_type_select option:selected").val()
        
        $("#documentType").empty();
        $("#documentType").append(selected_text);

        $("#primary_document").empty();
        $("#primary_document").append(selected_text+" Image*");
        
        if (selected_value == "pan")
        {
          $("#aadhar_upload_file").show()
        }
        else
        {
          $("#aadhar_upload_file").hide()
        }


      });

    function validatePAN(pan){ 
      // var regex = /[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}$/; 
      // return regex.test(pan);
      return true 
    }

    function validatePhone(number) {
      number = number.trim()
      var filter = /^((\+[1-9]{1,4}[ \-]*)|(\([0-9]{2,3}\)[ \-]*)|([0-9]{2,4})[ \-]*)*?[0-9]{3,4}?[ \-]*[0-9]{3,4}?$/;
      if (filter.test(number) && number.length == 10) {
          return true;
      }
      else {
          return false;
      }
    }
    function validateEmail(email) {
      var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
      return regex.test(email);
    }

    $("#logout").on("click", function() {
      location.href = "/eKYC/login";
    })

    function check_address_fileds()
    {

      let house_number = $('#house_number').val().trim();
      let street_locality = $('#street_locality').val().trim();
      let vtc = $('#vtc').val().trim();
      let district = $('#district').val().trim();
      let state = $('#state').val().trim();
      let pincode = $('#pincode').val().trim();
      if (house_number == "" || street_locality == "" || vtc == "" || district == "" || state == "" || pincode == "") 
      {
        return false;
      }
      else {
          return true;
      }
    }

    function showing_address_fileds_status(address_fileds_status)
    {
      if(address_fileds_status['house'] == true)
      {
        $('#house_number_wrong_tick_mark').hide()
        $('#house_number_correct_tick_mark').show()
      }
      else
      {
        $('#house_number_correct_tick_mark').hide()
        $('#house_number_wrong_tick_mark').show()
      }

      if(address_fileds_status['street_locality'] == true)
      {
        $('#street_locality_wrong_tick_mark').hide()
        $('#street_locality_correct_tick_mark').show()
      }
      else
      {
        $('#street_locality_correct_tick_mark').hide()
        $('#street_locality_wrong_tick_mark').show()
      }

      if(address_fileds_status['vtc'] == true)
      {
        $('#vtc_wrong_tick_mark').hide()
        $('#vtc_correct_tick_mark').show()
      }
      else
      {
        $('#vtc_correct_tick_mark').hide()
        $('#vtc_wrong_tick_mark').show()
      }

      if(address_fileds_status['dist'] == true)
      {
        $('#district_wrong_tick_mark').hide()
        $('#district_correct_tick_mark').show()
      }
      else
      {
        $('#district_correct_tick_mark').hide()
        $('#district_wrong_tick_mark').show()
      }

      if(address_fileds_status['state'] == true)
      {
        $('#state_wrong_tick_mark').hide()
        $('#state_correct_tick_mark').show()
      }
      else
      {
        $('#state_correct_tick_mark').hide()
        $('#state_wrong_tick_mark').show()
      }

      if(address_fileds_status['pc'] == true)
      {
        $('#pincode_wrong_tick_mark').hide()
        $('#pincode_correct_tick_mark').show()
      }
      else
      {
        $('#pincode_correct_tick_mark').hide()
        $('#pincode_wrong_tick_mark').show()
      }

      
    }


   

})