$(document).ready(function(){

    $(document).ready(function(){
        $("#login_btn").on("click", function() {
        login_check()
        })
    });

    $("#logIn").on("click", function() {
        login_check();
    });
    
    function login_check()
    {
      $("#login_process").show()
      console.log('***************************************')
      let username = $('#user').val().trim();
      let password = $('#password').val().trim();
      var formdata = new FormData();
      formdata.append("username",username)
      formdata.append("password",password)
      console.log(username)
      console.log(password)
      jQuery.ajax({
        url: '/eKYC/login_check',
        type: "POST",
        data: formdata,
        processData: false,
        contentType: false,
        beforeSend: function() {
              $("#processid").addClass("fa-pulse");
              $('#output-img').empty();
    
        },
        success: function (result) {
          $("#login_process").hide()
          console.log(result.status);
          let status = result.status
          if(status == true)
          {
              $('#myModal_login_success').modal('show'); 
              
          }
          else
          {
              $('#myModal_login_fail').modal('show');
          }
        },
        complete: function () {
          $("#login_process").hide()
        },
        fail: function(){
          $("#login_process").hide()
          $('#myModal_login_fail').modal('show');
        }
      });
                        
        
    }

    
    $("#login_success").on("click", function() {
        location.href = "/eKYC/index";
    });


})