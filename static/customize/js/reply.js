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
    var start = content.indexOf('\n');
    var end = content.indexOf('\n', start + 1);
    var lines = [];
    if (start < 0) {
      lines.push(content);
    } else {
      lines.push(content.substring(0, start));
      while (true) {
        end = end > 0 ? end : content.length;
        var lineContent = content.substring(start + 1, end);
        lineContent = (lineContent == '' ? '<br>' : lineContent);
        lines.push('<div>' + lineContent + '</div>');
        start = content.indexOf('\n', end);
        if (start < 0) break;
        end = content.indexOf('\n', start + 1);
      }
      lines.push('<div>' + content.substring(end + 1, content.length) + '</div>');
    }
    $('#materialText').html(lines.join(''));
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
  var deleteBtn = $('#deleteBtn');
  saveBtn.click(function() {
  	var url = window.location.pathname + window.location.search;
  	var params = getMaterialContent();
  	if (params['MsgType'] == null) {
  	  topAlert(params['Content'], 'error');
  	  return false;
  	}
    console.log(params);
    if ((params['MsgType'] == 'text' && params['Content'] == "") ||
        (params['MsgType'] != 'text' && (params['MediaId'] == undefined || params['MediaId'] == 'undefined'))) {
      topAlert('未选择素材', 'error');
      return false;
    }
    topAlert('正在保存中...');
  	$.post(url, params, function(res) {
  	  if (res['code'] == 0)
  	    topAlert(res['msg']);
  	  else
  	  	topAlert(JSON.stringify(res['msg']), 'error');
  	});
  });
  deleteBtn.click(function() {
    var url = window.location.pathname + '/delete' + window.location.search
    topAlert('正在删除中...');
    $.get(url, {}, function(res) {
      topAlert('回复删除成功');
    });
  });
}