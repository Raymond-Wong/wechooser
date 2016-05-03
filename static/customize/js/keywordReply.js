$(document).ready(function() {
  bindSaveRuleAction();
});

var parseFace = function(domEle) {
  var tmpDiv = domEle.clone();
  tmpDiv.find('img').each(function() {
    var face = $(this).attr('name');
    $(this).before(face);
    $(this).remove();
  });
  return tmpDiv.text();
}

var textHandler = function(box) {
  var params = {'MsgType' : 'text'};
  var content = parseFace(box.children('.val'));
  params['Content'] = content;
  return params;
}

var imageHandler = function(box) {
  var params = {'MsgType' : 'image'};
  var mediaId = box.attr('mediaId');
  params['MediaId'] = mediaId;
  return params;
}

var voiceHandler = function(box) {
  var params = {'MsgType' : 'voice'};
  var mediaId = box.attr('mediaId');
  params['MediaId'] = mediaId;
  return params;
}

var videoHandler = function(box) {
  var params = {'MsgType' : 'video'};
  var mediaId = box.attr('mediaId');
  params['MediaId'] = mediaId;
  params['Title'] = box.children('.val').children('.videoTitle').text();
  params['Name'] = box.children('.val').children('.videoName').text();
  params['Description'] = box.children('.val').children('.videoDesc').text();
  return params;
}

var bindSaveRuleAction = function() {
  $(document).delegate('.saveRuleBtn', 'click', function() {
  	var rule = $(this).parents('.ruleDetailWrapper');
  	// 获取该规则下的所有关键词
  	var keywords = {};
  	$(rule.find('.keyword')).each(function() {
  	  var keyword = parseFace($(this).children('.val'));
  	  var isFullMatch = $(this).attr('fullMatch');
  	  isFullMatch = (isFullMatch == undefined) ? "False" : isFullMatch;
  	  if (keywords[keyword]) {
  	  	topAlert('存在两个相同的关键词，且匹配规则不同', 'error');
  	  	return false;
  	  }
  	  keywords[keyword] = isFullMatch;
  	});
  	if (keywords.length <= 0) {
  	  topAlert('关键词不能为空', 'error');
  	  return false;
  	}
  	// 获取所有回复
  	var handlers = {
  	  'text' : textHandler,
  	  'image' : imageHandler,
  	  'voice' : voiceHandler,
  	  'video' : videoHandler,
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
  	var ruleName = $(rule.find('input[name="ruleName"]')[0]).val();
  	if ($.trim(ruleName) == '') {
  	  topAlert('规则名称不能为空', 'error');
  	  return false;
  	}
  	var replyAll = rule.attr('replyAll');
  	replyAll = replyAll == undefined ? 'False' : replyAll;
  	params = {'keywords' : JSON.stringify(keywords), 'replys' : JSON.stringify(replys), 'name' : ruleName, 'isReplyAll' : replyAll};
  	console.log(params);
  	$.post('/reply?type=keyword', params, function(res) {
  	  if (res['code'] == 0) {
  	  	topAlert('保存成功');
  	  	closeRuleAction($(this));
  	  } else {
  	  	topAlert(res['msg']);
  	  }
  	});
  	// closeRuleAction($(this));
  });
}

var closeRuleAction = function(saveRuleBtn) {
  	var rule = saveRuleBtn.parents('.ruleDetailWrapper');
  	var ruleShort = $(rule.siblings('.ruleShortWrapper')[0]);
  	var name = $(rule.find('input[name="ruleName"]')[0]).val();
  	var textAmount = $(rule.find('.textAmount')[0]).text();
  	var imageAmount = $(rule.find('.imageAmount')[0]).text();
  	var voiceAmount = $(rule.find('.voiceAmount')[0]).text();
  	var videoAmount = $(rule.find('.videoAmount')[0]).text();
  	var newsAmount = $(rule.find('.newsAmount')[0]).text();
  	var totalAmount = parseInt(textAmount) + parseInt(imageAmount);
  	totalAmount += (parseInt(voiceAmount) + parseInt(videoAmount));
  	totalAmount += (parseInt(newsAmount));
  	var keywords = [];
  	$(rule.find('.keyword')).each(function() {
  	  var keyword = $(this).children('.val').html();
  	  keywords.push(keyword);
  	});
  	$(ruleShort.find('.ruleName')[0]).text(name);
  	$(ruleShort.find('.totalAmount')[0]).text(totalAmount);
  	$(ruleShort.find('.textAmount')[0]).text(textAmount);
  	$(ruleShort.find('.imageAmount')[0]).text(imageAmount);
  	$(ruleShort.find('.voiceAmount')[0]).text(voiceAmount);
  	$(ruleShort.find('.videoAmount')[0]).text(videoAmount);
  	$(ruleShort.find('.newsAmount')[0]).text(newsAmount);
  	var keywordsWrapper = $(ruleShort.find('.keywordsWrapper .val')[0]);
  	keywordsWrapper.html('');
  	for (var i = 0; i < keywords.length; i++) {
  	  keywordsWrapper.append('<font>' + keywords[i] + '</font>');
  	}
  	rule.hide();
  	ruleShort.show();
}
