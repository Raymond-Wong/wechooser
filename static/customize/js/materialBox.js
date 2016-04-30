$(document).ready(function() {
  bindMaterialBoxAction();
});

var bindMaterialBoxAction = function() {
  showMaterialBoxAction();
  hideMaterialBoxAction();
  saveAction();
  bindMaterialImageBoxAction();
}

var bindMaterialImageBoxAction = function() {
  updateMaterialImageBox(0, 10);
  chooseImageAction();
  deleteImageAction();
}

var initMaterialImageBox = function(offset, count) {
  var params = {'type' : 'image', 'count' : count, 'offset' : offset};
  var box = $('#materialImageBox .materialBoxInner .materialBoxContent');
  // 清空容器中的东西
  box.html('');
  $.post('/wechat/getMaterial', params, function(res) {
    var images = res['msg']['item'];
    for (var i = 0; i < images.length; i++) {
      var image = images[i];
      var url = image['url'];
      var mediaId = image['media_id'];
      var name = image['name'];
      var newImgItem = $(IMG_ITEM);
      newImgItem.attr('mediaId') = mediaId;
      $(newImgItem.find('img')[0]).attr('src') = url;
      newImgItem.children('.imageName').html(name);
      box.append(newImgItem);
    }
  }); 
}

var showMaterialBoxAction = function() {
  var btns = $('.showMaterialBoxBtn');
  btns.click(function() {
  	var type = $(this).attr('type');
  	$('.materialBox.active').removeClass('active');
  	$('#material' + type + 'Box').addClass('active');
  	$('#materialBoxWrapper').fadeIn();
  });
}

var hideMaterialBoxAction = function() {
  $('.hideMaterialBoxBtn').click(function() {
  	$('#materialBoxWrapper').fadeOut();
  });
}

var chooseImageAction = function() {
  $(document).delegate('.imageItem', 'click', function() {
    var oldChoosenImage = $('.imageItem.choosen');
    var choosenFlag = $(oldChoosenImage.find('.choosenFlag')[0]);
    if (oldChoosenImage.length > 0) {
      oldChoosenImage.removeClass('choosen');
    } else {
      choosenFlag = '<div class="choosenFlag vertical_outer"><span class="vertical_inner glyphicon glyphicon-ok"></span></div>';
    }
    $(this).children('.imageContentBox').append(choosenFlag);
    $(this).addClass('choosen');
    $('.choosenAmount').text('1');
  });
}

var saveImage = function() {
  var choosenImage = $('.imageItem.choosen');
  var imgUrl = $(choosenImage.find('img')[0]).attr('src');
  var mediaId = choosenImage.attr('mediaId');
  $('#materialBoxWrapper').fadeOut();
  $('#materialImage').append('<img src="' + imgUrl + '" mediaId="' + mediaId + '" />');
  $('#materialImage').append('<a id="deleteImageMaterialBtn">删除</a>');
  $('#chooseImageBtn').hide();
  $('#materialImage').show();
  $('#materialBoxWrapper').fadeOut();
}

var saveAction = function() {
  var handlers = {
  	'materialImageBox' : saveImage,
  }
  $('#choosenBtn').click(function() {
  	var type = $('.materialBox.active').attr('id');
  	return handlers[type]();
  });
}

var deleteImageAction = function() {
  $(document).delegate('#materialImage a', 'click', function() {
  	$('#materialImage').html('');
  	$('#materialImage').hide();
  	$('#chooseImageBtn').show();
  });
}
