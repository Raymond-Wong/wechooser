$(document).ready(function() {
  var msgType = "image";
  var url = '/reply' + window.location.search;
  $('#btn').click(function() {
  	var content = $('#replyText').val();
  	$.post(url, {'MsgType' : msgType, 'MediaId' : content}, function(res) {
  	  console.log(res);
  	});
  });
});