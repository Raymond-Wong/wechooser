$(document).ready(function() {
  $('.releaseActivityBtn').click(function() {
    if (!confirm("确认发布？\n发布后的活动不可撤销！")) return false;
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