var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('progress_update', function(data) {
        document.getElementById("progress_label").innerHTML = data.percentage + "%";
        document.getElementById("progress_bar").value = data.percentage;
    });

    socket.on('download_status', function(data) {
        alert(data.message);
    });