$(document).ready(function() {
  $('#menuForm').submit(function() {
    var menu = $('#menu').text();
    var params = {"menu" : menu};
    console.log(params);
    $.post('/wechat/menu', params, function(res) {
  	  console.log(res);
    });
  });
});