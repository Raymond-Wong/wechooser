var alertBox = $('#alertBox');
var topAlertTimer = null;

var topAlert = function(msg, tp) {
  var tp = tp ? tp : 'info';
  console.log("alert: " + msg);
  alertBox.html(msg);
  alertBox.animate({'top' : '0px'});
  if (tp == 'error') {
  	topAlertTimer = alertBox.css('backgroundColor', 'red');
  }
  setTimeout(hideTopAlert, 5000);
}

var hideTopAlert = function() {
  alertBox.animate({'top' : '-3em'}, function() {
  	alertBox.css('backgroundColor', '#09bb07')
  });
}