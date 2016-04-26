$(document).ready(function() {
  var menu = {};
  menu['button'] = [];
  menu['button'].push({"type" : "click", "name" : "song", "key" : "V1001_TODAY_MUSIC"});
  menu['button'].push({"name" : "menu", "sub_button" : []});
  menu['button'][1]['sub_button'].push({'url' : 'http://www.baidu.com', 'type' : 'view', 'name' : 'search'});
  var params = {"menu" : JSON.stringify(menu)};
  console.log(params);
  $.post('/wechat/menu', params, function(res) {
  	console.log(res);
  });
});