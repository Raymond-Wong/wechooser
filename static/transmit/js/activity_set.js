var AID = undefined;
$(document).ready(function() {
  getAid();
  uploadImage();
  previewAction();
  submitAction();
  msgOptionAction();
  initGainCardMethod();
  chooseNews();
  chooseTemplate();
  toggleAchieveMsgBox();
  listenAchieveMsgHead();
  removeAchieveMsg();
  addAchieveMsg();
  achieveMsgRemovable();
  achieveMsgDraggable();
  // initInvitedReply()
});

var getAid = function() {
  // 获取当前页面的活动
  AID = $('.pageWrapper').attr('aid');
  $('.pageWrapper').removeAttr('aid');
}

var initGainCardMethod = function() {
  var gcmBox = $('.gainCardMethodBox');
  var type = gcmBox.attr('type');
  var kw = gcmBox.attr('keyword');
  var mid = gcmBox.attr('mid');
  gcmBox.removeAttr('type').removeAttr('keyword').removeAttr('mid');
  if (type == '1' || type == '0') {
    $('input[name="gainCardMethod"][value="' + type + '"]').trigger('click');
  } else if (type == '2') {
    $('input[name="gainCardMethod"][value="2"][mid="' + mid + '"]').trigger('click');
  } else {
    // $('input[name="gainCardMethod"][value="3"]').trigger('click');
    $('input[name="gainCardKw"]').val(kw);
  }
}

var msgOptionAction = function() {
  $('.msgOption').click(function() {
    // 保存当前textbox中的内容
    var content = $('#materialText').html();
    $('.msgOption.active').attr('value', content);
    $('.msgOption.active').removeClass('active');
    // 初始化textbox中的内容
    $('#materialText').html($(this).attr('value'));
    $(this).addClass('active');
  });
  // 将数据库中的文字信息转换成可直接设置为html的文字信息
  $('.msgOption[name="invited_msg"]').each(function() {
    var val = $(this).attr('value');
    val = text2html(val);
    $(this).attr('value', val);
  })
  $('.msgOption[name="invited_msg"]').trigger('click');
}

var previewAction = function() {
  var loading = $('.previewLoad');
  $('#refreshPreviewBtn').click(function() {
    loading.show();
    var res = getStyleParams();
    if (!res[0]) {
      topAlert(res[1], 'error');
      loading.hide();
      return false;
    }
    post('/transmit/getNameCard', res[1], function(msg) {
      $('.previewBox img').attr('src', msg['msg']);
      loading.hide();
    });
  });
  $('#refreshPreviewBtn').trigger('click');
}

var submitAction = function() {
  $('#submit').click(function() {
    res = getStyleParams()
    if (!res[0]) {
      topAlert(res[1], 'error');
      return false;
    }
    var params = res[1];
    params['target'] = $('input[name="target"]').val();
    if (params['target'] <= 0 || params['target'] == undefined) {
      topAlert('未申明达标数量', 'error');
      return false;
    }
    var content = $('#materialText').html();
    $('.msgOption.active').attr('value', content);
    params['gain_card_method'] = 3;//$('input[name="gainCardMethod"]:checked').val();
    params['name'] = $('input[name="activity_name"]').val();
    if (params['name'].length <= 0 || params['name'].length > 30) {
      topAlert('活动名称不合法，名称长度需大于0小于等于30！', 'error');
      return false;
    }
    if (params['gain_card_method'] == '2') {
      params['mid'] = $('input[name="gainCardMethod"]:checked').attr('mid');
    } else if (params['gain_card_method'] == '3') {
      params['keyword'] = $('input[name="gainCardKw"]').val();
      if (params['keyword'] == '') {
        topAlert('请输入获取名片的关键词', 'error');
        return false;
      }
    }
    params['achieveMsg'] = getAchieveMsg();
    if (!params['achieveMsg'][0]) {
      topAlert(params['achieveMsg'][1], 'error');
      return false;
    } else {
      params['achieveMsg'] = JSON.stringify(params['achieveMsg'][1])
    }
    params['invited_msg'] = get_invited_msg();
    if (params['invited_msg'] == false) {
      return false;
    } else {
      params['invited_msg'] = JSON.stringify(params['invited_msg']);
    }
    params['invite_msg'] = $('#invite_msg').val();
    if (params['invite_msg'] == '') {
      topAlert('成功邀请通知（发送邀请用户）不合法', 'error');
      return false;
    }
    topAlert('正在保存中...');
    url = '/transmit/activity/save' + ((AID == undefined || AID == '') ? '' : ('?aid=' + AID))
    post(url, params, function(msg) {
      if (msg['code'] == 0) {
        var resp = $.parseJSON(msg['msg']);
        if (resp['action'] == 'add') {
          topAlert('保存成功，页面即将自动跳转...');
          setTimeout(function() {
            window.location.href = "/transmit/activity/list"
          }, 2000);
        } else {
          topAlert('保存成功!');
        }
      } else {
        topAlert(msg['msg'], 'error');
      }
    });
  });
}

var getAchieveMsg = function() {
  var ret = [];
  var flag = true;
  var err_msg = '';
  $('.achieveMsgBox').each(function() {
    if (!flag) return false;
    var box = {};
    box['id'] = $(this).attr('mid');
    box['run_time'] = $($(this).find('input[name="run_time"]')[0]).val();
    // if (parseInt(box['run_time']) % 15 != 0) {
    //   flag = false;
    //   err_msg = '延迟发送时间必须为15分钟的整数倍！'
    // }
    box['url'] = $($(this).find('input[name="url"]')[0]).val();
    if (box['url'].length == 0) {
      flag = false;
      err_msg = '回复消息必须选择对应的图文链接！';
    }
    box['task_name'] = $($(this).find('input[name="task_name"]')[0]).val();
    if (box['task_name'].length <= 0 || box['task_name'] > 30) {
      flag = false;
      err_msg = '消息名称不得超过30字且不能为空！'
    }
    box['template_id'] = $($(this).find('.template_list')[0]).val();
    box['template_name'] = $($(this).find('option[value="' + box['template_id'] + '"]')[0]).text();
    if (box['template_id'] == 'none' || box['template_name'] == '未选择') {
      flag = false;
      err_msg = '回复消息必须选择一个模板！';
    }
    box['keywords'] = {};
    $($(this).find('.keywordsBox')[0]).find('input').each(function() {
      if (!flag) return false;
      var keyword = $(this).attr('name');
      var value = $(this).val();
      if (value.length == 0) {
        flag = false;
        err_msg = '关键词（' + keyword + '）的值不可为空！';
      }
      box['keywords'][keyword] = {'value' : value, 'color' : '#b2b2b2'};
    });
    box['news_item'] = {}
    box['news_item']['title'] = $($(this).find('input[name="news_title"]')[0]).val();
    box['news_item']['description'] = $($(this).find('.news_desc')[0]).val();
    box['news_item']['picurl'] = $($(this).find('input[name="news_pic_url"]')[0]).val();
    if (box['news_item']['title'] == undefined || box['news_item']['title'].length <= 0) {
      flag = false;
      err_msg = '图文消息标题不合法';
    }
    if (box['news_item']['description'] == undefined || box['news_item']['description'].length <= 0) {
      flag = false;
      err_msg = '图文消息描述不合法';
    }
    if (box['news_item']['picurl'] == undefined || box['news_item']['picurl'].length <= 0) {
      flag = false;
      err_msg = '图文消息封面不合法';
    }
    ret.push(box);
  });
  if (ret.length == 0) {
    flag = false;
    err_msg = '至少要有一条达成目标后回复的模板消息！';
  }
  if (!flag) {
    return [flag, err_msg]
  }
  return [flag, ret];
};

var getStyleParams = function() {
  var params = {}
  params['bg'] = $('input[name="bg"]').val();
  params['head_diameter'] = $('input[name="head_diameter"]').val();
  params['head_x'] = $('input[name="head_x"]').val();
  params['head_y'] = $('input[name="head_y"]').val();
  params['name_fontsize'] = $('input[name="name_fontsize"]').val();
  params['name_y'] = $('input[name="name_y"]').val();
  params['qrcode_size'] = $('input[name="qrcode_size"]').val();
  params['qrcode_x'] = $('input[name="qrcode_x"]').val();
  params['qrcode_y'] = $('input[name="qrcode_y"]').val();
  if (params['bg'].length <= 0 || params['bg'] == undefined) {
    return [false, '未提供背景图片'];
  }
  if (params['head_diameter'] == undefined || params['head_x'] == undefined || params['head_y'] == undefined ||
     params['name_fontsize'] == undefined || params['name_y'] == undefined ||
     params['qrcode_size'] == undefined || params['qrcode_x'] == undefined || params['qrcode_y'] == undefined) {
    return [false, '为提供足够参数'];
  }
  return [true, params]
}

var uploadImage = function() {
  var inputStr = '<input type="file" name="image" multiple="multiple" accept="image/*" class="hide" />';
  $(document).delegate('.uploadImgBtn', 'click', function() {
    var inputDom = $(inputStr);
    $('body').append(inputDom);
    autoUpload(inputDom, $(this));
  });
}

var autoUpload = function(dom, btn) {
  dom.trigger('click');
  var url = '/upload';
  dom.fileupload({
    autoUpload: true,//是否自动上传
    url: url,//上传地址
    sequentialUploads: true,
    add: function (e, data) {
      btn.removeClass('uploadImgBtn');
      btn.text('正在上传中...');
      data.submit();
    },
    done: function (e, resp) {
      resp = resp['result'];
      if (resp['code'] != 0) {
        topAlert(resp['msg'], 'error');
      } else {
        $('#' + btn.attr('target')).val(resp['msg']);
      }
      btn.addClass('uploadImgBtn');
      btn.text('点击上传');
      $(this).remove();
    },
  });
}

var text2html = function(text) {
  var content = str2face(text);
  var start = content.indexOf('\n');
  var end = content.indexOf('\n', start + 1);
  var lines = [];
  if (start < 0) {
    lines.push(content);
  } else {
    lines.push('<div>' + content.substring(0, start) + '</div>');
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
  return lines.join('')
}

var html2text = function(html) {
  var tmpDiv = $('<div></div>');
  tmpDiv.html(html);
  // 在每个div前面加一个换行符
  var counter = 0;
  tmpDiv.find('div').each(function() {
    var brOrTextOrImg = $(this).text().length;
    brOrTextOrImg += $(this).find('br').length;
    brOrTextOrImg += $(this).find('img').length;
    if (counter++ > 0 && brOrTextOrImg > 0)
      $(this).prepend('\n');
  })
  tmpDiv.find('img').each(function() {
    var face = $(this).attr('name');
    $(this).before(face);
    $(this).remove();
  });
  return tmpDiv.text()
}

var chooseTemplate = function(dom) {
  $(document).delegate('.template_list', 'change', function() {
    var template_id = $(this).val();
    var option = $(this).children('option[value="' + template_id + '"]');
    var keywords = option.attr('keywords');
    var keywordsBox = $($(this).parents('.achieveMsg')[0]).children('.keywordsBox');
    keywordsBox.html("");
    if (keywords == undefined || keywords.length <= 0) {
      return false;
    }
    keywords = $.parseJSON(keywords);
    for (var i = 0; i < keywords.length; i++) {
      var keyword = keywords[i];
      var kwDom = $(KEYWORD_LINE);
      kwDom.children('.lineLabel').text(keyword);
      kwDom.children('.lineInput').children('input').attr('name', keyword);
      keywordsBox.append(kwDom);
    }
  });
}

var chooseNews = function() {
  $(document).delegate('.chooseNewsBtn', 'click', function() {
    var that = $(this);
    showMaterialBox('News', function() {
      var choosenNews = $('.newsItemWrapper.choosen').clone();
      var url = choosenNews.children('.newsItemBox').attr('url');
      var news_title = choosenNews.children('.newsItemBox').children('.newsItemTitle').text();
      var news_desc = choosenNews.children('.newsItemBox').attr('description');
      var news_pic_url = choosenNews.children('.newsItemBox').attr('thumburl');
      that.parent().children('.lineInput').children('input').val(url);
      var achieveMsgBox = $(that.parents('.achieveMsgBox')[0]);
      achieveMsgBox.find('input[name="news_title"]').val(news_title);
      achieveMsgBox.find('.news_desc').text(news_desc);
      achieveMsgBox.find('input[name="news_pic_url"]').val(news_pic_url);
      $($('.newsItemWrapper.choosen').find('.choosenFlag')[0]).remove()
      $('.newsItemWrapper.choosen').removeClass('choosen');
      $(choosenNews.find('.choosenFlag')[0]).remove();
      choosenNews.removeClass('choosen');
      $('#materialBoxWrapper').fadeOut();
    });
  });
}

var toggleAchieveMsgBox = function() {
  $(document).delegate('.achieveMsgHead', 'click', function() {
    $(this).parent().children('.achieveMsg').slideToggle();
  });
}

var listenAchieveMsgHead = function() {
  $(document).delegate('input[name="task_name"]', 'change', function() {
    var name = $(this).val();
    if (name.length > 30) {
      name = name.substring(0, 30);
    }
    $(this).val(name);
    $($($(this).parents('.achieveMsgBox')[0]).find('.achieveMsgHeadText')[0]).text(name);
  });
}

var removeAchieveMsg = function() {
  $(document).delegate('.achieveMsgBtn.removeBtn', 'click', function() {
    var msgBox = $($(this).parents('.achieveMsgBox')[0]);
    var msgBoxName = $(msgBox.find('.achieveMsgHeadText')[0]).text();
    if (!confirm('确定删除回复消息（' + msgBoxName + '）吗？')) return false;
    msgBox.remove();
    return false;
  });
}

var addAchieveMsg = function() {
  $(document).delegate('.achieveMsgBtn.addBtn', 'click', function() {
    var msgBox = $($(this).parents('.achieveMsgBox')[0]);
    var newMsgBox = msgBox.clone();
    newMsgBox.removeAttr('mid');
    $(newMsgBox.find('.achieveMsgHeadText')[0]).text('回复消息');
    $(newMsgBox.find('input[name="task_name"]')[0]).val('');
    $(newMsgBox.find('input[name="run_time"]')[0]).val('');
    $(newMsgBox.find('input[name="url"]')[0]).val('');
    $(newMsgBox.find('.template_list')[0]).val('none');
    $(newMsgBox.find('.keywordsBox')[0]).html('');
    $(newMsgBox.find('.template_list')[0]).val('none');
    $(newMsgBox.find('input[name="news_title"]')[0]).val('');
    $(newMsgBox.find('.news_desc')[0]).text('');
    $(newMsgBox.find('input[name="news_pic_url"]')[0]).val('');
    $(newMsgBox.find('.achieveMsg')[0]).show();
    msgBox.after(newMsgBox);
    achieveMsgDraggable(newMsgBox);
    achieveMsgRemovable();
    return false;
  });
};

var achieveMsgRemovable = function() {
  $('.removeBtn').show();
  $($($('.achieveMsgBox')[0]).find('.removeBtn')[0]).hide();
}

var achieveMsgDraggable = function(dom) {
  if (dom == undefined) {
    dom = $('.achieveMsgBox');
  }
  var startTop = 0;
  dom.draggable({
    containment:'#achieveMsgWrapper',
    scroll:true,
    cursor:'move',
    start: function() {
      $(this).css('z-index', '100');
      startTop = $(this).offset().top;
    },
    stop: function() {
      var that = $(this);
      var moveDomTop = that.offset().top;
      var moveDomBottom = moveDomTop + that.height();
      // 如果位移在10个像素点内则认为没有位移
      if (Math.abs(moveDomTop - startTop) > 10) {
        var flag = false;
        var newThat = that.clone();
        $(newThat.find('.template_list')[0]).val($(that.find('.template_list')[0]).val());
        achieveMsgDraggable(newThat);
        var achieveMsgBox = $('.achieveMsgBox');
        var moveDomStandard = moveDomTop;
        // 如果是向上位移
        if (moveDomTop > startTop) {
          achieveMsgBox = $.makeArray(achieveMsgBox);
          achieveMsgBox.reverse();
          achieveMsgBox = $(achieveMsgBox);
          moveDomStandard = moveDomBottom;
        } 
        achieveMsgBox.each(function() {
          if (flag) return false;
          var domTop = $(this).offset().top;
          var domHeight = $(this).height();
          if (moveDomStandard < (domTop + domHeight / 2)) {
            $(this).before(newThat);
            that.remove();
            flag = true;
          } else if (moveDomStandard >= (domTop + domHeight / 2) && moveDomStandard < (domTop + domHeight)) {
            $(this).after(newThat);
            that.remove();
            flag = true;
          }
        });
      }
      var target = (newThat == undefined ? that : newThat);
      target.css('z-index', '1');
      target.css('top', '0');
      target.css('left', '0');
      achieveMsgRemovable();
    }
  });
}

var initInvitedReply = function() {
  var templateStr = $('#invited_msg').attr('template');
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
      lines.push('<div>' + content.substring(0, start) + '</div>');
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
  } else if (template['MsgType'] == 'news') {
    var box = $('#materialNews');
    var mediaId = template['MediaId'];
    var newsWrapper = $(NEWS_WRAPPER);
    var newsItems = template['Items'];
    newsWrapper.attr('mediaId', mediaId);
    for (var j = 0; j < newsItems.length; j++) {
      var newsItem = newsItems[j];
      var title = newsItem['Title'];
      var desc = newsItem['Description'];
      var url = newsItem['Url'];
      var thumbUrl = newsItem['PicUrl'];
      var mediaId = newsItem['MediaId'];
      var img = newsItem['ImageUrl']
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
    $('#chooseNewsBtn').hide();
    box.show();
  }
}

var get_invited_msg = function() {
  var rule = $('.ruleDetailWrapper');
  // 获取所有回复
  var handlers = {
    'text' : textHandler,
    'image' : imageHandler,
    'voice' : voiceHandler,
    'video' : videoHandler,
    'news' : newsHandler,
  }
  var replys = [];
  $(rule.find('.reply')).each(function() {
    var type = $(this).attr('type');
    replys.push(handlers[type]($(this)));
  });
  if (replys.length <= 0) {
    topAlert('回复内容不可为空', 'error');
    return false;
  }
  var replyAll = rule.attr('replyAll');
  if (replyAll == '') {
    replyAll = "True";
  }
  replyAll = replyAll == undefined ? 'False' : replyAll;
  params = {'replys' : replys, 'replyAll' : replyAll}
  return params
}