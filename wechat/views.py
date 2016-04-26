# -*- coding: utf-8 -*-
import sys
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

from models import ReplyTemplate

TOKEN = 'wechooser'
APPID = 'wxa9e7579ea96fd669'
APPSECRET = '684b3b6d705db03dfda263b64412b1cd'

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
  sendMsgTo(token, dictionary['FromUserName'], 'text', u'客服信息')
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
def custom(request):
  if request.method == 'GET':
    template = None
    try:
      template = ReplyTemplate.objects.get(msgType='image')
    except:
      pass
    return render_to_response('custom.html', {'template' : template})
  else:
    try:
      template = ReplyTemplate.objects.get(msgType=request.POST.get('msgType'))
      template.content = request.POST.get('content')
    except Exception:
      template = ReplyTemplate(msgType=request.POST.get('msgType'), content=request.POST.get('content'))
    template.save()
    return HttpResponse('设置完成!')

# @has_token
# def getUserInfo(dictionary, token):
#   host = 'api.weixin.qq.com'
#   path = '/cgi-bin/user/info'
#   method = 'GET'
#   params = {
#     'access_token' : token.token,
#     'openid' : dictionary['FromUserName'],
#     'lang' : 'zh_CN'
#   }
#   res = send_request(host, path, method, port=80, params=params)
#   if res[0]:
#     return res[1]
#   return None