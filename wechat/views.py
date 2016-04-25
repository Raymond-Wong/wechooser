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

APPID = 'wxfd6b432a6e1e6d48'
APPSECRET = 'fc9428a6b0aa1a27aecd5850871580cb'
TOKEN = 'wechooser'

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
def parseXml(request):
  root = ET.fromstring(smart_str(request.body))
  dictionary = xml2dict(root)
  return message(dictionary)

def message(dictionary):
  if dictionary['MsgType'] != 'image':
    return HttpResponse('')
  return sendMsgTo(dictionary['ToUserName'], dictionary['FromUserName'], str(int(time.time())), 'text', u'收到一条图片信息')

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