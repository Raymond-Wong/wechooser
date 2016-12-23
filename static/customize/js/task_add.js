$(document).ready(function() {
  chooseTime();
  chooseNews();
  chooseTemplate();
  saveTaskAction();
});

var chooseTemplate = function() {
  $('#template_list').change(function() {
    var template_id = $(this).val();
    var option = $(this).children('option[value="' + template_id + '"]');
    var keywords = option.attr('keywords');
    var keywordsBox = $('.keywordsBox');
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

var saveTaskAction = function() {
  $('#submit').click(function() {
    topAlert('正在提交任务...');
    var task_name = $('input[name="task_name"]').val();
    var run_time = $('input[name="run_time"]').datetimepicker('getValue');
    var url = $('input[name="url"]').val();
    var template_id = $('#template_list').val();
    var template_name = $('option[value="' + template_id + '"]').text();
    var params = {'action' : 'add'};
    if (task_name != undefined && task_name.length > 0 && task_name.length < 30) {
      params['task_name'] = task_name;
    } else {topAlert('请填写任务名称', 'error'); return false}
    if (run_time != undefined) {
      params['run_time'] = run_time.Format("yyyy-MM-dd hh:mm");
    } else {topAlert('请选择发送时间', 'error'); return false}
    if (url != undefined && url.length > 0) {
      params['url'] = url;
    } else {topAlert('请选择图文消息', 'error'); return false}
    params['keywords'] = {}
    $($('.keywordsBox').find('input')).each(function() {
      var keyword = $(this).attr('name');
      var value = $(this).val();
      if (value == null || value == undefined || value.length <= 0) {
        topAlert('请填写模板关键词（' + keyword + '）', 'error');
        return false;
      }
      params['keywords'][keyword] = {'value' : value, 'color' : '#b2b2b2'};
    });
    params['keywords'] = JSON.stringify(params['keywords']);
    params['template_id'] = template_id;
    if (params['template_id'] == 'none') {
      topAlert('请选择消息模板', 'error');
      return false;
    }
    params['template_name'] = template_name;
    post('/task/add', params, function(resp) {
      if (resp['code'] == 0) {
        topAlert(resp['msg']);
      } else {
        topAlert(resp['msg'], 'error');
      }
    });
  });
}

var chooseTime = function() {
  var diff = 15;
  var now = new Date();
  var minute = now.getMinutes();
  if (minute % diff == 0) {
    now.setMinutes(parseInt(minute / diff) * diff);
  } else {
    now.setMinutes((parseInt(minute / diff) + 1) * diff);
  }
  $('input[name="run_time"').datetimepicker({
    step: diff,
    format: "Y-m-d H:i",
    value: now,
  });
}

var chooseNews = function() {
  $('#chooseNewsBtn').click(function() {
    showMaterialBox('News', function() {
      var choosenNews = $('.newsItemWrapper.choosen').clone();
      var url = choosenNews.children('.newsItemBox').attr('url');
      $('input[name="url"]').val(url);
      $($('.newsItemWrapper.choosen').find('.choosenFlag')[0]).remove()
      $('.newsItemWrapper.choosen').removeClass('choosen');
      $(choosenNews.find('.choosenFlag')[0]).remove();
      choosenNews.removeClass('choosen');
      $('#materialBoxWrapper').fadeOut();
    });
  });
}