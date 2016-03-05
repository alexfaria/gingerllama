$(document).ready(function() {
    $("#clock").countdown("2016/03/26", function(event) {
        $(this).text(event.strftime('%D days %H:%M:%S'));
    });

    $('.delete-btn').click(function(ev){
        // GetScroll();
        var form = $(this).parent().siblings('.delete-form');
        $('.modal .btn-danger').click(function(){
            form.submit();
        });
    });

    $('.check-btn').click(function(){
        // GetScroll();
        $(this).parent().siblings('.check-form').submit();
    });
    $('.uncheck-btn').click(function(){
        // GetScroll();
        $(this).parent().siblings('.check-form').submit();
    });


    $().alert('close');
    $('[data-toggle="tooltip"]').tooltip();

    // Keep Scroll position in web storage

    ;
    (function($) {

        /**
         * Store scroll position for and set it after reload
         *
         * @return {boolean} [loacalStorage is available]
         */
        $.fn.scrollPosReload = function() {
            if (localStorage) {
                var posReader = localStorage["posStorage"];
                if (posReader) {
                    $(window).scrollTop(posReader);
                    localStorage.removeItem("posStorage");
                }
                $(this).click(function(e) {
                    localStorage["posStorage"] = $(window).scrollTop();
                });

                return true;
            }

            return false;
        }

        /* ================================================== */

        $(document).ready(function() {
            // Feel free to set it for any element who trigger the reload
            // $('select').scrollPosReaload();
            $(window).scroll().scrollPosReload();
        });

    }(jQuery));


});
