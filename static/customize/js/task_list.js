$(document).ready(function() {
  initTable();
  initStatusChooser();
  cancelTask();
});

TABLE = null;
var initTable = function() {
  TABLE = $('#taskTable').DataTable({
    autoWidth : true,
    lengthChange: false,
    pageLength : 15,
    processing : true,
  });
}

var initStatusChooser = function() {
  $('#taskStatusChooser').change(function() {
    TABLE.draw();
  })
  var sid = ['all', '待执行', '成功', '取消', '失败'];
  $.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
      var a = sid[parseInt($('#taskStatusChooser').val())];
      var b = data[5];
      console.log(a, b);
      if (a == "all" || a == b) {
        return true;
      }
      return false;
    }
  );
}

var cancelTask = function() {
  $('.cancelBtn').click(function() {
    var row = $(this).parent().parent();
    var tid = row.attr('tid');
    post('/task/add', {'tid' : tid, 'action' : 'cancel'}, function(resp) {
      if (resp['code'] == 0) {
        row.children('.cancelCol').html('--');
        row.children('.statusCol').html('取消');
        topAlert(resp['msg']);
      } else {
        topAlert(resp['msg'], 'error');
      }
    })
  })
}