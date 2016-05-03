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

var ADD_KEYWORD_ROW = '<div class="ruleRow small keyword" role="editKeyword">' +
                      '  <div class="left point">&nbsp;</div>' +
                      '  <div class="left val"></div>' +
                      '  <div class="hint right"><a class="fullMatchBtn">未全匹配</a><a class="showMaterialBoxBtn" role="Text">编辑</a><a class="deleteRowBtn">删除</a></div>' +
                      '  <div class="clear"></div>' +
                      '</div>';

var TEXT_ROW = '<div class="ruleRow small reply" type="text">' +
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
               '</div>'