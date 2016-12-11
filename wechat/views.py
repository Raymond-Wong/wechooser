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
from urllib import quote

from django.utils.encoding import smart_str
from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from wechooser.decorator import has_token, is_verified
from wechooser.utils import Response, PastDueException
from ReplyTemplates import TextTemplate
from ReplyHandlers import *
from wechooser.settings import WX_APPID, WX_SECRET, WX_TOKEN
from transmit.views import get_name_card_mediaid, invited_by
import wechooser.utils
import utils

from models import Reply, User

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
    # 获取当前交互的用户对象
    state, user = utils.get_user(dictionary['FromUserName'], token)
    dictionary['user'] = user
    # 测试获取名片
    if dictionary['MsgType'] == 'text' and dictionary['Content'] == 'card':
      state, mediaId = get_name_card_mediaid(user, token)
      if state:
        imgTemplate = ImageTemplate(ToUserName=dictionary['FromUserName'], FromUserName=dictionary['ToUserName'], MediaId=mediaId)
        return HttpResponse(imgTemplate.toReply())
    # 如果信息类型不是文字，图片或者事件的话，则用默认处理类进行处理
    handler = DefaultReplyHandler
    if dictionary['MsgType'] in HANDLERS.keys():
      handler = HANDLERS[dictionary['MsgType']]
    ret = handler(dictionary).getReply()
    wechooser.utils.logger('INFO', 'return following msg: %s' % ret)
    return HttpResponse(ret)
  except Exception, e:
    print e
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

def loginHandler(request, view):
  # 如果session中已经保存了用户信息，则不用重复获取用户信息
  if request.session.has_key('user'):
    return view(request)
  # 获取code
  code = request.GET.get('code', None)
  if code is None and request.method == 'GET':
    url = 'http://' + request.get_host() + request.get_full_path()
    url = quote(url, safe='')
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APPID + '&redirect_uri=' + url + '&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
    return redirect(url)
  # 用code换取access token
  params = {}
  params['appid'] = APPID
  params['secret'] = APPSECRET
  params['code'] = code
  params['grant_type'] = 'authorization_code'
  res = wechooser.utils.send_request('api.weixin.qq.com', '/sns/oauth2/access_token', 'GET', params=params)
  if not res[0]:
    return HttpResponse(Response(c=1, m="login failed: get access token failed").toJson(), content_type='application/json')
  access_token = res[1]['access_token']
  openid = res[1]['openid']
  # 获取用户
  user = None
  try:
    # 用户存在数据库中
    user = User.objects.get(wx_openid=str(openid))
  except:
    # 用户不存在数据库中
    params = {}
    params['access_token'] = access_token
    params['openid'] = openid
    params['lang'] = 'zh_CN'
    res = wechooser.utils.send_request('api.weixin.qq.com', '/sns/userinfo', 'GET', params=params)
    if not res[0]:
      return HttpResponse(Response(c=2, m="login failed: get user from wechat info failed").toJson(), content_type='application/json')
    userInfo = res[1]
    user = User()
    user.wx_openid = openid
    user.nickname = userInfo['nickname']
    user.sex = userInfo['sex']
    user.province = userInfo['province']
    user.city = userInfo['city']
    user.country = userInfo['country']
    user.headimgurl = userInfo['headimgurl']
    user.save()
    print 'openid: %s, nickname: %s, id: %s' % (openid, userInfo['nickname'], user.id)
  request.session['user'] = user.wx_openid
  return view(request)