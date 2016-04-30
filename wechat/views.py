# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

import hashlib
import time
import json
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

from datetime import datetime, timedelta
from django.utils.encoding import smart_str

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from wechooser.decorator import has_token, is_verified
from wechooser.utils import Response, PastDueException
from ReplyHandlers import *
import wechooser.utils
import utils

from models import Reply

TOKEN = 'wechooser'
# 测试平台
# APPID = 'wxfd6b432a6e1e6d48'
# APPSECRET = 'fc9428a6b0aa1a27aecd5850871580cb'
# 公众号
# APPID = 'wxa9e7579ea96fd669'
# APPSECRET = '684b3b6d705db03dfda263b64412b1cd'
# 服务号
APPID = 'wx466a0c7c6871bc8e'
APPSECRET = 'aa06e2a00ce7dcae1d5e975e5217c478'

@csrf_exempt
def entrance(request):
  if request.method == 'GET':
    if utils.verify(TOKEN, request.GET.get('timestamp', None), request.GET.get('nonce', None), request.GET.get('signature', None)):
      utils.update_token()
      return HttpResponse(request.GET.get('echostr', None))
    else:
      return HttpResponse('forbiden from browswer')
  else:
    return parseXml(request)
  raise Http404

@is_verified
@has_token
def parseXml(request, token):
  root = ET.fromstring(smart_str(request.body))
  dictionary = wechooser.utils.xml2dict(root)
  return message(dictionary, token)

# 所有信息类型的处理类
HANDLERS = {
  'text' : TextReplyHandler,
  'image' : ImageReplyHandler,
  'event' : EventReplyHandler,
}
def message(dictionary, token):
  # 如果信息类型不是文字，图片或者事件的话，则用默认处理类进行处理
  handler = DefaultReplyHandler
  if dictionary['MsgType'] in HANDLERS.keys():
    handler = HANDLERS[dictionary['MsgType']]
  return HttpResponse(handler(dictionary).getReply())

@csrf_exempt
@has_token
def editMenu(request, token):
  if request.method == 'GET':
    return HttpResponse('forbidden from browser')
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/menu/create?access_token='
  method = 'POST'
  params = json.loads(request.POST.get('menu'))
  try:
    res = wechooser.utils.send_request(host, path + token.token, method, port=80, params=params)
  except PastDueException:
    token = utils.update_token()
    res = wechooser.utils.send_request(host, path + token.token, method, port=80, params=params)
  if res[0]:
    now = datetime.now()
    offset = timedelta(seconds=(5 * 60))
    end = now + offset
    end = end.strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(Response(m=u"自定义菜单将在 %s 时生效; access_token: %s" % (end, token.token)).toJson())
  return HttpResponse(Response(c=-1, m=str(res[1])).toJson())

@csrf_exempt
@has_token
def getMaterial(request, token):
  if request.method == 'GET':
    return HttpResponse('forbidden from browser')
  tp = request.POST.get('type')
  offset = request.POST.get('offset', 0)
  count = request.POST.get('count', 0)
  materials = utils.getMaterial(token, tp, offset, count)
  # 如果是获取图片素材，则要将图片的url转换成base64
  if tp == 'image':
    materials = utils.imgUrl2base64(token, materials)
  if tp == 'voice':
    materials = utils.getVoiceLen(token, materials)
  if tp == 'video':
    materials = utils.getVideoImg(token, materials)
  return HttpResponse(Response(m=materials).toJson(), content_type='application/json')
