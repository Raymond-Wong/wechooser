$(document).ready(function() {
  $('#submitBtn').click(function() {
  	var url="/login";
  	var account = $('input[name="account"]').val();
  	if (account == '') {
  	  topAlert("账号不能为空", 'error')
  	  return;
  	}
  	console.log("account: " + account);
  	var password = $('input[name="password"]').val();
  	if (password == '') {
  	  topAlert("密码不能为空", 'error')
  	  return;
  	}
  	console.log("password: " + password);
  	var params = {'account' : account, 'password' : password};
  	$.post(url, params, function(res) {
  	  console.log(res);
  	  if (res['code'] == '0') {
  	  	window.location.href=res['msg'];
  	  } else {
  	  	topAlert(res['msg'], 'error');
  	  }
  	});
  });
});