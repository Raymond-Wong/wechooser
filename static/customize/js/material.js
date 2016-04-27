$(document).ready(function() {
  $.post('/wechat/getMaterial', {'type' : 'image'}, function(res) {
  	$('#material').text(res);
  });
});