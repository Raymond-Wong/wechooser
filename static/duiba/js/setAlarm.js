$(document).ready(function() {
  saveAction();
});

var saveAction = function() {
  $('#saveBtn').click(function() {
    var hour = parseInt($('input[name="hour"]').val());
    var minute = parseInt($('input[name="minute"]').val());
    if (hour < 0 || hour >= 24) {
      alert('小时不合法');
      return false;
    }
    if (minute < 0 || minute >= 60) {
      alert('分钟不合法');
      return false;
    }
    alert('hour: ' + hour + '; minute: ' + minute);
    post('/duiba/setAlarm', {'hour' : hour, 'minute' : minute}, function(msg) {
      alert(msg['msg']);
    });
  });
}