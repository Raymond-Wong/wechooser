$(document).ready(function() {
  releaseAction();
  deleteAction();
});

var deleteAction = function() {
  $('.delActivityBtn').click(function() {
    if (!confirm("确认删除活动？\n删除后的活动不可撤销！")) return false;
    var aid = $($(this).parents('.activity_box')[0]).attr('aid');
    post('/transmit/activity/delete', {'aid' : aid}, function(resp) {
      if (resp['code'] == 0) {
        window.location.href = window.location.href;
      } else {
        topAlert(resp['msg'], 'error');
      }
    });
  });
}

var releaseAction = function() {
  $('.releaseActivityBtn').click(function() {
    if (!confirm("确认发布活动？\n发布后的活动不可撤销！")) return false;
    var aid = $($(this).parents('.activity_box')[0]).attr('aid');
    post('/transmit/activity/release', {'aid' : aid}, function(resp) {
      if (resp['code'] == 0) {
        window.location.href = window.location.href;
      } else {
        topAlert(resp['msg'], 'error');
      }
    });
  });
}