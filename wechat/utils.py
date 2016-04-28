# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import httplib
import urllib
import json
import hashlib
import time
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404

from wechat.models import access_token
from wechooser.utils import Response, PastDueException
import wechooser.utils

# 测试平台
# APPID = 'wxfd6b432a6e1e6d48'
# APPSECRET = 'fc9428a6b0aa1a27aecd5850871580cb'
# 订阅号
# APPID = 'wxa9e7579ea96fd669'
# APPSECRET = '684b3b6d705db03dfda263b64412b1cd'
# 服务号
APPID = 'wx466a0c7c6871bc8e'
APPSECRET = 'aa06e2a00ce7dcae1d5e975e5217c478'


# 获取数据库中access_token的接口
def get_access_token():
  tokens = access_token.objects.order_by('-start_time')
  now = datetime.now()
  if len(tokens) <= 0 or now > tokens[0].end_time:
    most_recent_token = update_token()
  else:
    most_recent_token = tokens[0]
  return most_recent_token

# 当数据库中access_token失效以后用于更新token的接口
def update_token():
  params = {
    'grant_type': 'client_credential',
    'appid': APPID,
    'secret': APPSECRET
  }
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/token'
  method = 'GET'
 
  res = wechooser.utils.send_request(host, path, method, params=params)
  if not res[0]:
    return False
  if res[1].get('errcode'):
    return False
  token = res[1].get('access_token')
  starttime = datetime.now()
  expires_in = timedelta(seconds=int(res[1].get('expires_in')))
  endtime = starttime + expires_in
  token_record = access_token.objects.order_by('-start_time')
  if len(token_record) > 0:
    token_record = token_record[0]
  else:
    token_record = access_token()
  token_record.token = token
  token_record.end_time = endtime
  token_record.save()
  wechooser.utils.logger('DEBUG', u'更新数据库中的access token: %s' % token_record.token)
  return token_record


# 回复文本信息
def replyMsgTo(_from, _to, createTime, tp, content):
  resp = {}
  resp['FromUserName'] = _from
  resp['ToUserName'] = _to
  resp['CreateTime'] = createTime
  resp['MsgType'] = tp
  resp['Content'] = content
  return HttpResponse(ET.tostring(wechooser.utils.dict2xml(ET.Element('xml'), resp), 'utf-8'))

# 发送文本信息
def sendMsgTo(token, params):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/message/custom/send?access_token='
  method = 'POST'
  wechooser.utils.logger('DEBUG', '发送一条客服消息: %s' % params)
  try:
    res = wechooser.utils.send_request(host=host, path=path + token.token, method=method, port=443, params=params)
  except PastDueException:
    token = update_token()
    res = wechooser.utils.send_request(host=host, path=path + token.token, method=method, port=443, params=params)
  return res

def getMaterial(token, tp, offset, count):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/material/batchget_material?access_token='
  method = 'POST'
  params = {'type' : tp, 'offset' : offset, 'count' : count}
  try:
    res = wechooser.utils.send_request(host, path + token.token, method, port=443, params=params)
  except PastDueException:
    token = update_token()
    res = wechooser.utils.send_request(host, path + token.token, method, port=443, params=params)
  if res[0]:
    return res[1]
  return {}

def getMaterialCount(token, tp):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/material/get_materialcount'
  method = 'GET'
  params = {'access_token' : token.token}
  try:
    res = wechooser.utils.send_request(host, path, method, port=443, params=params)
  except PastDueException:
    token = update_token()
    params['access_token'] = token.token
    res = wechooser.utils.send_request(host, path, method, port=443, params=params)
  if res[0]:
    return res[1][tp + '_count']
  return -1

# 获取菜单接口
def getMenu(token):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/menu/get'
  method = 'GET'
  params = {'access_token' : token.token}
  try:
    res = wechooser.utils.send_request(host, path, method, port=443, params=params)
  except PastDueException:
    token = update_token()
    params['access_token'] = token.token
    res = wechooser.utils.send_request(host, path, method, port=443, params=params)
  if res[0]:
    return res[1]
  return {}


# 验证信息是否从微信发送过来
def verify(token, timestamp, nonce, signature):
  tmpList = [token, timestamp, nonce]
  tmpList.sort()
  tmpStr = '%s%s%s' % tuple(tmpList)
  tmpStr = hashlib.sha1(tmpStr).hexdigest()
  return tmpStr == signature



