TABLE = null;
$(document).ready(function() {
  initTable();
});

var initTable = function() {
  TABLE = $('#toShowTable').DataTable({
    autoWidth : false,
    lengthChange: false,
    pageLength : 15,
    processing : true,
    searching : false,
  });
  $('.loadingHint').hide();
  $('#toShowTable').show();
}