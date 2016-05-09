$(document).ready(function() {
  showMpNewsBoxAction();
});

var showMpNewsBoxAction = function() {
  $('#chooseMpNewsBtn').click(function() {
  	showMaterialBox('MpNews', saveMpNewsHandler);
  });
}

var saveMpNewsHandler = function() {
  var choosenMpNews = $('input[name="mpNewsSelect"]:checked').parents('.mpNewsItem');
  var url = choosenMpNews.attr('url');
  $('#menuViewLink').val(url);
  $('#materialBoxWrapper').fadeOut();
}