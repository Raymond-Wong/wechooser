$(document).ready(function() {
  var form = $('#menuForm');
  form.submit(function() {
  	var menu = JSON.stringify($('#menu').text());
  	var params = {"menu" : menu};
  	$.post('/wechat/menu', params, function(res) {
  		console.log(res);
  	});
  });
});