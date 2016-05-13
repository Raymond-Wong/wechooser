$(document).ready(function() {
  post('/wechat/update', {}, function() {
  	topAlert('更新token成功');
  });
});