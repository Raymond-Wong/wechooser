$(document).ready(function() {
  bindMaterialAction();
});

var bindMaterialAction = function() {
  changeMsgTypeAction();
  showFacesAction();
  chooseFaceAction();
  listenInput();
  showMaterialBoxAction();
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
    insertIntoCaret('materialText', insertFaceStr);
    updateRemainChar();
  	return false;
  });
}

// 监听输入框变化
var listenInput = function() {
  var materialText = $('#materialText')[0];
  $('#materialText').keydown(function(evt) {
    if (evt.keyCode == '13') {
      // insertIntoCaret('materialText', '<nl />');
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
  // 在每个div前面加一个换行符
  tmpDiv.find('div').each(function() {
    $(this).append('\n');
  })
  tmpDiv.find('img').each(function() {
    var face = $(this).attr('name');
    $(this).before(face);
    $(this).remove();
  });
  params = {'MsgType' : 'text'};
  // 去除连续的空行
  // var content = tmpDiv.text().split('\n');
  // for (var i = 0; i < content.length; i++) {
  //   if (content[i] == '')
  //     content.splice(i, 1);
  // }
  // params['Content'] = content.join('\n');
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
  // var imageUrl = $('#materialImage img').attr('src');
  imageUrl = undefined;
  var oriUrl = $('#materialImage img').attr('ori_url');
  params = {'MsgType' : 'image', 'MediaId' : mediaId, 'ImageUrl' : imageUrl, 'OriUrl' : oriUrl};
  return params;
}

var voiceHandler = function() {
  var mediaId = $('#materialVoice').attr('mediaId');
  var voiceName = $('#materialVoice').children('.voiceName').text()
  params = {'MsgType' : 'voice', 'MediaId' : mediaId, 'VoiceName' : voiceName};
  return params;
}

var videoHandler = function() {
  var mediaId =$('#materialVideo').attr('mediaId');
  var title = $('#materialVideo').children('.videoTitle').text();
  var name = $('#materialVideo').children('.videoName').text();
  var desc = $('#materialVideo').children('.videoDesc').text();
  params = {'MsgType' : 'video', 'MediaId' : mediaId, 'Title' : title, 'Name' : name, 'Description' : desc};
  return params;
}

var newsHandler = function() {
  var box = $('#materialNews');
  var params = {'MsgType' : 'news'};
  box = $(box.find('.newsItemWrapper')[0]);
  params['MediaId'] = box.attr('mediaId');
  params['item'] = []
  $(box.find('.newsItemBox')).each(function() {
    var item = {};
    item['Url'] = $(this).attr('url');
    item['Title'] = $(this).children('.newsItemTitle').text()
    item['Description'] = $(this).attr('description');
    item['PicUrl'] = $(this).attr('thumbUrl');
    item['MediaId'] = $(this).attr('mediaId');
    params['item'].push(item);
  });
  return params;
}


var getMaterialContent = function() {
  var HANDLERS = {
    'text' : textHandler,
    'image' : imageHandler,
    'voice' : voiceHandler,
    'video' : videoHandler,
    'news' : newsHandler,
  };
  var choosenType = $('#materialNav li.active').attr('name');
  return HANDLERS[choosenType]();
}


// 当素材框中是图片素材框时，将内容提取出来
var saveImage = function() {
  var choosenImage = $('.imageItem.choosen');
  var imgUrl = $(choosenImage.find('img')[0]).attr('src');
  var mediaId = choosenImage.attr('mediaId');
  var ori_url = choosenImage.attr('ori_url');
  $('#materialImage').html('');
  $('#materialImage').append('<img src="' + imgUrl + '" mediaId="' + mediaId + '" ori_url="' + ori_url + '"/>');
  $('#materialImage').append('<a id="deleteImageMaterialBtn" class="deleteMaterialBtn">删除</a>');
  $('#chooseImageBtn').hide();
  $('#materialImage').show();
  $('#materialBoxWrapper').fadeOut();
}

// 当素材框中是语音素材时，将内容提取出来
var saveVoice = function() {
  var choosenVoice = $($('input[name="voiceSelect"]:checked').parents('.voiceItem')[0]);
  var mediaId = choosenVoice.attr('mediaId');
  var name = choosenVoice.children('.voiceName').text();
  var len = choosenVoice.children('.voiceLen').text();
  $('#materialVoice').children('.voiceName').text(name);
  $('#materialVoice').children('.voiceLen').text(len);
  $('#materialVoice').attr('mediaId', mediaId);
  $('#chooseVoiceBtn').hide();
  $('#materialVoice').show();
  $('#materialBoxWrapper').fadeOut();
}

// 当素材框中是视频素材时，将内容提取出来
var saveVideo = function() {
  var choosenVideo = $($('input[name="videoSelect"]:checked').parents('.videoItem')[0]);
  var mediaId = choosenVideo.attr('mediaId');
  var name = choosenVideo.children('.videoName').text();
  var title = choosenVideo.children('.videoTitle').text();
  var desc = choosenVideo.children('.videoDesc').text();
  $('#materialVideo').children('.videoName').text(name);
  $('#materialVideo').children('.videoTitle').text(title);
  $('#materialVideo').children('.videoDesc').text(desc);
  $('#materialVideo').attr('mediaId', mediaId);
  $('#chooseVideoBtn').hide();
  $('#materialVideo').show();
  $('#materialBoxWrapper').fadeOut();
}

var saveNews = function() {
  var choosenNews = $('.newsItemWrapper.choosen').clone();
  $($('.newsItemWrapper.choosen').find('.choosenFlag')[0]).remove();
  $('.newsItemWrapper.choosen').removeClass('choosen');
  $(choosenNews.find('.choosenFlag')[0]).remove();
  choosenNews.removeClass('choosen');
  $('#materialNews .newsItemWrapper').remove();
  $('#materialNews').prepend(choosenNews);
  $('#chooseNewsBtn').hide();
  $('#materialNews').show();
  $('#materialBoxWrapper').fadeOut();
}

var showMaterialBoxAction = function() {
  var handlers = {
    'Image' : saveImage,
    'Voice' : saveVoice,
    'Video' : saveVideo,
    'News' : saveNews,
  };
  $('.showMaterialBoxBtn').click(function() {
    var type = $(this).attr('type');
    showMaterialBox(type, handlers[type]);
  });
}