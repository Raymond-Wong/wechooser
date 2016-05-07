var MENU = [];
var IS_DELETING = false;

$(document).ready(function() {
  addMenuAction();
  deleteMenuAction();
  editMenuAction();
  initMenu();
  initReply();
  bindSaveAction();
  deleteMaterialPreviewAction();
});

var bindSaveAction = function() {
  $('#menuSaveBtn').click(function() {
    $('.editMenuBtn.choosen').trigger('click');
    for (var i = 0; i < MENU.length; i++) {
      var flBtn = MENU[i];
      if (flBtn['sub_button'].length <= 0 && flBtn['reply'] == undefined) {
        $('.editMenuBtn[mid="' + flBtn['mid'] + '"]').trigger('click');
        topAlert('菜单: ' + flBtn['name'] + ' 未填入内容', 'error');
        return false;
      }
      if (flBtn['sub_button'].length > 0) {
        for (var j = 0; j < flBtn['sub_button'].length; j++) {
          var slBtn = flBtn['sub_button'][j];
          if (slBtn['reply'] == undefined) {
            $('.editMenuBtn[mid="' + slBtn['mid'] + '"]').trigger('click');
            topAlert('子菜单: ' + slBtn['name'] + ' 未填入内容', 'error');
            return false;
          }
        }
      }
    }
    $.post('/menu', {'menu' : JSON.stringify(MENU)}, function(res) {
      if (res['code'] == 0) {
        topAlert('保存成功');
      } else {
        topAlert(res, 'error');
      }
    });
  });
}

var deleteMaterialPreviewAction = function() {
  $(document).delegate('.deleteMaterialBtn', 'click', function() {
    var choosenBtn = $('.editMenuBtn.choosen');
    var btnIndex = getBtnIndexByMid(choosenBtn.attr('mid'));
    if (btnIndex[1] >= 0) {
      MENU[btnIndex[0]]['sub_button'][btnIndex[1]]['reply'] = undefined;
    } else {
      MENU[btnIndex[0]]['reply'] = undefined;
    }
  });
}

var initMenu = function() {
  MENU = $.parseJSON($('#menuPreviewWrapper').attr('menu'));
  var menu = MENU;
  for (var i = 0; i < menu.length; i++) {
    // 添加一个一级菜单
    $('#addFstMenuBtnBox .menuBtn').trigger('click');
    var btnDom = $('.menuBtn.choosen');
    // 判断该菜单类型
    var btn = menu[i];
    if (btn['sub_button'] && btn['sub_button'].length > 0) {
      btnDom.text(btn['name']);
      for (var j = 0; j < btn['sub_button'].length; j++) {
        var subBtn = btn['sub_button'][j];
        $($(btnDom.siblings('.menuSubBtnContainer')[0]).find('.addMenuBtn')[0]).trigger('click');
        var subBtnDom = $('.menuBtn.choosen');
        setBtnDom(subBtnDom, subBtn);
      }
    } else {
      setBtnDom(btnDom, btn);
    }
  }
}

var setBtnDom = function(btnDom, btn) {
  if (btn['type'] == 'click') {
    btnDom.attr('type', 'click');
    btnDom.text(btn['name']);
    btnDom.attr('key', btn['key']);
  } else {
    btnDom.attr('type', 'view');
    btnDom.text(btn['name']);
    btnDom.attr('url', btn['url']);
  }
}

var initReply = function() {
  $('#materialNav li[name="image"]').trigger('click');
}

var deleteMenuAction = function() {
  $(document).delegate('.deleteMenuBtn', 'click', function() {
    IS_DELETING = true;
    var choosenBtn = $('.editMenuBtn.choosen');
    var mid = choosenBtn.attr('mid');
    // 如果该按钮已经保存过
    if (mid != undefined) {
      var index = getBtnIndexByMid(mid);
      if (index[1] >= 0) {
        // 把二级菜单按钮从MENU字典中删除
        MENU[index[0]]['sub_button'].remove(index[1]);
      } else {
        // 把一级菜单按钮从MENU中删除
        MENU.remove(index[0]);
      }
      $('#' + mid).remove();
    }
    if (!choosenBtn.hasClass('flMenuBtn')) {
      // 获取二级菜单按钮的添加按钮
      var addBtn = choosenBtn.parents('.menuSubBtnBox').children('.addMenuBtn');
      // 获取二级菜单删除后被激活的按钮
      var toChooseBtn = $(choosenBtn.siblings('.editMenuBtn')[0]);
      if (toChooseBtn == undefined || toChooseBtn.length == 0) {
        toChooseBtn = choosenBtn.parents('.menuBtnBox').children('.flMenuBtn');
      }
      // 把二级菜单按钮删除
      choosenBtn.remove();
      // 调整二级菜单样式
      adjustSlMenuBtnStyle(addBtn);
      // 点击邻近的按钮
      toChooseBtn.trigger('click');
    } else {
      // 获取下一个可能选中的按钮
      var btnBox = choosenBtn.parent();
      var toChooseBtn = $(btnBox.siblings('.menuBtnBox')[0]).children('.flMenuBtn');
      // 删除一级菜单按钮
      btnBox.remove();
      // 调整一级菜单样式
      adjustFlMenuBtnStyle();
      // 如果存在一级按钮就点击,否则隐藏掉输入栏
      console.log(toChooseBtn);
      if (toChooseBtn.length > 0) {
        toChooseBtn.trigger('click');
      } else {
        $('#menuContentWrapper').hide();
        $('#nameOnlyPanel').hide();
        $('#inputContentPanel').hide();
      }
    }
    IS_DELETING = false;
  });
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
  // 插入一个新的菜单按钮
  var newBtnBox = $(NEW_MENU_ITEM);
  $('#addFstMenuBtnBox').before(newBtnBox);
  adjustFlMenuBtnStyle();
  var mid = Date.parse(new Date());
  newBtnBox.children('.editMenuBtn').attr('mid', mid);
  MENU.push({'type' : 'click', 'name' : '菜单名称', 'key' : mid, 'mid' : mid, 'sub_button' : []});
  chooseBtn(newBtnBox.children('.editMenuBtn'));
}

var adjustFlMenuBtnStyle = function() {
  // 获取当前一级菜单数量
  var fstBtnBoxAmount = $('.menuBtnBox').length;
  if (fstBtnBoxAmount > 3) {
    // 如果正在添加第三个主菜单,则把添加菜单按钮隐藏
    $('#addFstMenuBtnBox').hide();
    fstBtnBoxAmount -= 1;
  }
  // 计算每一个btnBox的宽度
  var btnBoxWidth = $('.menuBtnWrapper').width() / (fstBtnBoxAmount);
  $('.menuBtnBox').css('width', btnBoxWidth + 'px');
  // 计算subBtnBox的箭头偏移量
  var outerOffset = (btnBoxWidth - 22) / 2;
  var innerOffset = outerOffset + 2;
  $('.arrowOuter').css('left', outerOffset + 'px');
  $('.arrowInner').css('left', innerOffset + 'px');
}

var addSecondLevelMenu = function(addBtn) {
  var btnBox = addBtn.parent();
  var newMenuBtn = $(MENU_SECOND_BTN);
  btnBox.prepend(newMenuBtn);
  adjustSlMenuBtnStyle(addBtn);
  var mid = Date.parse(new Date());
  var pMid = newMenuBtn.parents('.menuBtnBox').children('.flMenuBtn').attr('mid');
  newMenuBtn.attr('mid', mid);
  var pMidIndex = getBtnIndexByMid(pMid)[0];
  MENU[pMidIndex]['sub_button'].push({'type' : 'click', 'name' : '子菜单名称', 'key' : mid, 'mid' : mid});
  $('#' + pMid).remove();
  chooseBtn(newMenuBtn);
  MENU[pMidIndex]['reply'] = undefined;
};

var adjustSlMenuBtnStyle = function(addBtn) {
  var btnBox = addBtn.parent();
  var btnHeight = addBtn.height();
  var btnAmount = btnBox.children('.menuBtn').length;
  if (btnAmount == 6) {
    addBtn.hide();
    btnAmount -= 1;
  }
  var container = addBtn.parents('.menuSubBtnContainer');
  var newH = btnAmount * (btnHeight + 2) + 2;
  var newT = -1 * btnAmount * (btnHeight + 2) - 12;
  container.css('height', newH + 'px');
  container.css('top',  + newT + 'px');
}

var editMenuAction = function() {
  $(document).delegate('.editMenuBtn', 'click', function() {
    chooseBtn($(this));
  });
}

var chooseBtn = function(btn) {
  $('#menuContentWrapper').css('display', 'block');
  var oldBtn = $('.menuBtn.choosen');
  // 处理旧的数据
  if (($('#inputContentPanel').css('display') != 'none' ||
      $('#nameOnlyPanel').css('display') != 'none') && !IS_DELETING) {
    backupMaterialContent(oldBtn);
  }
  // 处理新数据
  updateMaterialContent(btn);
  oldBtn.parents('.menuBtnBox').removeClass('choosen');
  oldBtn.removeClass('choosen');
  btn.parents('.menuBtnBox').addClass('choosen');
  btn.addClass('choosen');
}

var backupMaterialContent = function(oldBtn) {
  var btnName = "";
  if ($('#nameOnlyPanel').css('display') != 'none') {
    btnName = $('#nameOnlyPanel input[name="menuName"]').val();
    oldBtn.text(btnName);
    MENU[getBtnIndexByMid(oldBtn.attr('mid'))[0]]['name'] = btnName;
    $('#nameOnlyPanel').hide();
  } else {
    btnName = $('#inputContentPanel input[name="menuName"]').val();
    oldBtn.text(btnName);
    var btnIndex = getBtnIndexByMid(oldBtn.attr('mid'));
    if (btnIndex[1] >= 0) {
      MENU[btnIndex[0]]['sub_button'][btnIndex[1]]['name'] = btnName;
    } else {
      MENU[btnIndex[0]]['name'] = btnName;
    }
    // 把所有显示素材框隐藏,把所有显示素材按钮显示
    // 把旧的material的内容备份起来
    var materialContent = getMaterialContent();
    var materialContentBox = $('#material' + firstCharUpper(materialContent['MsgType']));
    // 如果有选择素材的话就备份
    if (materialContentBox.css('display') != 'none') {
      if (btnIndex[1] >= 0) {
        MENU[btnIndex[0]]['sub_button'][btnIndex[1]]['reply'] = materialContent;
      } else {
        MENU[btnIndex[0]]['reply'] = materialContent;
      }
      var backupBox = $('#' + oldBtn.attr('mid'));
      if (backupBox.length == 0) {
        $('body').append('<div class="backupBox" id="' + oldBtn.attr('mid') + '"></div>');
        backupBox = $('#' + oldBtn.attr('mid'));
      }
      backupBox.html(materialContentBox.html());
    } else {
      if (btnIndex[1] >= 0) {
        MENU[btnIndex[0]]['sub_button'][btnIndex[1]]['reply'] = undefined;
      } else {
        MENU[btnIndex[0]]['reply'] = undefined;
      }
      var backupBox = $('#' + oldBtn.attr('mid'));
      backupBox.remove();
    }
    $('.showMaterialBoxBtn').show();
    $('.showMaterialChoosenBox').hide();
    $('#inputContentPanel').hide();
  }
}

var updateMaterialContent = function(btn) {
  var btnIndex = getBtnIndexByMid(btn.attr('mid'));
  var btnInfo = null;
  if (btnIndex[1] >= 0) {
    btnInfo = MENU[btnIndex[0]]['sub_button'][btnIndex[1]];
  } else {
    btnInfo = MENU[btnIndex[0]];
  }
  if (btn.hasClass('flMenuBtn') &&
      $(btn.parent().find('.menuSubBtnBox')[0]).children().length > 1) {
    $('#nameOnlyPanel input[name="menuName"]').val(btnInfo['name']);
    $('#nameOnlyPanel .head .menuName').text(btnInfo['name']);
    $('#nameOnlyPanel').show();
  } else {
    $('#inputContentPanel input[name="menuName"]').val(btnInfo['name']);
    $('#inputContentPanel .head .menuName').text(btnInfo['name']);
    if (btnInfo['reply'] != undefined) {
      $('#materialNav li[name=' + btnInfo['reply']['MsgType'] + ']').trigger('click');
      $('#material' + firstCharUpper(btnInfo['reply']['MsgType'])).html($('#' + btn.attr('mid')).html());
      $('#choose' + firstCharUpper(btnInfo['reply']['MsgType']) + 'Btn').hide();
      $('#material' + firstCharUpper(btnInfo['reply']['MsgType'])).show();
    }
    $('#inputContentPanel').show();
  }
}

var getBtnIndexByMid = function(mid) {
  for (var i = 0; i < MENU.length; i++) {
    if (MENU[i]['mid'] == mid)
      return [i, -1];
    if (MENU[i]['sub_button'].length > 0) {
      for (var j = 0; j < MENU[i]['sub_button'].length; j++) {
        if (MENU[i]['sub_button'][j]['mid'] == mid)
          return [i, j];
      }
    }
  }
  return [-1, -1];
}

var firstCharUpper = function(str) {
  var ret = '';
  ret = str.substr(0, 1).toUpperCase() + str.substr(1);
  return ret;
}