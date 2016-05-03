$(document).ready(function() {
  $.post('/wechat/getMaterial', {'type' : 'news', 'count' : 10, 'offset' : 0}, function(res) {
  	console.log(res);
  	$('#material').html(JSON.stringify(res));
  });
});