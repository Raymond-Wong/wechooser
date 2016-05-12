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

var parseFirstLine = function(ele) {
  var html = ele.html();
  return ele;
}