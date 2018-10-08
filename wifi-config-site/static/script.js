var ws = null;
var sendMes = ["", "", ""];

// èâä˙âª...
window.addEventListener('load', function() {
    url = "ws://" + location.hostname + ":80/pipe";
    ws = new WebSocket(url);

    var btn_save_r = document.getElementById('submit_save_reboot');
    btn_save_r.addEventListener('click', function() {
            sendMes[0] = "save-reboot";
            sendMes[1] = document.getElementById('ssid_input').value;
            sendMes[2] = document.getElementById('password_input').value;
            ws.send(sendMes);
    });

    var btn_nosave_r = document.getElementById('submit_nosave_reboot');
    btn_nosave_r.addEventListener('click', function() {
            sendMes[0] = "nosave_reboot";
            sendMes[1] = "";
            sendMes[2] = "";
            ws.send(sendMes);
    });

    ws.onmessage = function(e) {
        document.getElementById("previous_ip").innerHTML = e.data;
    }
});
