$(document).ready(function() {
  bindReplyAction();
});

var bindReplyAction = function() {
  var saveBtn = $('#saveBtn');
  saveBtn.click(function() {
  	var url = window.location.pathname + window.location.search;
  	var params = getMaterialContent();
  	if (params['MsgType'] == null) {
  	  topAlert(params['Content'], 'error');
  	  return false;
  	}
    console.log(getMaterialContent());
  	// $.post(url, getMaterialContent(), function(res) {
  	//   if (res['code'] == 0)
  	//     topAlert(res['msg']);
  	//   else
  	//   	topAlert(res['msg'], 'error');
  	// });
  });
}