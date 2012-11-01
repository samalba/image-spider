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
            tr = $('<tr>');
        tr.append(mkCell(jobId));
        $(['status', 'result', 'stop']).each(function (k,v) {
            tr.append(mkLinkCell(v, '/' + v + qs));
        })
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
