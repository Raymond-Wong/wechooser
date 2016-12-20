var insertIntoCaret = function(id, str){
  var selection= window.getSelection ? window.getSelection() : document.selection;
  var range= selection.createRange ? selection.createRange() : selection.getRangeAt(0);
  if (!window.getSelection){
    document.getElementById(id).focus();
    var selection= window.getSelection ? window.getSelection() : document.selection;
    var range= selection.createRange ? selection.createRange() : selection.getRangeAt(0);
    range.pasteHTML(str);
    range.collapse(false);
    range.select();
  }else{
    document.getElementById(id).focus();
    range.collapse(false);
    var hasR = range.createContextualFragment(str);
    var hasR_lastChild = hasR.lastChild;
    while (hasR_lastChild && hasR_lastChild.nodeName.toLowerCase() == "br" && hasR_lastChild.previousSibling && hasR_lastChild.previousSibling.nodeName.toLowerCase() == "br") {
      var e = hasR_lastChild;
      hasR_lastChild = hasR_lastChild.previousSibling;
      hasR.removeChild(e)
    }
    range.insertNode(hasR);
    if (hasR_lastChild) {
      range.setEndAfter(hasR_lastChild);
      range.setStartAfter(hasR_lastChild)
    }
    selection.removeAllRanges();
    selection.addRange(range)
  }
}

var showLoading = function() {
  $('#loadingEle').addClass('rotate');
  $('#loadingContainer').show();
}

var hideLoading = function() {
  $('#loadingEle').removeClass('rotate');
  $('#loadingContainer').hide();
}

var post = function(url, data, callback) {
  console.log('url:', url, 'data:', data);
  $.ajax({
    url: url,
    data: data,
    type: 'POST',
    success: function(data, status) {
      if (data['code'] == 0) {
        callback(data, status);
      } else {
        topAlert(data['msg'], 'error');
        return false;
      }
    },
    error: function() {
      topAlert('服务器发生错误', 'error');
    }
  });
}

// 把字符串中的表情转换成图片
var str2face = function(str) {
  if (str == undefined || str.length == 0) {
    return '';
  }
  var faceImg = '<img class="insertedFace" src="{0}" name="{1}" />';
  var start = str.indexOf('[', 0);
  var end = str.indexOf(']', start) + 1;
  while (start >= 0 && end >= 0) {
    var faceStr = str.substring(start + 1, end - 1);
    var faceImgStr = String.format(faceImg, $('img[name="[' + faceStr + ']"]').attr('src'), faceStr);
    str = str.replace('[' + faceStr + ']', faceImgStr);
    start = str.indexOf('[', end);
    end = str.indexOf(']', start) + 1;
  }
  var tmpDom = $('<div></div>');
  tmpDom.html(str);
  tmpDom.children('img').each(function() {
    $(this).attr('name', '[' + $(this).attr('name') + ']');
  })
  return tmpDom.html();
}

// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，   
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)   
// 例子：   
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423   
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.Format = function(fmt) { //author: meizz   
  var o = {   
    "M+" : this.getMonth()+1,                 //月份   
    "d+" : this.getDate(),                    //日   
    "h+" : this.getHours(),                   //小时   
    "m+" : this.getMinutes(),                 //分   
    "s+" : this.getSeconds(),                 //秒   
    "q+" : Math.floor((this.getMonth()+3)/3), //季度   
    "S"  : this.getMilliseconds()             //毫秒   
  };   
  if(/(y+)/.test(fmt))   
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));   
  for(var k in o)   
    if(new RegExp("("+ k +")").test(fmt))   
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
  return fmt;
}