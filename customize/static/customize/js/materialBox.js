var SAVE_HANDLER = null;

$(document).ready(function() {
  bindMaterialBoxAction();
});

var bindMaterialBoxAction = function() {
  hideMaterialBoxAction();
  toPageAction();
  saveAction();
  bindMaterialTextBoxAction();
  bindMaterialImageBoxAction();
  bindMaterialVoiceBoxAction();
  bindMaterialVideoBoxAction();
  bindMaterialNewsBoxAction();
  bindMaterialMpNewsBoxAction();
}

var bindMaterialTextBoxAction = function() {
  showFace();
  chooseFace();
  remainCharAmount();
}

var bindMaterialImageBoxAction = function() {
  chooseImageAction();
  deleteImageAction();
}

var bindMaterialVoiceBoxAction = function() {
  deleteVoiceAction();
}

var bindMaterialVideoBoxAction = function() {
  deleteVideoAction();
}

var bindMaterialNewsBoxAction = function() {
  chooseNewsAction();
  deleteNewsAction();
}

var bindMaterialMpNewsBoxAction = function() {
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
    } else if (type == 'materialVideoBox') {
      updateMaterialVideoBox(5 * (page - 1), 5);
    } else if (type == 'materialNewsBox') {
      updateMaterialNewsBox(2 * (page - 1), 2);
    } else if (type == 'materialMpNewsBox') {
      updateMaterialMpNewsBox(5 * (page - 1), 5);
    }
  });
}

// 更新图片素材框中的图片
var updateMaterialImageBox = function(offset, count, callback) {
  // return false;
  console.log('update image material: (', offset, ', ', count, ')');
  var params = {'type' : 'image', 'count' : count, 'offset' : offset};
  var box = $('#materialImageBox .materialBoxInner .materialBoxContent');
  // 清空容器中的东西
  box.html(LOADING_ELEMENT);
  post('/wechat/getMaterial', params, function(res) {
    var images = res['msg']['item'];
    var totalCount = res['msg']['total_count'];
    $($('#materialImageBox').find('.totalPage')[0]).text(Math.ceil(totalCount / 10));
    for (var i = 0; i < images.length; i++) {
      var image = images[i];
      var url = image['url'];
      var mediaId = image['media_id'];
      var name = image['name'];
      var ori_url = image['ori_url'];
      var newImgItem = $(IMG_ITEM);
      newImgItem.attr('mediaId', mediaId);
      newImgItem.attr('ori_url', ori_url);
      $(newImgItem.find('img')[0]).attr('src', url);
      newImgItem.children('.imageName').html(name);
      box.append(newImgItem);
    }
    box.children('.loadingElement').remove();
  }); 
}

var updateMaterialNewsBox = function(offset, count, callback) {
  // return false;
  console.log('update news material: (', offset, ', ', count, ')');
  var params = {'type' : 'news', 'count' : count, 'offset' : offset};
  var box = $('#materialNewsBox .materialBoxContent');
  box.html(LOADING_ELEMENT);
  post('/wechat/getMaterial', params, function(res) {
    var items = res['msg']['item']
    var totalCount = res['msg']['total_count'];
    $($('#materialNewsBox').find('.totalPage')[0]).text(Math.ceil(totalCount / 2));
    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      var mediaId = item['media_id'];
      var newsItems = item['content']['news_item'];
      var newsWrapper = $(NEWS_WRAPPER);
      newsWrapper.attr('mediaId', mediaId);
      for (var j = 0; j < newsItems.length; j++) {
        var newsItem = newsItems[j];
        var title = newsItem['title'];
        var desc = newsItem['digest'];
        var url = newsItem['url'];
        var thumbUrl = newsItem['thumb_url'];
        var mediaId = newsItem['thumb_media_id'];
        var img = newsItem['img']
        var newsBox = $(NEWS_BOX);
        newsBox.children('.newsItemTitle').text(title);
        newsBox.children('.newsItemImg').css('backgroundImage', 'url(' + img + ')');
        newsBox.attr('thumbUrl', thumbUrl);
        newsBox.attr('description', desc);
        newsBox.attr('url', url);
        newsBox.attr('mediaId', mediaId);
        newsWrapper.append(newsBox);
      }
      box.append(newsWrapper);
    }
    box.children('.loadingElement').remove();
  });
}

var updateMaterialMpNewsBox = function(offset, count, callback) {
  // return false;
  console.log('update mpNews material: (', offset, ', ', count, ')');
  var params = {'type' : 'news', 'count' : count, 'offset' : offset};
  var box = $('#materialMpNewsBox .materialBoxContent');
  box.html(LOADING_ELEMENT);
  post('/wechat/getMaterial', params, function(res) {
    var items = res['msg']['item']
    var totalCount = res['msg']['total_count'];
    $($('#materialMpNewsBox').find('.totalPage')[0]).text(Math.ceil(totalCount / 5));
    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      var newsItems = item['content']['news_item'];
      // var createTime = formatDate(new Date(item['update_time']));
      for (var j = 0; j < newsItems.length; j++) {
        var newsItem = newsItems[j];
        var title = newsItem['title'];
        var url = newsItem['url'];
        var mpNews = $(MPNEWS_ITEM);
        mpNews.children('.mpNewsName').text(title);
        mpNews.children('.mpNewsCreateTime').text('');
        mpNews.attr('url', url);
        box.append(mpNews);
      }
    }
    box.children('.loadingElement').remove();
  });
}

// 更新语音素材框中的语音
var updateMaterialVoiceBox = function(offset, count, callback) {
  // return false;
  console.log('update voice material: (', offset, ', ', count, ')');
  var params = {'type' : 'voice', 'count' : count, 'offset' : offset};
  var box = $('#materialVoiceBox .materialBoxContent');
  box.html(LOADING_ELEMENT);
  post('/wechat/getMaterial', params, function(res) {
    var voices = res['msg']['item'];
    var totalCount = res['msg']['total_count'];
    $($('#materialVoiceBox').find('.totalPage')[0]).text(Math.ceil(totalCount / 5));
    for (var i = 0; i < voices.length; i++) {
      var voice = voices[i];
      var name = voice['name'];
      var mediaId = voice['media_id'];
      var len = voice['length'];
      newVoiceItem = $(VOICE_ITEM);
      newVoiceItem.children('.voiceName').text(name);
      newVoiceItem.children('.voiceLen').text(len);
      newVoiceItem.attr('mediaId', mediaId);
      box.append(newVoiceItem);
    }
    box.children('.loadingElement').remove();
  });
}

// 更新视频素材库中的视频
var updateMaterialVideoBox = function(offset, count, callback) {
  // return false;
  console.log('update video material: (', offset, ', ', count, ')');
  var params = {'type' : 'video', 'count' : count, 'offet' : offset};
  var box = $('#materialVideoBox .materialBoxContent');
  box.html(LOADING_ELEMENT);
  post('/wechat/getMaterial', params, function(res) {
    var videos = res['msg']['item'];
    var totalCount = res['msg']['total_count'];
    $($('#materialVoiceBox').find('.totalPage')[0]).text(Math.ceil(totalCount / 5));
    for (var i = 0; i < videos.length; i++) {
      var video = videos[i];
      var name = video['name'];
      var mediaId = video['media_id'];
      var desc = video['description'];
      newVideo = $(VIDEO_ITEM);
      newVideo.children('.videoName').text(name);
      newVideo.attr('mediaId', mediaId);
      newVideo.children('.videoDesc').text(desc);
      newVideo.children('.videoTitle').text(video['title']);
      box.append(newVideo);
    }
    box.children('.loadingElement').remove();
  });
}

// 显示素材框
// 传入要显示的素材框的类型（首字母大写）
// 传入点击保存时的处理函数
var showMaterialBox = function(type, handler) {
  SAVE_HANDLER = handler;
  $('.materialBox.active').removeClass('active');
  var box = $('#material' + type + 'Box');
  var content = $(box.find('.materialBoxContent')[0]);
  if (content.find('*').length <= 0) {
    if (type == 'Image') {
      updateMaterialImageBox(0, 10);
    } else if (type == 'Voice') {
      updateMaterialVoiceBox(0, 5);
    } else if (type == 'Video') {
      updateMaterialVideoBox(0, 5);
    } else if (type == 'News') {
      updateMaterialNewsBox(0, 2);
    } else if (type == 'MpNews') {
      updateMaterialMpNewsBox(0, 5);
    }
  }
  box.addClass('active');
  $('#materialBoxWrapper').fadeIn();
}

// 隐藏素材框
var hideMaterialBoxAction = function() {
  $('.hideMaterialBoxBtn').click(function() {
  	$('#materialBoxWrapper').fadeOut();
  });
  $('#cancelBtn').click(function() {
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

var chooseNewsAction = function() {
  $(document).delegate('.newsItemWrapper', 'click', function() {
    var oldChoosenNews = $('.newsItemWrapper.choosen');
    var choosenFlag = $(oldChoosenNews.find('.choosenFlag')[0]);
    var height = $(this).height() + 2 * parseFloat($(this).css('padding'));
    if (oldChoosenNews.length > 0) {
      oldChoosenNews.removeClass('choosen');
    } else {
      choosenFlag = $('<div class="choosenFlag vertical_outer"><span class="vertical_inner glyphicon glyphicon-ok"></span></div>');
    }
    choosenFlag.css('height', height + 'px');
    $(this).append(choosenFlag);
    $(this).addClass('choosen');
    $($('#materialNewsBox').find('.choosenAmount')[0]).text('1');
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

var deleteNewsAction = function() {
  $(document).delegate('#deleteNewsMaterialBtn', 'click', function() {
    $($(this).siblings('.newsItemWrapper')[0]).remove();
    $('#materialNews').hide();
    $('#chooseNewsBtn').show();
  });
}

// 删除已选语音
var deleteVoiceAction = function() {
  $(document).delegate('#deleteVoiceMaterialBtn', 'click', function() {
    $('input[name="voiceSelect"]:checked').removeAttr('checked');
    $('#materialVoice').hide();
    $('#materialVoice').attr('mediaId', 'undefined');
    $('#materialVoiceWrapper .showMaterialBoxBtn').show();
  });
}

// 删除已选视频
var deleteVideoAction = function() {
  $(document).delegate('#deleteVideoMaterialBtn', 'click', function() {
    $('input[name="videoSelect"]:checked').removeAttr('checked');
    $('#materialVideo').hide();
    $('#materialVideo').attr('mediaId', 'undefined');
    $('#materialVideoWrapper .showMaterialBoxBtn').show();
  });
}

var showFace = function() {
  $('#materialTextHintArea .showFaceBtn').click(function() {
    $('#faceTable2').fadeIn();
    return false;
  });
  $(window).click(function() {
    $('#faceTable2').fadeOut();
  });
}

var chooseFace = function() {
  $('#faceTable2 tr td').click(function() {
    var face = $(this).children('img');
    var materialText = $('#materialTextInputArea');
    var insertFaceStr = '<img src="' + face.attr('src') + '" name="' + face.attr('name') + '" class="insertedFace" />';
    insertIntoCaret('materialTextInputArea', insertFaceStr);
    updateRemainChar();
    return false;
  });
}

var remainCharAmount = function() {
  var materialText = $('#materialTextInputArea');
  materialText.keydown(function(evt) {
    if ($(materialText).text() == '') {
      $(materialText).html('');
    }
    if (evt.keyCode == '13') {
      if ($(materialText).html().indexOf('<div>') != 0) {
        var content = $(materialText).html();
        $(materialText).html('');
        insertIntoCaret('materialTextInputArea', ('<div>' + content + '</div>'));
      }
    }
  });
  if (materialText[0].addEventListener) {
    materialText[0].addEventListener('DOMCharacterDataModified', function(evt) {
      updateRemainChar();
    }, false);
  }
}

// 更新可输入字符数
var updateRemainChar = function() {
  var materialText = $('#materialTextInputArea');
  var remainText = $('#materialTextHintArea .remainChar font');
  var charAmount = materialText.text().length;
  var faceAmount = materialText.find('.insertedFace').length;
  var maxAmount = parseInt(TO_INSERT_ROW.attr('maxCharAmount'));
  var remainAmount = maxAmount - charAmount - faceAmount;
  remainText.text(remainAmount);
  return remainAmount;
}

// 点击素材框中的保存按钮时，根据当前素材框显示的信息类别不同，选择不同的handler来提取素材狂内容并隐藏素材狂
var saveAction = function() {
  $('#choosenBtn').click(function() {
  	return SAVE_HANDLER();
  });
}

String.format = function() {
    if (arguments.length == 0)
        return null;
    var str = arguments[0];
    for ( var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
};

/* 
 *  方法:Array.remove(dx) 
 *  功能:根据元素位置值删除数组元素. 
 *  参数:元素值 
 *  返回:在原数组上修改数组 
 *  作者：pxp 
 */  
Array.prototype.remove = function (dx) {  
    if (isNaN(dx) || dx > this.length) {  
        return false;  
    }  
    for (var i = 0, n = 0; i < this.length; i++) {  
        if (this[i] != this[dx]) {  
            this[n++] = this[i];  
        }  
    }  
    this.length -= 1;  
};

var formatDate = function(now)   {     
  var   year=now.getYear();     
  var   month=now.getMonth()+1;     
  var   date=now.getDate();     
  var   hour=now.getHours();     
  var   minute=now.getMinutes();     
  var   second=now.getSeconds();     
  return   year+"-"+month+"-"+date+"   "+hour+":"+minute+":"+second;     
}   