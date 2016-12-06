# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

import hashlib
import time
import json
import urllib

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from wechooser.utils import Response, send_request
from wechooser.decorator import wx_logined
from wechat.models import User
from wechooser.settings import WX_APPID, WX_SECRET, WX_TOKEN
import utils

# 获取名片卡
@wx_logined
def getNameCard(request):
  user = User.objects.get(wx_openid=request.GET.get('uid', None))
  # 获取用户头像
  headimg = utils.image_to_base64(get_head_image(user.headimgurl))
  return HttpResponse(headimg)
