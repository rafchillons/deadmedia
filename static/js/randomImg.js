$(document).ready(function () {
    function random_img() {
        var myimages = new Array()
        myimages[1] = "img_1.png"
        myimages[2] = "img_2.png"

        var ry = Math.floor(Math.random() * myimages.length)
        if (ry == 0)
            ry = 1
        $(".admin-sign-in-image").html('<img src="/assets/img/' + myimages[ry] + '" width="302px" title="Administration" alt="Adminpanel9000">');

    }
    random_img()
});
