$(document).ready(function() {
  $('.releaseActivityBtn').click(function() {
    var aid = $(this).attr('aid');
    post('/transmit/activity/release', {'aid' : aid}, function(resp) {
      if (resp['code'] == 0) {
        window.location.href = window.location.href;
      } else {
        topAlert(resp['msg'], 'error');
      }
    });
  });
});