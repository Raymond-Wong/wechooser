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
from ReplyTemplates import TextTemplate
from ReplyHandlers import *
from wechooser.settings import WX_APPID, WX_SECRET, WX_TOKEN
import wechooser.utils
import utils

from models import Reply

TOKEN = WX_TOKEN
APPID = WX_APPID
APPSECRET = WX_SECRET

@csrf_exempt
def entrance(request):
  if request.method == 'GET':
    if utils.verify(TOKEN, request.GET.get('timestamp', None), request.GET.get('nonce', None), request.GET.get('signature', None)):
      utils.update_token()
      return HttpResponse(request.GET.get('echostr', None))
    else:
      return HttpResponse('forbiden from browswer')
  else:
    wechooser.utils.logger('INFO', 'Get the following msg: %s' % request.body)
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
def message(dictionary, token, retried=False):
  try:
    # 如果信息类型不是文字，图片或者事件的话，则用默认处理类进行处理
    handler = DefaultReplyHandler
    if dictionary['MsgType'] in HANDLERS.keys():
      handler = HANDLERS[dictionary['MsgType']]
    ret = handler(dictionary).getReply()
    wechooser.utils.logger('INFO', 'return following msg: %s' % ret)
    return HttpResponse(ret)
  except:
    # 尝试更新token后重新发送消息
    if not retried:
      token = utils.update_token()
      return message(dictionary, token, True)
  # 发生异常，返回错误信息
  errTemplate = TextTemplate(ToUserName=dictionary['FromUserName'], FromUserName=dictionary['ToUserName'], Content='服务器发生错误，请联系工作人员')
  return HttpResponse(errTemplate.toReply())

@csrf_exempt
@has_token
def getMaterialHandler(request, token):
  try:
    return getMaterial(request, token)
  except PastDueException:
    return HttpResponse(Response(c=-1, m='access token过期').toJson(), content_type='application/json')
  except Exception, e:
    return HttpResponse(Response(c=-2, m='未知错误: %s' % e).toJson(), content_type='application/json')

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
    materials = utils.getVideoInfo(token, materials)
  if tp == 'news':
    materials = utils.getNewsInfo(token, materials)
  return HttpResponse(Response(m=materials).toJson(), content_type='application/json')

@csrf_exempt
def updateTokenHandler(request):
  try:
    utils.update_token()
    return HttpResponse(Response(m='更新成功').toJson(), content_type='application/json')
  except Exception, e:
    return HttpResponse(Response(c=-2, m='未知错误: %s' % e).toJson(), content_type='application/json')
