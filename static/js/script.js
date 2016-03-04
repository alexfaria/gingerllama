$(document).ready(function() {
  $("#clock").countdown("2016/03/26", function(event) {
      $(this).text(event.strftime('%D days %H:%M:%S'));
  });

  $('.delete-btn').click(function(ev){
    var form = $(this).parent().siblings('.delete-form');
    $('.modal .btn-danger').click(function(){
      form.submit();
    });
  });

  $('.check-btn').click(function(){
    $(this).parent().siblings('.check-form').submit();
  });
  $('.uncheck-btn').click(function(){
    $(this).parent().siblings('.check-form').submit();
  });


  $().alert('close');
  $('[data-toggle="tooltip"]').tooltip();

});
