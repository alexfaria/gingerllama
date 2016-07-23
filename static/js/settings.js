$(document).ready(function() {

  $('#delete-username').on('input',function(e){
    var username = $(this).parent().siblings('#hidden-username').val();
    var button = $(this).parent().siblings(':button');
    if ($(this).val() == username){
      button.prop('disabled', false);
    }
    if ($(this).val() != username){
      button.prop('disabled', true);
    }
  });

  $('.change-password-btn').on('click', function(e){
    var form = $(this).siblings('form');
    $.ajax({
      url: '/api/changepassword',
      data: form.serialize(),
      type: 'POST',
      cache: false,
      success: function(response){
        if(response != null){
          if('error' in response){
            // str = format('<div class="alert alert-danger" role="alert">{0}</div>', [response.error]);
            form.parent().append(response.error);
            console.log(response.error);
          }
          else if('success' in response){
            console.log(response.success);
          }
        }
      },
      error: function(error){
        console.log(error);
      }
    });
  });


  function format(source, params) {
    $.each(params,function (i, n) {
      source = source.replace(new RegExp("\\{" + i + "\\}", "g"), n);
    })
    return source;
  }

  $("#clock").countdown("2016/09/04", function(event) {
    $(this).text(event.strftime('%D days %H:%M:%S'));
  });

});
