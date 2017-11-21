$(document).ready(function () {
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

    //admin special information button 
    $('body').on('click', '.file-admin-information-btn', function () {
        $(this).parent().find('.file-admin-information').slideToggle("fast");
    });
});
