$(document).ready(function () {
    //tip
    tippy('.category-title > .title');

    //reesponsive menu
    $('#menu-trigger-btn').click(function () {
        $('.menu ul').slideToggle(500);
    });

    //responsive menu debug
    $(window).resize(function () {
        if ($(window).width() > 767) {
            $('.menu ul').removeAttr('style');
        }
    });

    
});
