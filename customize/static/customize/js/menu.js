$(document).ready(function() {
  var menu = {};
  menu['button'] = [];
  menu['button'].push({"type" : "click", "name" : "今日歌曲", "key" : "V1001_TODAY_MUSIC"});
  menu['button'].push({"name" : "菜单", "sub_button" : []});
  menu['button'][1]['sub_button'].push({'url' : 'http://www.baidu.com', 'type' : 'view', 'name' : '搜索'});
  var params = {"menu" : menu};
  alert(params);
  $.post('/wechat/menu', params, function(res) {
  	console.log(res);
  });
});