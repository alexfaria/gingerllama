$(document).ready(function() {

  $('#delete-username').on('input',function(e){
    username = $(this).parent().siblings('#hidden-username').val();
    button = $(this).parent().siblings(':button');
    if ($(this).val() == username){
     button.prop('disabled', false);
    }
    if ($(this).val() != username){
     button.prop('disabled', true);
    }

    });


    $("#clock").countdown("2016/09/04", function(event) {
        $(this).text(event.strftime('%D days %H:%M:%S'));
    });

});
