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
import wechooser.utils as utils

TOKEN = 'wechooser'
# 测试平台
APPID = 'wxfd6b432a6e1e6d48'
APPSECRET = 'fc9428a6b0aa1a27aecd5850871580cb'
# 公众号
# APPID = 'wxa9e7579ea96fd669'
# APPSECRET = '684b3b6d705db03dfda263b64412b1cd'

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
  dictionary = utils.xml2dict(root)
  return message(dictionary, token)

def message(dictionary, token):
  utils.sendMsgTo(token, dictionary['FromUserName'], 'text', '客服信息1')
  if dictionary['MsgType'] == 'text':
    return utils.replyMsgTo(dictionary['ToUserName'], dictionary['FromUserName'], str(int(time.time())), 'text', u'服务器捕获消息: %s' % dictionary['Content'])
  if dictionary['MsgType'] != 'image':
    return HttpResponse('')
  template = u'收到一条图片信息'
  try:
    template = utils.ReplyTemplate.objects.get(msgType='image').content
  except Exception as e:
    utils.logger('ERROR', e)
    pass
  return utils.replyMsgTo(dictionary['ToUserName'], dictionary['FromUserName'], str(int(time.time())), 'text', template)

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
    res = utils.send_request(host, path + token.token, method, port=80, params=params)
  except PastDueException:
    token = utils.update_token()
    res = utils.send_request(host, path + token.token, method, port=80, params=params)
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
  return HttpResponse(Response(m=utils.getMaterial(token, tp)).toJson())

