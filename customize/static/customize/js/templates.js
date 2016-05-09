var IMG_ITEM = '<div class="imageItem left" mediaId="">' +
  	  	       '  <div class="imageContentBox">' +
  	  	  	   '    <img src="" />' +
  	  	       '  </div>' +
  	  	       '  <div class="imageName">图片1.jpg</div>' +
  	  	       '</div>';

var VOICE_ITEM = '<div class="voiceItem">' +
          		 '	<span class="voiceSelect"><input type="radio" name="voiceSelect" /></span>' +
          		 '	<span class="voiceName"></span>' +
          		 '	<span class="voiceLen"></span>' +
        		 '</div>';


var VIDEO_ITEM = '<div class="videoItem">' +
          		 '	<span class="videoSelect"><input type="radio" name="videoSelect" /></span>' +
          		 '	<span class="videoName"></span>' +
               '  <span class="videoTitle"></span>' +
               '  <span class="videoDesc"></span>' +
        		   '</div>';

var MPNEWS_ITEM = '<div class="mpNewsItem">' +
                  '  <span class="mpNewsSelect"><input type="radio" name="mpNewsSelect" /></span>' +
                  '  <span class="mpNewsName"></span>' +
                  '  <span class="mpNewsCreateTime"></span>' +
                  '</div>';


var LOADING_ELEMENT = '<div class="loadingElement">正在加载素材...<div>';

var IMG_ROW = '<div class="ruleRow small reply" type="image">' +
              '  <div class="left point">&nbsp;</div>' +
              '  <div class="left val">' + 
              '    <img src="" />' +
              '  </div>' +
              '  <div class="right hint">' +
              '    <a class="deleteRowBtn" type="msg">删除</a>' +
              '  </div>' +
              '  <div class="clear"></div>' +
              '</div>';

var ADD_KEYWORD_ROW = '<div class="ruleRow small keyword" role="editKeyword" maxCharAmount="30">' +
                      '  <div class="left point">&nbsp;</div>' +
                      '  <div class="left val"></div>' +
                      '  <div class="hint right"><a class="fullMatchBtn">未全匹配</a><a class="showMaterialBoxBtn" type="Text">编辑</a><a class="deleteRowBtn">删除</a></div>' +
                      '  <div class="clear"></div>' +
                      '</div>';

var TEXT_ROW = '<div class="ruleRow small reply" type="text" maxCharAmount="300">' +
               '  <div class="left point">&nbsp;</div>' +
               '  <div class="left val"></div>' +
               '  <div class="right hint">' +
               '    <a class="showMaterialBoxBtn" type="Text">编辑</a>' +
               '    <a class="deleteRowBtn" type="msg">删除</a>' +
               '  </div>' +
               '  <div class="clear"></div>' +
               '</div>';

var VOICE_ROW = '<div class="ruleRow small reply" type="voice">' +
                '  <div class="left point">&nbsp;</div>' +
                '  <div class="left val">' +
                '    <img class="left" src="/static/customize/icon/voice.png" />' +
                '    <div class="voiceName"></div>' +
                '    <div class="voiceLen"></div>' +
                '  </div>' +
                '  <div class="right hint">' +
                '    <a class="deleteRowBtn" type="msg">删除</a>' +
                '  </div>' +
                '  <div class="clear"></div>' +
                '</div>';

var VIDEO_ROW = '<div class="ruleRow small reply" type="video">' +
                '  <div class="left point">&nbsp;</div>' +
                '  <div class="left val">' +
                '    <div class="videoName"></div>' +
                '    <div class="videoTitle"></div>' +
                '    <div class="videoDesc"></div>' +
                '  </div>' +
                '  <div class="right hint">' +
                '    <a class="deleteRowBtn" type="msg">删除</a>' +
                '  </div>' +
                '  <div class="clear"></div>' +
                '</div>';

var NEWS_ROW = '<div class="ruleRow small reply" type="news">' +
                '  <div class="left point">&nbsp;</div>' +
                '  <div class="left val">' +
                '  </div>' +
                '  <div class="right hint">' +
                '    <a class="deleteRowBtn" type="msg">删除</a>' +
                '  </div>' +
                '  <div class="clear"></div>' +
                '</div>';

var NEWS_WRAPPER = '<div class="newsItemWrapper left"></div>';

var NEWS_BOX = '<div class="newsItemBox">' +
               '  <div class="newsItemImg"></div>' +
               '  <div class="newsItemTitle"></div>' +
               '</div>';

var NEW_RULE = '<div class="ruleWrapper">' +
               '  <div class="ruleShortWrapper">' +
               '    <div class="head">' +
               '      <font class="ruleName">新规则</font>' +
               '      <font class="right showDetailBtn"><span class="glyphicon glyphicon-chevron-down"></span></font>' +
               '    </div>' +
               '    <div class="content">' +
               '      <div class="keywordsWrapper">' +
               '        <div class="key left">关键词：</div>' +
               '        <div class="right val"></div>' +
               '        <div class="clear"></div>' +
               '      </div>' +
               '      <div class="replyWrapper">' +
               '        <div class="key left">回复：</div>' +
               '        <div class="right val">' +
               '          <font class="totalAmount">0</font>条（' +
               '          <font class="textAmount">0</font>条文字' +
               '          <font class="imageAmount">0</font>条图片' +
               '          <font class="voiceAmount">0</font>条语音' +
               '          <font class="videoAmount">0</font>条视频' +
               '          <font class="newsAmount">0</font>条图文）' +
               '        </div>' +
               '        <div class="clear"></div>' +
               '      </div>' +
               '    </div>' +
               '  </div>' +
               '  <div class="ruleDetailWrapper">' +
               '    <div class="head">' +
               '      新规则' +
               '      <font class="right showDetailBtn"><span class="glyphicon glyphicon-chevron-up"></span></font>' +
               '    </div>' +
               '    <div class="content">' +
               '      <div class="ruleRow">' +
               '        <div class="left point">·</div>' +
               '        <div class="left key">规则名</div>' +
               '        <div class="left val"><input type="text" name="ruleName" placeholder="规则名最多60字" /></div>' +
               '        <div class="clear"></div>' +
               '      </div>' +
               '      <div class="ruleRow" role="addKeyword" maxCharAmount="30">' +
               '        <div class="left point">·</div>' +
               '        <div class="left key">关键字</div>' +
               '        <div class="left val"></div>' +
               '        <div class="right hint"><a class="showMaterialBoxBtn" type="Text">添加关键字</a></div>' +
               '        <div class="clear"></div>' +
               '      </div>' +
               '      <div class="keywordsWrapper">' +
               '      </div>' +
               '      <div class="ruleRow">' +
               '        <div class="left point">·</div>' +
               '        <div class="left key">回复</div>' +
               '        <div class="left val"></div>' +
               '        <div class="right hint"><a class="replyAllBtn">未回复全部</a></div>' +
               '        <div class="clear"></div>' +
               '      </div>' +
               '      <div class="ruleRow small" role="btnBox" maxCharAmount="300">' +
               '        <div class="left point">&nbsp;</div>' +
               '        <div class="left val">' +
               '          <a class="addContentBtn showMaterialBoxBtn" type="Text">文字</a>' +
               '          <a class="addContentBtn showMaterialBoxBtn" type="Image">图片</a>' +
               '          <a class="addContentBtn showMaterialBoxBtn" type="Voice">语音</a>' +
               '          <a class="addContentBtn showMaterialBoxBtn" type="Video">视频</a>' +
               '          <a class="addContentBtn showMaterialBoxBtn" type="News">图文</a>' +
               '        </div>' +
               '        <div class="clear"></div>' +
               '      </div>' +
               '    </div>' +
               '    <div class="foot">' +
               '      文字（<font class="textAmount">0</font>）' +
               '      图片（<font class="imageAmount">0</font>）' +
               '      语音（<font class="voiceAmount">0</font>）' +
               '      视频（<font class="videoAmount">0</font>）' +
               '      图文（<font class="newsAmount">0</font>）' +
               '      <div class="btnBox right">' +
               '        <div class="btn saveRuleBtn">保存</div>' +
               '        <div class="btn wait deleteRuleBtn">删除</div>' +
               '      </div>' +
               '      <div class="clear"></div>' +
               '    </div>' +
               '  </div>' +
               '</div>';
var NEW_MENU_ITEM = '<div class="menuBtnBox">' +
                    '  <div class="editMenuBtn menuBtn flMenuBtn">菜单名称</div>' +
                    '  <div class="menuSubBtnContainer">' +
                    '    <div class="menuSubBtnWrapper">' +
                    '      <div class="menuSubBtnBox">' +
                    '        <div class="addMenuBtn menuBtn">' +
                    '          <span class="glyphicon glyphicon-plus"></span>' +
                    '        </div>' +
                    '      </div>' +
                    '      <div class="arrowOuter"></div>' +
                    '      <div class="arrowInner"></div>' +
                    '</div></div></div>';

var MENU_SECOND_BTN = '<div class="editMenuBtn menuBtn">子菜单名称</div>'