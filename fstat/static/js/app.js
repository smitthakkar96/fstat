$('input[name="daterange"]').daterangepicker({
locale: {format: "YYYY-MM-DD"},
}, function(start, end, label) {
    start = start.format('YYYY-MM-DD');
    end = end.format('YYYY-MM-DD');
    var location = window.location.toString().split("?")[0];
    window.location = location + `?start_date=${start}&end_date=${end}`;
});

function showModal(fid, bugs) {
    failure_id = fid
    $('#associate-bug-modal').modal('show');
    $('#bugIds').val(bugs);
    $('#bugIds').tagsinput();
}

function hasNaN(array) {
    for (let i = 0; i < array.length; i++) {
        if (isNaN(array[i])) {
            return true;
        }
    }
    return false;
}

function submit() {
    if ($('#bugIds').val() !== "") {
        var bugIds = $('#bugIds').val().split(',').map(function(bugId){return parseInt(bugId)});
            if (!hasNaN(bugIds)) {
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
                        alert(err.response);
                    }
                });
            } else {
                alert("All BugIDs must be integer.")
            }
    } else {
        alert("Please enter at least one BugID.")
    }
}
