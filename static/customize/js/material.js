$(document).ready(function() {
  $.post('/wechat/getMaterial', {'type' : 'image', 'offset' : 0, 'count' : 1}, function(res) {
  	$('#material').text(res);
  });
});