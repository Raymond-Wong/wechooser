$(document).ready(function() {
  bindKeywordAction();
});

var bindKeywordAction = function() {
  bindDetailToggle();
  bindDeleteRowAction();
  bindFullMatchAction();
  bindReplyAllAction();
  bindSaveRuleAction();
  bindDeleteRuleAction();
  showMaterialBoxAction();
}

var bindDetailToggle = function() {
  $(document).delegate('.ruleShortWrapper .head', 'click', function() {
  	var shortBox = $(this).parent();
  	var detailBox = $(shortBox.siblings('.ruleDetailWrapper')[0]);
  	shortBox.hide();
  	detailBox.show();
  });
  $(document).delegate('.ruleDetailWrapper .head', 'click', function() {
  	var detailBox = $(this).parent();
  	var shortBox = $(detailBox.siblings('.ruleShortWrapper')[0]);
  	detailBox.hide();
  	shortBox.show();
  });
}

var bindDeleteRowAction = function() {
  $(document).delegate('.deleteRowBtn', 'click', function() {
  	var type = $(this).attr('type');
  	var row = $(this).parents('.ruleRow');
  	if (type == 'msg') {
  	  var msgType = row.attr('type');
  	  var amountBox = $(row.parents('.ruleDetailWrapper').find('.' + msgType + 'Amount')[0]);
  	  var cAmount = parseInt(amountBox.text());
  	  amountBox.text(cAmount - 1);
  	}
  	row.remove();
  });
}

var bindFullMatchAction = function() {
  $(document).delegate('.fullMatchBtn', 'click', function() {
  	var keyword = $(this).parents('.keyword');
  	var state = keyword.attr('fullMatch');
  	console.log(state);
  	if (state == undefined || state == "False") {
  	  keyword.attr('fullMatch', 'True');
  	  $(this).text('全匹配');
  	} else {
  	  keyword.attr('fullMatch', 'False');
  	  $(this).text("未全匹配");
  	}
  })
}

var bindReplyAllAction = function() {
  $(document).delegate('.replyAllBtn', 'click', function() {
  	var rule = $(this).parents('.ruleDetailWrapper');
  	var state = rule.attr('replyAll');
  	if (state == undefined || state == "False") {
  	  rule.attr('replyAll', 'True');
  	  $(this).text('回复全部');
  	} else {
  	  rule.attr('replyAll', 'False');
  	  $(this).text('未回复全部');
  	}
  });
}

var bindSaveRuleAction= function() {
  $(document).delegate('.saveRuleBtn', 'click', function() {
  	var rule = $(this).parents('.ruleDetailWrapper');
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
  });
}

var bindDeleteRuleAction = function() {
  $(document).delegate('.deleteRuleBtn', 'click', function() {
    var rule = $(this).parents('.ruleWrapper');
    rule.remove();
  });
}

TO_INSERT_ROW = null;

// 当用户在素材框中选择了图片时将图片加到回复中的行为
var saveImage = function() {
  var choosenImage = $('.imageItem.choosen');
  var imgUrl = $(choosenImage.find('img')[0]).attr('src');
  var mediaId = choosenImage.attr('mediaId');
  // 如果进入这个判断，则说明是点击添加按钮，否则是点击编辑按钮
  if (TO_INSERT_ROW == null || TO_INSERT_ROW.attr('role') == 'btnBox') {
    var box = TO_INSERT_ROW.parents('.content');
    var newRow = $(IMG_ROW);
    $(newRow.find('img')[0]).attr('src', imgUrl);
    newRow.attr('mediaId', mediaId);
    box.append(newRow);
    // 在最下面的信息计数中增加一个计数器
    var box = TO_INSERT_ROW.parents('.ruleDetailWrapper');
    var imageAmountBox = $(box.find('.imageAmount')[0]);
    imageAmountBox.text(parseInt(imageAmountBox.text()) + 1);
  } else {
    var box = TO_INSERT_ROW.children('.val');
    box.html('<img src="' + imgUrl + '" />');
  }
  // 把已选择的图片去除选择标记
  choosenImage.removeClass('choosen');
  $(choosenImage.find('.choosenFlag')[0]).remove();
  $('#materialBoxWrapper').fadeOut();
  TO_INSERT_ROW = null;
}

// 当用户在素材框中填写了新文字时将文字加到回复中的行为
var saveText = function() {
  var textContent = $('#materialTextInputArea').html();
  $('#materialTextInputArea').html('');
  if (TO_INSERT_ROW != null && TO_INSERT_ROW.attr('role') == 'addKeyword') {
    var row = $(ADD_KEYWORD_ROW);
    row.children('.val').html(textContent);
    var box = TO_INSERT_ROW.parent().children('.keywordsWrapper');
    box.prepend(row);
  } else if (TO_INSERT_ROW != null && TO_INSERT_ROW.attr("role") == 'editKeyword') {
    TO_INSERT_ROW.children('.val').html(textContent);
  } else if (TO_INSERT_ROW != null && TO_INSERT_ROW.attr("role") == 'btnBox') {
    var box = TO_INSERT_ROW.parents('.content');
    var row = $(TEXT_ROW);
    row.children('.val').html(textContent);
    box.append(row);
    // 在最下面的计数器中加一
    var box = TO_INSERT_ROW.parents('.ruleDetailWrapper');
    var textAmountBox = $(box.find('.textAmount')[0]);
    textAmountBox.text(parseInt(textAmountBox.text()) + 1);
  } else {
    TO_INSERT_ROW.children('.val').html(textContent);
  }
  $('#materialBoxWrapper').fadeOut();
  TO_INSERT_ROW = null;
}

// 当用户在素材框中选择了语音后将语音加到回复中的行为
var saveVoice = function() {
  var choosenVoice = $($('input[name="voiceSelect"]:checked').parents('.voiceItem')[0]);
  var mediaId = choosenVoice.attr('mediaId');
  var name = choosenVoice.children('.voiceName').text();
  var len = choosenVoice.children('.voiceLen').text();
  if (TO_INSERT_ROW != null && TO_INSERT_ROW.attr('role') == 'btnBox') {
    var row = $(VOICE_ROW);
    row.attr('mediaId', mediaId);
    row.children('.val').children('.voiceName').text(name);
    row.children('.val').children('.voiceLen').text(len);
    var box = TO_INSERT_ROW.parents('.content');
    box.append(row);
    // 在最下面的计数器中加一
    var box = TO_INSERT_ROW.parents('.ruleDetailWrapper');
    var voiceAmountBox = $(box.find('.voiceAmount')[0]);
    voiceAmountBox.text(parseInt(voiceAmountBox.text()) + 1);
  } else {
    TO_INSERT_ROW.children('.val').children('.voiceName').text(name);
    TO_INSERT_ROW.children('.val').children('.voiceLen').text(len);
    TO_INSERT_ROW.attr('mediaId', mediaId);
  }
  $('#materialBoxWrapper').fadeOut();
  TO_INSERT_ROW = null;
}

var showMaterialBoxAction = function() {
  var handlers = {
    'Image' : saveImage,
    'Text' : saveText,
  };
  $(document).delegate('.showMaterialBoxBtn', 'click', function() {
  	var type = $(this).attr('type');
    TO_INSERT_ROW = $(this).parents('.ruleRow');
  	var handler = handlers[type];
  	showMaterialBox(type, handler);
  });
}