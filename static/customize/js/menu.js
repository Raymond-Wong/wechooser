$(document).ready(function() {
  $('#menuForm').submit(function() {
    var menu = $('#menu').html();
    if (confirm(menu))
      var params = {"menu" : menu};
      $.post('/wechat/menu', params, function(res) {
  	    console.log(res);
      });
  });
});