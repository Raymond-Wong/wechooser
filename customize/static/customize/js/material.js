$(document).ready(function() {
  bindMaterialAction();
});

var bindMaterialAction = function() {
  changeMsgTypeAction();
  showFacesAction();
  chooseFaceAction();
  listenInput();
}

// 切换回复消息类型的事件
var changeMsgTypeAction = function() {
  $('#materialNav li').click(function() {
    $('.materialPanel.active').removeClass('active');
    $('#materialNav li.active').removeClass('active');
    $('#' + $(this).attr('target')).addClass('active');
    $(this).addClass('active');
  });
}

// 显示表情菜单
var showFacesAction = function() {
  $('#materialFace').click(function() {
  	$('#faceTable').fadeIn();
  	return false;
  });
  $(window).click(function() {
  	$('#faceTable').fadeOut();
  });
}

// 插入表情时间
var chooseFaceAction = function() {
  $('#faceTable tr td').click(function() {
  	var face = $(this).children('img');
  	var materialText = $('#materialText');
  	var insertFaceStr = '<img src="' + face.attr('src') + '" name="' + face.attr('name') + '" class="insertedFace" />';
    materialText.append(insertFaceStr);
    updateRemainChar();
  	return false;
  });
}

// 监听输入框变化
var listenInput = function() {
  var materialText = $('#materialText')[0]
  $('#materialText').keydown(function(evt) {
    if (evt.keyCode == '13') {
      return false;
    }
  });
  if (materialText.addEventListener) {
    materialText.addEventListener('DOMCharacterDataModified', function(evt) {
      updateRemainChar();
    }, false);
  }
}

// 更新可输入字符数
var updateRemainChar = function() {
  var materialText = $('#materialText');
  var remainText = $('#materialRemain font');
  var charAmount = materialText.text().length;
  var faceAmount = materialText.find('.insertedFace').length;
  var remainAmount = 600 - charAmount - faceAmount;
  remainText.text(remainAmount);
  return remainAmount;
}

// 将text信息返回给后台的json
var textHandler = function() {
  var tmpDiv = $('#materialText').clone();
  tmpDiv.find('img').each(function() {
    var face = $(this).attr('name');
    $(this).before(face);
    $(this).remove();
  });
  params = {'MsgType' : 'text'};
  params['Content'] = tmpDiv.text();
  if (parseInt($('#materialRemain font').text()) < 0) {
    params['MsgType'] = null;
    params['Content'] = '输入字数不可超过600字';
    return params;
  }
  return params;
}

// 将image信息返回给后台的json
var imageHandler = function() {
  var mediaId = $('#materialImage img').attr('mediaId');
  params = {'MsgType' : 'image', 'MediaId' : mediaId};
  return params;
}

var voiceHandler = function() {
  var mediaId = $('#materialVoice').attr('mediaId');
  params = {'MsgType' : 'voice', 'MediaId' : mediaId};
  return params;
}

var videoHandler = function() {
  var mediaId =$('#materialVideo').attr('mediaId');
  params = {'MsgType' : 'video', 'MediaId' : mediaId};
  return params;
}

var HANDLERS = {
  'text' : textHandler,
  'image' : imageHandler,
  'voice' : voiceHandler,
  'video' : videoHandler,
  // 'news' : newsHandler,
};
var getMaterialContent = function() {
  var choosenType = $('#materialNav li.active').attr('name');
  return HANDLERS[choosenType]();
}
