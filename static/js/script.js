$(document).ready(function() {
    $("#clock").countdown("2016/03/26", function(event) {
        $(this).text(event.strftime('%D days %H:%M:%S'));
    });


    $('.delete-list-btn').click(function(){
        var form = $(this).parent().siblings('.delete-form');
        $('.modal .btn-danger').click(function(){
            $.ajax({
                url: '/api/deletelist',
                data: form.serialize(),
                type: 'POST',
                success: function(response){
                    $('.confirm-modal').modal('toggle');
                    form.closest('.col-md-6').fadeOut('medium');
                },
                error: function(error){
                    console.log(error);
                }
            });
        });
    });

    $('.delete-btn').click(function(){
        var form = $(this).parent().siblings('.delete-form');
        $('.modal .btn-danger').click(function(){
            $.ajax({
                url: '/api/delete',
                data: form.serialize(),
                type: 'POST',
                success: function(response){
                    $('.confirm-modal').modal('toggle');
                    form.parent().fadeOut('medium');
                }
            });
        });
    });

    $('.new-btn').click(function(){
        var form = $(this).closest('form');
        if(form.find('input[name="item"]').val()){
            $.ajax({
                url: '/api/new',
                data: form.serialize(),
                type: 'POST',
                success: function(response){
                    console.log(response);
                    var item = `

                          <li class="list-group-item">
                              ${response.title}
                              <div class="btn-group pull-right" role="group" aria-label="...">
                                  <button type="button" class="btn btn-success btn-xs check-btn" aria-label="Left Align" data-toggle="tooltip" data-placement="top" title="Check">
                                      <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                                  </button>
                                  <button type="button" class="btn btn-danger btn-xs delete-btn" data-toggle="modal" data-target=".confirm-modal">
                                      <span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
                                  </button>
                              </div>
                              <form method="POST" action="/delete" class="delete-form">
                                  <input type="hidden" name="item-id" value="${response.id}"/>
                                  <input type="hidden" name="list-id" value="${response.list_id}">
                              </form>
                              <form method="POST" action="/check" class="check-form">
                                  <input type="hidden" name="item-id" value="${response.id}"/>
                                  <input type="hidden" name="list-id" value="${response.list_id}">
                                  <input type="hidden" name="check" value="true"/>
                              </form>
                          </li>

                                `;
                    form.closest('ul').prepend(item);
                    // form.closest('ul').append(response.html);
                }
            });
        }
        return false;
    });

    $().alert('close');
    $('[data-toggle="tooltip"]').tooltip();

    $('.check-btn').click(function(){
        button = $(this);
        $.ajax({
            url: '/api/check',
            data: $(this).parent().siblings('.check-form').serialize(),
            type: 'POST',
            success: function(response){
                button.toggleClass('btn-info btn-success check-btn uncheck-btn');
                button.parent().siblings('.check-form').find('input[name="check"]').val('true');
                button.closest('li').toggleClass('list-group-item-success strike-through');
            }
        });
    });

    $('.uncheck-btn').click(function(){
        button = $(this);
        $.ajax({
            url: '/api/check',
            data: $(this).parent().siblings('.check-form').serialize(),
            type: 'POST',
            success: function(response){
                button.toggleClass('btn-info btn-success check-btn uncheck-btn');
                button.parent().siblings('.check-form').find('input[name="check"]').val('false');
                button.closest('li').toggleClass('list-group-item-success strike-through');
            }
        });
    });


    // Keep Scroll position in web storage

    (function($) {

        /**
         * Store scroll position for and set it after reload
         *
         * @return {boolean} [loacalStorage is available]
         */
        $.fn.scrollPosReload = function() {
            if (localStorage) {
                var posReader = localStorage.posStorage;
                if (posReader) {
                    $(window).scrollTop(posReader);
                    localStorage.removeItem("posStorage");
                }
                $(this).click(function(e) {
                    localStorage.posStorage = $(window).scrollTop();
                });

                return true;
            }

            return false;
        };

        /* ================================================== */

        $(document).ready(function() {
            // Feel free to set it for any element who trigger the reload
            // $('select').scrollPosReaload();
            $(window).scroll().scrollPosReload();
        });

    }(jQuery));


});
