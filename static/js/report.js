$(document).ready(function () {
    function deleteRow(button, decision) {
        var row = $(button).closest('tr')
            .children('td')
            .css({
                backgroundColor: decision,
                borderColor: decision
            });
        setTimeout(function () {
            $(row)
                .animate({
                    paddingTop: 0,
                    paddingBottom: 0
                }, 500)
                .wrapInner('<div />')
                .children()
                .slideUp(500, function () {
                    $(this).closest('tr').remove();
                });
        }, 350);
    };
    $('body').on('click', '.report-file-delete', function () {
        var elem_id = $(this).parent().parent().find(".report-file-name").attr('id');
        console.log("/video/" + elem_id + "/delete/");
        jQuery.getJSON("/video/" + elem_id + "/delete/");
        deleteRow(this, "red");
        alertTip("File deleted");
    });
    $('body').on('click', '.report-file-ok', function () {
        var elem_id = $(this).parent().parent().find(".report-file-name").attr('id');
        console.log("/video/" + elem_id + "/reports/reset/");
        jQuery.getJSON("/video/" + elem_id + "/reports/reset/");
        deleteRow(this, "#80E800");
        alertTip("Report deleted");
    });
});
