$(document).ready(function() {
  $('#updateTokenBtn').click(function() {
	post('/wechat/update', {}, function() {
	  topAlert('更新token成功');
	});
  })
});