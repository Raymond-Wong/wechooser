$(document).ready(function() {
  $('#btn').click(function() {
    var menu = $('#menu').val();
    if (confirm(menu)) {
      var params = {"menu" : menu};
      $.post('/wechat/menu', params, function(res) {
  	    console.log(res);
      });
    }
  });
});