$(document).ready(function() {
  uploadImage();
  previewAction();
  submitAction();
  msgOptionAction();
});

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
  $('.msgOption').each(function() {
    var val = $(this).attr('value');
    val = text2html(val);
    $(this).attr('value', val);
  })
  $('.msgOption[name="invited_msg"]').trigger('click');
}

var previewAction = function() {
  $('#refreshPreviewBtn').click(function() {
    var res = getStyleParams();
    if (!res[0]) {
      topAlert(res[1], 'error');
      return false;
    }
    post('/transmit/getNameCard', res[1], function(msg) {
      $('.previewBox img').attr('src', msg['msg']);
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
    params['invited_msg'] = html2text($('.msgOption[name="invited_msg"]').attr('value'));
    params['goal_msg'] = html2text($('.msgOption[name="goal_msg"]').attr('value'));
    topAlert('正在保存中...');
    post('/transmit/save', params, function(msg) {
      if (msg['code'] == 0) {
        topAlert('保存成功！');
      } else {
        topAlert(msg['msg'], 'error');
      }
    });
  });
}

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