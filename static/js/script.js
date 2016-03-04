$(document).ready(function() {
  $("#clock")
    .countdown("2016/03/26", function(event) {
      $(this).text(
      event.strftime('%D days %H:%M:%S')
    );
  });
  $('.delete-btn').click(function(ev){
    var form = $(this).parent().siblings('.delete-form');
    $('.btn-danger').click(function(){
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


  // var cval = Cookies.get('scroll');
  //
  // if (cval !== undefined){
  //   $(document).scrollTop(cval);
  // }
  //
  // $('button :not(.modal-footer > .btn-danger)').on('click', function(){
  //   Cookie.set('scroll', $(document).scrollTop());
  // });
  //


});
