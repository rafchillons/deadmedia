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

    $('body').on('click', '.file-delete-btn', function () {
        $(this).css('cursor', 'default').css('text-decoration', 'none').css('color', 'red');
        $(this).text("Deleted");
        Img = $(this).parent().parent().parent().parent().parent().find('.image')
        id = linkImg.attr('id');
        img = $("#" + id).find('img');

        jQuery.getJSON("video/" + id + "/delete/");

        linkImg.css("background-image", "url(/assets/img/deleted.png)");
        linkImg.attr("onclick", " ");
        linkImg.css('cursor', 'default');
        linkImg.css('opacity', '0.7');
    });

    //file short info slide
    $(document).on({
        mouseenter: function () {
            $(this).find('.file-size').fadeIn('fast');
        },
        mouseleave: function () {
            $(this).find('.file-size').fadeOut('fast');
        }
    }, ".image-link");

    //like btn
    $('body').on('click', '.file-like-area', function () {
        console.log('sdfsdf');
        likeBtn = $(this).find('.fa');
        likeBtn.removeClass('fa-heart-o');
        likeBtn.addClass('fa-heart active');
    });
});
