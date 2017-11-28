$(document).ready(function () {
    var $container = $('<div id="fullscreen-container"></div>');
    var $win = $(window);
    var active = false;
    var mouse_on_container = false;
    var img_width, img_height;
    var multiplier = 1;
    var container_mouse_pos_x = 0;
    var container_mouse_pos_y = 0;
    var webm = false;
    var mp4 = false;
    var mp3 = false;
    var video = false;

    var border_offset = 4;

    $('body').append($container);
    window.expand = function (num, src, image_width, image_height, cloud, elem_id) {

		jQuery.get('https://deadmedia.ru/video/hit/' + elem_id)
            .done(function(data) {
                if (data >= 0) $('#' + elem_id).find('.file-views-number').text(data);
            }); //views counter

        if (active == num) {
            hide();
            return false;
        }

        var win_width = $win.width();
        var win_height = $win.height();

        img_width = image_width;
        img_height = image_height;
        multiplier = 1;
        active = num;
        webm = src.substr(-5) == '.webm';
        mp4 = src.substr(-4) == '.mp4';
        mp3 = src.substr(-4) == '.mp3';
        video = webm || mp4 || mp3;
        mouse_on_container = false;

        $container
            .html(video ? '<video id="html5video" name="media" loop="1" controls="" autoplay="" height="100%" width="100%"><source class="video" height="100%" width="100%" type="' + (mp4 ? 'video/mp4' : 'video/webm') + '" src="' + src + '"></source></video>' : '<img src="' + src + '" width="100%" height="100%" />')
            //.append(!cloud?$controls:'')
            .css('top', (((win_height - image_height) / 2) - border_offset) + 'px')
            .css('left', (((win_width - image_width) / 2) - border_offset) + 'px')
            .width(image_width)
            .height(!mp3 ? image_height : '200px')
            .show();

        if (image_width > win_width || image_height > win_height) {
            var multiplier_width = Math.floor(win_width / image_width * 10) / 10;
            var multiplier_height = Math.floor(win_height / image_height * 10) / 10;
            if (multiplier_width < 0.1) multiplier_width = 0.1;
            if (multiplier_height < 0.1) multiplier_height = 0.1;

            resize(multiplier_width < multiplier_height ? multiplier_width : multiplier_height, true);
        }

        return false;
    };

    var hide = function () {
        active = false;
        mouse_on_container = false;
        $container.hide();
        if (video) {
            $container.html('');
        }
    };

    var resize = function (new_multiplier, center) {
        if (new_multiplier < 0.1) return;
        if (new_multiplier > 5) return;

        repos(new_multiplier, center);
        multiplier = new_multiplier;
        $container
            .width(img_width * multiplier)
            .height(img_height * multiplier);
    };

    var repos = function (new_multiplier, center) {
        var scroll_top = $win.scrollTop();
        var scroll_left = $win.scrollLeft();
        var container_offset = $container.offset();
        var x_on_container;
        var y_on_container;
        if (center) {
            x_on_container = img_width / 2;
            y_on_container = img_height / 2;
        } else {
            x_on_container = (container_mouse_pos_x - container_offset.left + scroll_left);
            y_on_container = (container_mouse_pos_y - container_offset.top + scroll_top);
        }
        var container_top = container_offset.top - scroll_top;
        var container_left = container_offset.left - scroll_left;
        var delta_multiplier = new_multiplier - multiplier;
        var delta_top = delta_multiplier * y_on_container / multiplier;
        var delta_left = delta_multiplier * x_on_container / multiplier;

        $container
            .css('left', (container_left - delta_left) + 'px')
            .css('top', (container_top - delta_top) + 'px');
    };

    $container.mouseover(function () {
        mouse_on_container = true;
    });

    $container.mouseout(function () {
        mouse_on_container = false;
    });

    $container.mousemove(function (e) {
        container_mouse_pos_x = e.clientX;
        container_mouse_pos_y = e.clientY;
    });

    $win.keyup(function (e) {
        if (!active) return;
        var move;
        var code = e.keyCode || e.which;

        if (code == 37 || code == 65 || code == 97 || code == 1092) {
            move = -1;
        } else if (code == 39 || code == 68 || code == 100 || code == 1074) {
            move = 1;
        } else if (code == 27) {
            return hide();
        } else {
            return;
        }

        var $images = $('.image-link');
        var active_index = $images.index($('#exlink-' + active));
        var new_index = active_index + move;
        if (new_index < 0) new_index = $images.length - 1;
        if (new_index > $images.length - 1) new_index = 0;
        var next = $images.eq(new_index);

        next.find('a').click();
    });

    $win.click(function (e) {
        console.log($(e.target).closest('#fullscreen-container').length);
        if (!active) return;
        if (e.which != 1) return;
        if ($(e.target).closest('.img').length) return;
        if ($(e.target).closest('#fullscreen-container').length) return;

    });

    $win.on((/Firefox/i.test(navigator.userAgent)) ? "DOMMouseScroll" : "mousewheel", function (e) {
        if (!active) return;
        if (!mouse_on_container) return;
        e.preventDefault();
        var evt = window.event || e; //equalize event object
        evt = evt.originalEvent ? evt.originalEvent : evt; //convert to originalEvent if possible
        var delta = evt.detail ? evt.detail * (-40) : evt.wheelDelta; //check for detail first, because it is used by Opera and FF

        if (delta > 0) {
            resize(multiplier + 0.1);
        } else {
            resize(multiplier - 0.1);
        }
    });

    draggable($container, {
        click: function () {
            console.log('hide');
            hide();
        },
        mousedown: function (e_x, e_y) {
            console.log(webm + '-' + mp4);
            if (!video) return; //@todo упаковать типы
            console.log('after');
            var container_top = parseInt($container.css('top'));
            var container_height = $container.height();

            if ((container_top + container_height) - e_y < 35) return false;
        }
    });

    function draggable(el, events) {
        var in_drag = false;
        var moved = 0;
        var last_x, last_y;

        var win = $(window);

        el.mousedown(function (e) {
            if (e.which != 1) return;
            if (events && events.mousedown && events.mousedown(e.clientX, e.clientY) === false) return;
            e.preventDefault();
            in_drag = true;
            moved = 0;

            last_x = e.clientX;
            last_y = e.clientY;
        });

        win.mousemove(function (e) {
            var delta_x, delta_y;
            var el_top, el_left;

            if (!in_drag) return;

            delta_x = e.clientX - last_x;
            delta_y = e.clientY - last_y;
            moved += Math.abs(delta_x) + Math.abs(delta_y);

            last_x = e.clientX;
            last_y = e.clientY;

            el_top = parseInt(el.css('top'));
            el_left = parseInt(el.css('left'));

            el.css({
                top: (el_top + delta_y) + 'px',
                left: (el_left + delta_x) + 'px'
            });
        });

        win.mouseup(function (e) {
            if (!in_drag) return;
            in_drag = false;
            if (moved < 6 && events && events.click) events.click(last_x, last_y);
        });
    }
});