$(document).ready(function() {
  uploadImage();
  previewAction();
  submitAction();
});

var previewAction = function() {
  $('#refreshPreviewBtn').click(function() {
    var res = getParams();
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
    res = getParams()
    if (!res[0]) {
      topAlert(res[1], 'error');
      return false;
    }
    post('/transmit/save', res[1], function(msg) {
      console.log(msg);
    });
  });
}

var getParams = function() {
  var params = {}
  params['bg'] = $('input[name="bg"]').val();
  params['head_diameter'] = $('input[name="head_diameter"]').val();
  params['head_x'] = $('input[name="head_x"]').val();
  params['head_y'] = $('input[name="head_y"]').val();
  params['name_fontsize'] = $('input[name="name_fontsize"]').val();
  params['name_size'] = $('input[name="name_len"]').val();
  params['name_x'] = $('input[name="name_x"]').val();
  params['name_y'] = $('input[name="name_y"]').val();
  params['qrcode_size'] = $('input[name="qrcode_size"]').val();
  params['qrcode_x'] = $('input[name="qrcode_x"]').val();
  params['qrcode_y'] = $('input[name="qrcode_y"]').val();
  if (params['bg'].length <= 0 || params['bg'] == undefined) {
    return [false, '未提供背景图片'];
  }
  if (params['head_diameter'] == undefined || params['head_x'] == undefined || params['head_y'] == undefined ||
     params['name_fontsize'] == undefined || params['name_size'] == undefined || params['name_x'] == undefined || params['name_y'] == undefined ||
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