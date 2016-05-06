$(document).ready(function() {
  addMenuAction();
  editMenuAction();
  initReply();
});

var initReply = function() {
  $('#materialNav li[name="image"]').trigger('click');
}

var addMenuAction = function() {
  $(document).delegate('.addMenuBtn', 'click', function() {
    // 判断添加的是一级菜单还是二级菜单
    var addType = $(this).parents('.menuSubBtnBox').length > 0 ? 2 : 1;
    if (addType == 1) {
      addFirstLevelMenu($(this));
    } else {
      addSecondLevelMenu($(this));
    }
  });
}

var addFirstLevelMenu = function() {
  // 获取当前一级菜单数量
  var fstBtnBoxAmount = $('.menuBtnBox').length - 1;
  if (fstBtnBoxAmount > 1) {
    // 如果正在添加第三个主菜单,则把添加菜单按钮隐藏
    $('#addFstMenuBtnBox').hide();
    fstBtnBoxAmount -= 1;
  }
  var newBtnBox = $(NEW_MENU_ITEM);
  $('#addFstMenuBtnBox').before(newBtnBox);
  // 计算每一个btnBox的宽度
  var btnBoxWidth = $('.menuBtnWrapper').width() / (fstBtnBoxAmount + 2);
  $('.menuBtnBox').css('width', btnBoxWidth + 'px');
  // 计算subBtnBox的箭头偏移量
  var outerOffset = (btnBoxWidth - 22) / 2;
  var innerOffset = outerOffset + 2;
  $('.arrowOuter').css('left', outerOffset + 'px');
  $('.arrowInner').css('left', innerOffset + 'px');
  chooseBtn(newBtnBox.children('.editMenuBtn'));
}

var addSecondLevelMenu = function(addBtn) {
  var btnBox = addBtn.parent();
  var btnHeight = addBtn.height();
  var btnAmount = btnBox.children('.menuBtn').length;
  if (btnAmount == 5) {
    addBtn.hide();
    btnAmount -= 1;
  }
  var container = addBtn.parents('.menuSubBtnContainer');
  var newH = (btnAmount + 1) * (btnHeight + 2) + 2;
  var newT = -1 * (btnAmount + 1) * (btnHeight + 2) - 12;
  container.css('height', newH + 'px');
  container.css('top',  + newT + 'px');
  var newMenuBtn = $(MENU_SECOND_BTN);
  btnBox.prepend(newMenuBtn);
  chooseBtn(newMenuBtn);
};

var editMenuAction = function() {
  $(document).delegate('.editMenuBtn', 'click', function() {
    chooseBtn($(this));
  });
}

var chooseBtn = function(btn) {
  var oldBtn = $('.menuBtn.choosen');
  oldBtn.parents('.menuBtnBox').removeClass('choosen');
  oldBtn.removeClass('choosen');
  btn.parents('.menuBtnBox').addClass('choosen');
  btn.addClass('choosen');
  if (btn.hasClass('flMenuBtn')) {
    if ($(btn.parent().find('.menuSubBtnBox')[0]).children().length > 1) {
      $('#inputContentPanel').hide();
      $('#nameOnlyPanel').show();
    } else {
      $('#nameOnlyPanel').hide();
      $('#inputContentPanel').show();
    }
  }
}