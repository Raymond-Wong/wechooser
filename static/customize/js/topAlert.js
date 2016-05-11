var alertBox = $('#alertBox');
var topAlertTimer = null;
var alertType = 'info';

var topAlert = function(msg, tp) {
  // 终止上一次的动作
  alertBox.stop(true, true);
  clearTimeout(topAlertTimer);
  alertType = tp;
  hideTopAlert(function() {
    // 开始下一次的动作
    if (alertType == 'error') {
      alertBox.css('backgroundColor', '#110000');
    } else {
      alertBox.css('backgroundColor', '#09bb07');
    }
    alertBox.html(msg);
    alertBox.animate({'top' : '0px'});
    topAlertTimer = setTimeout(hideTopAlert, 5000);  
  });
}

var hideTopAlert = function(callback) {
  alertBox.animate({'top' : '-3em'}, callback);
}