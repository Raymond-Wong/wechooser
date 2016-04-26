$(document).ready(function() {
  var form = $('#menuForm');
  form.submit(function() {
  	var menu = $('#menu').val();
  	var params = {"menu" : menu};
  	$.post('/wechat/menu', params, function(res) {
  		console.log(res);
  	});
  });
});