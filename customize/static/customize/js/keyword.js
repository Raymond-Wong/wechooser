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
  	  var keyword = $(this).children('.val').text();
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

var saveImage = function() {
  var choosenImage = $('.imageItem.choosen');
  var imgUrl = $(choosenImage.find('img')[0]).attr('src');
  var mediaId = choosenImage.attr('mediaId');
  if (TO_INSERT_ROW == null || TO_INSERT_ROW.attr('role') == 'btnBox') {
    var box = TO_INSERT_ROW.parents('.content');
    var newRow = $(IMG_ROW);
    $(newRow.find('img')[0]).attr('src', imgUrl);
    $(newRow.find('img')[0]).attr('mediaId', mediaId);
    box.append(newRow);
    // 在最下面的信息计数中增加一个计数器
    var box = TO_INSERT_ROW.parents('.ruleDetailWrapper');
    var imageAmountBox = $(box.find('.imageAmount')[0]);
    imageAmountBox.text(parseInt(imageAmountBox.text()) + 1);
  } else {
    var box = TO_INSERT_ROW.children('.val');
    box.html('<img src="' + imgUrl + '" mediaId="' + mediaId + '" />');
  }
  // 把已选择的图片去除选择标记
  choosenImage.removeClass('choosen');
  $(choosenImage.find('.choosenFlag')[0]).remove();
  $('#materialBoxWrapper').fadeOut();
  TO_INSERT_ROW = null;
}

var showMaterialBoxAction = function() {
  var handlers = {
    'Image' : saveImage,
  };
  $(document).delegate('.showMaterialBoxBtn', 'click', function() {
  	var type = $(this).attr('type');
    TO_INSERT_ROW = $(this).parents('.ruleRow');
  	var handler = handlers[type];
  	showMaterialBox(type, handler);
  });
}