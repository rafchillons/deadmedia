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

    $('body').on('click', '.file-admin-tools-btn', function () {
        $(this).parent().find('.file-change-category').slideToggle("fast");
    });

    $('body').on('click', '.file-delete-btn', function () {
        $(this).css('cursor', 'default').css('text-decoration', 'none').css('color', 'red');
        $(this).text("Deleted");
        image = $(this).parent().parent().parent().parent();
        imageId = image.attr('id');
        console.log(imageId);

        linkImage = $('#' + imageId).children().find('.image-link');
        jQuery.getJSON("/video/" + imageId + "/delete/");

        linkImage.css("background-image", "url(/assets/img/deleted.png)");
        linkImage.attr("onclick", " ");
        linkImage.css('cursor', 'default');
        linkImage.css('opacity', '0.7');
        $(this).parent().find('.file-admin-tools-btn').remove();
    });

    //file change category 
    $('body').on('click', '.file-category-change-btn', function () {
        console.log("change category");
        $(this).css('cursor', 'default').css('text-decoration', 'none').css('color', 'red');
        $(this).text("Moved");
        var category = $(this).parent().find('.file-category-change-select :selected').text();
        image = $(this).parent().parent().parent().parent().parent();
        imageId = image.attr('id');

        linkImage = $('#' + imageId).children().find('.image-link');
        jQuery.getJSON("/video/" + imageId + "/move/" + category + "/");

        linkImage.css("background-image", "url(/assets/img/category.jpg)");
        linkImage.attr("onclick", " ");
        linkImage.css('cursor', 'default');
        linkImage.css('opacity', '0.7');
        $(this).parent().find('.file-category-change-select').remove();
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


    //report btn 
    $('body').on('click', '.file-report', function () {
        $(this).css('cursor', 'default').css('text-decoration', 'none').css('font-style', 'italic');
        $(this).text("Reported");
        image = $(this).parent().parent().parent().parent();
        imageId = image.attr('id');
        jQuery.getJSON("/video/" + imageId + "/report/");
    });

    //like btn
    $('body').on('click', '.file-like-area', function () {
        elem_id = $(this).parent().parent().parent().parent().parent().attr('id');
        console.log('Лайк-лайк-ла-ла-лайк!');
        likeBtn = $(this).find('.fa');
        likeBtn.removeClass('fa-heart-o');
        likeBtn.addClass('fa-heart active');
        jQuery.get('/video/' + elem_id + '/like/')
            .done(function (data) {
                if (data == "True") {
                    var currentLikesCountInc = parseInt($('#' + elem_id).find('.file-likes-number').text()) + 1;
                    $('#' + elem_id).find('.file-likes-number').text(currentLikesCountInc);
                }
            });
    });
});
