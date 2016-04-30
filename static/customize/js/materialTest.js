$(document).ready(function() {
  $.post('/wechat/getMaterial', {'type' : 'image', 'count' : 10, 'offset' : 0}, function(res) {
  	$('#material').html(res);
  });
});