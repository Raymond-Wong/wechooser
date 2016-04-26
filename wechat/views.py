# -*- coding: utf-8 -*-
import sys
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

from decorator import has_token, is_verified
from utils import *

TOKEN = 'wechooser'
APPID = 'wxfd6b432a6e1e6d48'
APPSECRET = 'fc9428a6b0aa1a27aecd5850871580cb'
# APPID = 'wxa9e7579ea96fd669'
# APPSECRET = '684b3b6d705db03dfda263b64412b1cd'

@csrf_exempt
def entrance(request):
  if request.method == 'GET':
    if verify(TOKEN, request.GET.get('timestamp', None), request.GET.get('nonce', None), request.GET.get('signature', None)):
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
  dictionary = xml2dict(root)
  return message(dictionary, token)

def message(dictionary, token):
  sendMsgTo(token, dictionary['FromUserName'], 'text', '客服信息')
  if dictionary['MsgType'] == 'text':
    return replyMsgTo(dictionary['ToUserName'], dictionary['FromUserName'], str(int(time.time())), 'text', u'服务器捕获消息: %s' % dictionary['Content'])
  if dictionary['MsgType'] != 'image':
    return HttpResponse('')
  template = u'收到一条图片信息'
  try:
    template = ReplyTemplate.objects.get(msgType='image').content
  except Exception as e:
    logger('ERROR', e)
    pass
  return replyMsgTo(dictionary['ToUserName'], dictionary['FromUserName'], str(int(time.time())), 'text', template)

@csrf_exempt
@has_token
def editMenu(request, token):
  if request.method == 'GET':
    return HttpResponse('forbidden from browser')
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/menu/create?access_token=' + token.token
  method = 'POST'
  # params = json.loads(request.POST.get('menu'))
  params = {'button' : []}
  params['button'].append({"name" : "今日歌曲", "type" : "click", "key" : "asdf"})
  logger('DEBUG', 'is unicode: %s' % (json.dumps(params, ensure_ascii=False))))
  res = send_request(host, path, method, port=80, params=params)
  if res[0]:
    now = datetime.now()
    offset = timedelta(seconds=(5 * 60))
    end = now + offset
    end = end.strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(Response(m=u"自定义菜单将在 %s 时生效; access_token: %s" % (end, token.token)).toJson())
  return HttpResponse(Response(c=-1, m=(str(res[1]) + ', ' + json.dumps(json.loads(request.POST.get('menu')), ensure_ascii=False)), s="failed").toJson())
