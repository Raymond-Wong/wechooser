$(document).ready(function() {
  var msgType = "text";
  var url = '/reply' + window.location.search;
  $('#btn').click(function() {
  	var content = $('#replyText').val();
  	$.post(url, {'MsgType' : msgType, 'Content' : content}, function(res) {
  	  console.log(res);
  	});
  });
});