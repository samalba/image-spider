$(document).ready(function () {

    var mkCell = function (content) {
        return $('<td>').append(content);
    };

    var mkLinkCell = function (text, href) {
        var a = $('<a>', { href : href }).text(text);
        return mkCell(a);
    };

    var addRow = function (jobId) {
        var qs = '?job_id=' + jobId,
            tr = $('<tr>'),
            button = $('<button>').
                text('stop').
                click(function () {
                    btn = $(this).
                       attr('disabled', 'disabled').
                       text('stopping\u2026');
                    $.ajax({
                        type    : 'POST',
                        url     : '/stop?' + jobId,
                        success : function () {
                            btn.text('stopped');
                        }
                    });
                });

        tr.append(mkCell(jobId));
        $(['status', 'result']).each(function (k,v) {
            tr.append(mkLinkCell(v, '/' + v + qs));
        })
        tr.append(mkCell(button));
        $('table').append(tr);
    };

    $('form input').click(function () {
        $('#loading').show();
        $.ajax({
            type    : 'POST',
            url     : '/',
            data    : $('form').serialize(),
            success : function (data) {
                var output = JSON.stringify(data);
                $('#output').text($('#output').text() + '\n' + output);
                addRow(data.job_id);
                $('#loading').hide();
            }
        });
        return false;
    });

    $('table').on('click', 'a', function () {
        open(this.href);
        return false;
    });
});
