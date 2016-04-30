$(document).ready(function() {
  bindMaterialBoxAction();
});

var bindMaterialBoxAction = function() {
  showMaterialBoxAction();
  hideMaterialBoxAction();
  toPageAction();
  saveAction();
  bindMaterialImageBoxAction();
  bindMaterialVoiceBoxAction();
}

var bindMaterialImageBoxAction = function() {
  updateMaterialImageBox(0, 10);
  chooseImageAction();
  deleteImageAction();
}

var bindMaterialVoiceBoxAction = function() {
  updateMaterialVoiceBox(0, 5);
  deleteVoiceAction();
}

// 跳转页码
var toPageAction = function() {
  $('.materialBoxPageWrapper .toPageBtn').click(function() {
    var page = parseInt($($(this).siblings('.toPage')[0]).val());
    var type = $($(this).parents('.materialBox')[0]).attr('id');
    var totalPage = parseInt($($(this).siblings('.totalPage')[0]).text());
    var offset = parseInt($(this).attr('offset'));
    var curPage = parseInt($($(this).parents('.materialBox')[0]).attr('curPage'));
    curPage = curPage ? curPage : 1;
    if (page == curPage) {
      page += offset;
    }
    if (page > totalPage || page <= 0) {
      topAlert('目标页数不合法', 'error');
      return false;
    }
    $($(this).parents('.materialBox')[0]).attr('curPage', page);
    $($(this).siblings('.toPage')[0]).val(page);
    if (type == 'materialImageBox') {
      updateMaterialImageBox(10 * (page - 1), 10);
    } else if (type == 'materialVoiceBox') {
      updateMaterialVoiceBox(5 * (page - 1), 5);
    }
  });
}

// 更新图片素材框中的图片
var updateMaterialImageBox = function(offset, count, callback) {
  var params = {'type' : 'image', 'count' : count, 'offset' : offset};
  var box = $('#materialImageBox .materialBoxInner .materialBoxContent');
  // 清空容器中的东西
  box.html(LOADING_ELEMENT);
  $.post('/wechat/getMaterial', params, function(res) {
    var images = res['msg']['item'];
    var totalCount = res['msg']['total_count'];
    $($('#materialImageBox').find('.totalPage')[0]).text(Math.ceil(totalCount / 10));
    for (var i = 0; i < images.length; i++) {
      var image = images[i];
      var url = image['url'];
      var mediaId = image['media_id'];
      var name = image['name'];
      var newImgItem = $(IMG_ITEM);
      newImgItem.attr('mediaId', mediaId);
      $(newImgItem.find('img')[0]).attr('src', url);
      newImgItem.children('.imageName').html(name);
      box.append(newImgItem);
    }
    box.children('.loadingElement').remove();
  }); 
}

// 更新语音素材框中的语音
var updateMaterialVoiceBox = function(offset, count, callback) {
  var params = {'type' : 'voice', 'count' : count, 'offset' : offset};
  var box = $('#materialVoiceBox .materialBoxContent');
  box.html(LOADING_ELEMENT);
  $.post('/wechat/getMaterial', params, function(res) {
    var voices = res['msg']['item'];
    var totalCount = res['msg']['total_count'];
    $($('#materialVoiceBox').find('.totalPage')[0]).text(Math.ceil(totalCount / 5));
    for (var i = 0; i < voices.length; i++) {
      var voice = voices[i];
      console.log(voice);
      var name = voice['name'];
      var mediaId = voice['media_id'];
      var len = voice['length'];
      newVoiceItem = $(VOICE_ITEM);
      newVoiceItem.children('voiceName').text(name);
      newVoiceItem.children('voiceLen').text(len);
      newVoiceItem.attr('mediaId', mediaId);
      box.append(newVoiceItem);
    }
    box.children('.loadingElement').remove();
  });
}

// 显示素材框
var showMaterialBoxAction = function() {
  var btns = $('.showMaterialBoxBtn');
  btns.click(function() {
  	var type = $(this).attr('type');
  	$('.materialBox.active').removeClass('active');
  	$('#material' + type + 'Box').addClass('active');
  	$('#materialBoxWrapper').fadeIn();
  });
}

// 隐藏素材框
var hideMaterialBoxAction = function() {
  $('.hideMaterialBoxBtn').click(function() {
  	$('#materialBoxWrapper').fadeOut();
  });
}

// 选择图片
var chooseImageAction = function() {
  $(document).delegate('.imageItem', 'click', function() {
    var oldChoosenImage = $('.imageItem.choosen');
    var choosenFlag = $(oldChoosenImage.find('.choosenFlag')[0]);
    if (oldChoosenImage.length > 0) {
      oldChoosenImage.removeClass('choosen');
    } else {
      choosenFlag = '<div class="choosenFlag vertical_outer"><span class="vertical_inner glyphicon glyphicon-ok"></span></div>';
    }
    $(this).children('.imageContentBox').append(choosenFlag);
    $(this).addClass('choosen');
    $('.choosenAmount').text('1');
  });
}

// 删除已选择的图片
var deleteImageAction = function() {
  $(document).delegate('#materialImage a', 'click', function() {
    $('#materialImage').html('');
    $('#materialImage').hide();
    $('#chooseImageBtn').show();
    var choosenImage = $('.imageItem.choosen');
    var choosenFlag = $(choosenImage.find('.choosenFlag')[0]);
    choosenImage.removeClass('choosen');
    choosenFlag.remove();
  });
}

// 删除已选语音
var deleteVoiceAction = function() {
  $('#deleteImageMaterialBtn').click(function() {
    $('input[name="voiceSelect"]:checked').removeAttr('checked');
    $('#materialVoice').hide();
    $('#materialVoiceWrapper .showMaterialBoxBtn').show();
  });
}

// 当素材框中是图片素材框时，将内容提取出来
var saveImage = function() {
  var choosenImage = $('.imageItem.choosen');
  var imgUrl = $(choosenImage.find('img')[0]).attr('src');
  var mediaId = choosenImage.attr('mediaId');
  $('#materialImage').append('<img src="' + imgUrl + '" mediaId="' + mediaId + '" />');
  $('#materialImage').append('<a id="deleteImageMaterialBtn">删除</a>');
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

// 点击素材框中的保存按钮时，根据当前素材框显示的信息类别不同，选择不同的handler来提取素材狂内容并隐藏素材狂
var saveAction = function() {
  var handlers = {
  	'materialImageBox' : saveImage,
    'materialVoiceBox' : saveVoice,
  }
  $('#choosenBtn').click(function() {
  	var type = $('.materialBox.active').attr('id');
  	return handlers[type]();
  });
}
