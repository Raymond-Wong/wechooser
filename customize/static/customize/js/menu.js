$(document).ready(function() {
  $('#btn').click(function() {
    var menu = $('#menu').html();
    console.log($('#menu'));
    console.log($('#menu').val());
    console.log($('#menu').html());
    // if (confirm(menu)) {
    //   var params = {"menu" : menu};
    //   $.post('/wechat/menu', params, function(res) {
  	 //    console.log(res);
    //   });
    // }
  });
});