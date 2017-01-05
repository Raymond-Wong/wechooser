$(document).ready(function() {
  chooseNews();
  chooseTemplate();
  saveTaskAction();
  addTaskAction();
  removeTaskAction();
});

var removeTaskAction = function() {
  $(document).delegate('.removeTaskBtn', 'click', function() {
    $($(this).parents('.subTaskBox')[0]).remove();
  });
}

var addTaskAction = function() {
  initTime($('input[name="run_time"]'));
  var btn = $('.addTaskBtn');
  btn.click(function() {
    if ($('.subTaskBox').length >= 10) {
      topAlert('最多添加十个子任务！', 'error');
      return false;
    }
    var that = $(this);
    var taskList = $(that.parents('.borderBox')[0]).children('.taskList');
    var newTaskBox = $(SUB_TASK_BOX);
    taskList.append(newTaskBox);
    initTime($(newTaskBox.find('input[name="run_time"]')[0]));
  });
}

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
    var taskList = {};
    var taskAmount = 0;
    var taskValide = true;
    $('.subTaskBox').each(function() {
      var taskName = $($(this).find('input[name="task_name"]')[0]).val();
      if (taskName.length == 0) {
        taskValide = false;
        return false;
      }
      var run_time = $($(this).find('input[name="run_time"]')[0]).datetimepicker('getValue').Format('yyyy-MM-dd hh:mm');
      if (!(taskName in taskList)) {
        taskAmount++;
      }
      taskList[taskName] = run_time;
    });
    var url = $('input[name="url"]').val();
    var template_id = $('#template_list').val();
    var template_name = $('option[value="' + template_id + '"]').text();
    var params = {'action' : 'add'};
    if (!taskValide) {
      topAlert('所有子任务名称都必填！', 'error');
      return false;
    }
    if (taskList != undefined && taskAmount > 0 && taskAmount <= 10) {
      params['task_list'] = JSON.stringify(taskList);
    } else {topAlert('请至少添加一个子任务，且子任务数量不得超过10', 'error'); return false}
    if (url != undefined && url.length > 0) {
      params['url'] = url;
    } else {topAlert('请选择图文消息', 'error'); return false}
    params['keywords'] = {}
    $($('.keywordsBox').find('input')).each(function() {
      var keyword = $(this).attr('name');
      var value = $(this).val();
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

var initTime = function(dom) {
  var diff = 15;
  var now = new Date();
  var minute = now.getMinutes();
  if (minute % diff == 0) {
    now.setMinutes(parseInt(minute / diff) * diff);
  } else {
    now.setMinutes((parseInt(minute / diff) + 1) * diff);
  }
  dom.datetimepicker({
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