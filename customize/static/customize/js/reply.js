$(document).ready(function() {
  initReply()
  bindReplyAction();
});

var initReply = function() {
  var templateStr = $('#replyHead').attr('template');
  if (templateStr == '' || templateStr == 'None')
    return false;
  var template = $.parseJSON(templateStr);
  $('#materialNav li[name="' + template['MsgType'] + '"]').trigger('click');
  if (template['MsgType'] == 'text') {
    var content = str2face(template['Content']);
    $('#materialText').html(content);
    var textAmount = $('#materialText').text().length + $('#materialText').find('.insertedFace').length;
    $('#materialRemain font').text(parseInt($('#materialRemain font').text()) - textAmount);
  } else if (template['MsgType'] == 'image') {
    $('#materialImage').append('<img src="' + template['ImageUrl'] + '" mediaId="' + template['MediaId'] + '" ori_url="' + template['OriUrl'] + '" />');
    $('#materialImage').append('<a id="deleteImageMaterialBtn">删除</a>');
    $('#chooseImageBtn').hide();
    $('#materialImage').show();
  } else if (template['MsgType'] == 'voice') {
    var box = $('#materialVoice');
    box.attr('mediaId', template['MediaId']);
    box.children('.voiceName').text(template['VoiceName']);
    box.children('.voiceLen').text(template['VoiceLen']);
    $('#chooseVoiceBtn').hide();
    box.show();
  } else if (template['MsgType'] == 'video') {
    var box = $('#materialVideo');
    box.children('.videoName').text(template['Title']);
    box.children('.videoTitle').text(template['Title']);
    box.children('.videoDesc').text(template['Description']);
    box.attr('mediaId', template['MediaId']);
    $('#chooseVideoBtn').hide();
    box.show();
  }
}

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
  	$.post(url, getMaterialContent(), function(res) {
  	  if (res['code'] == 0)
  	    topAlert(res['msg']);
  	  else
  	  	topAlert(res['msg'], 'error');
  	});
  });
}