$('input[name="daterange"]').daterangepicker({
locale: {format: "YYYY-MM-DD"},
}, function(start, end, label) {
    start = start.format('YYYY-MM-DD');
    end = end.format('YYYY-MM-DD');
    var location = window.location.toString().split("?")[0];
    window.location = location + `?start_date=${start}&end_date=${end}`;
});

function showModal(fid, bugs) {
    console.log(bugs);
    failure_id = fid
    $('#associate-bug-modal').modal('show');
    $('#bugIds').val(bugs);
    $('#bugIds').tagsinput();
}

function submit() {
    var bugIds = $('#bugIds').val().split(',').map(function(bugId){return parseInt(bugId)});
    var URL = `/associate-bugs/${failure_id}`;
        $.ajax({
            url: URL,
            beforeSend: function(xhr){
                xhr.setRequestHeader("Content-Type","application/json");
            },
            data: JSON.stringify({bugIds: bugIds}),
            type: 'POST',
            success: function(data, status, xhr){
                location.reload();
            },
            error: function(err, status, xhr){
            }
        });

    // $.post(URL, JSON.stringify({bugIds: bugIds}), function(data) {
    //     $('#associate-bug-modal').modal('show');
    //     location.reload();
    // }, 'json');
}