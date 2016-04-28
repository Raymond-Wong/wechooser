var alertBox = $('#alertBox');

var topAlert = function(msg) {
  console.log("alert: " + msg);
  alertBox.html(msg);
  alertBox.animate({'top' : '0px'});
  setTimeout(hideTopAlert, 5000);
}

var hideTopAlert = function() {
  alertBox.animate({'top' : '-3em'});
}