$(document).ready(function() {
    $("#clock").countdown("2016/03/26", function(event) {
        $(this).text(event.strftime('%D days %H:%M:%S'));
    });

    $('.delete-list-btn').click(function(ev){
        var form = $(this).parent().siblings('.delete-form');
        $('.modal .btn-danger').click(function(){
            form.submit();
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
