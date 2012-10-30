$(document).ready(function () {

    var mkLinkListItem = function (href) {
        var a = $('<a>', { href : href }).text(href);
        return li = $('<li>').append(a);
    };

    var addLinks = function (jobId) {
        $(['status', 'result']).each(function (k,v) {
            $('#' + v + '_links').append(mkLinkListItem(
                '/' + v + '?job_id=' + jobId));
        })
    };

    $('form').click(function () {
        $.ajax({
            type    : 'POST',
            url     : '/',
            data    : $(this).serialize(),
            success : function (data) {
                var output = JSON.stringify(data);
                $('#output').text($('#output').text() + '\n' + output);
                addLinks(data.job_id);
            }
        });
        return false;
    });

    $('ol').on('click', 'a', function () {
        open(this.href);
        return false;
    });
});
