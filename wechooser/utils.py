# -*- coding: utf-8 -*-
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

# 测试平台
APPID = 'wxfd6b432a6e1e6d48'
APPSECRET = 'fc9428a6b0aa1a27aecd5850871580cb'
# 公众号
# APPID = 'wxa9e7579ea96fd669'
# APPSECRET = '684b3b6d705db03dfda263b64412b1cd'

# 日志
def logger(tp, msg):
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print '[%s][%s]\t%s' % (tp, now, msg)

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
  logger('DEBUG', u'更新数据库中的access token')
  params = {
    'grant_type': 'client_credential',
    'appid': APPID,
    'secret': APPSECRET
  }
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/token'
  method = 'GET'
 
  res = send_request(host, path, method, params=params)
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
  return token_record

# 发送请求
# 如果发送请求时服务器返回的是access_token过期的话，就跑出一个PastDueException
def send_request(host, path, method, port=443, params={}):
  client = httplib.HTTPSConnection(host, port)
  if method == 'GET':
    path = '?'.join([path, urllib.urlencode(params)])
    client.request(method, path)
  else:
    client.request(method, path, json.dumps(params, ensure_ascii=False).encode('utf8'))
    # client.request(method, path, urllib.urlencode(params))
  res = client.getresponse()
  if not res.status == 200:
    return False, res.status
  resDict = json.loads(res.read())
  if 'errcode' in resDict.keys() and resDict['errcode'] == 40001:
    raise PastDueException('access token past due')
  if 'errcode' in resDict.keys() and resDict['errcode'] != 0:
    return False, resDict
  return True, resDict

# 回复文本信息
def replyMsgTo(_from, _to, createTime, tp, content):
  resp = {}
  resp['FromUserName'] = _from
  resp['ToUserName'] = _to
  resp['CreateTime'] = createTime
  resp['MsgType'] = tp
  resp['Content'] = content
  return HttpResponse(ET.tostring(dict2xml(ET.Element('xml'), resp), 'utf-8'))

# 发送文本信息
def sendMsgTo(token, _to, msgType, content):
  params = {
    "touser" : _to,
    "msgtype" : msgType,
    "text" : {
      "content" : content
    }
  }
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/message/custom/send?access_token='
  method = 'POST'
  try:
    res = send_request(host=host, path=path + token.token, method=method, port=443, params=params)
  except PastDueException:
    token = update_token()
    res = send_request(host=host, path=path + token.token, method=method, port=443, params=params)
  # logger('DEBUG', u'发送一条客服消息：' + str(res) + "; " + json.dumps(params, ensure_ascii=False))
  return res

def getMaterial(token, tp, offset, count):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/material/batchget_material?access_token='
  method = 'POST'
  params = {'type' : tp, 'offset' : offset, 'count' : count}
  try:
    res = send_request(host, path + token.token, method, port=443, params=params)
  except PastDueException:
    token = update_token()
    res = send_request(host, path + token.token, method, port=443, params=params)
  return res

def getMaterialCount(token, tp):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/material/get_materialcount'
  method = 'GET'
  params = {'access_token' : token.token}
  try:
    res = send_request(host, path, method, port=443, params=params)
  except PastDueException:
    token = update_token()
    params['access_token'] = token.token
    res = send_request(host, path, method, port=443, params=params)
  if res[0]:
    return res[1][tp + '_count']
  return -1

# 将xml解析成字典
def xml2dict(root):
  dictionary = {}
  for child in root:
    if child.text:
      dictionary[child.tag] = child.text
    else:
      dictionary[child.tag] = xml2dict(child)
  return dictionary

# 将字典解析成xml
def dict2xml(root, d):
  if isinstance(d, dict):
    for key in d.keys():
      child = ET.SubElement(root, key)
      child = dict2xml(child, d[key])
  else:
    root.text = d
  return root

# 验证信息是否从微信发送过来
def verify(token, timestamp, nonce, signature):
  tmpList = [token, timestamp, nonce]
  tmpList.sort()
  tmpStr = '%s%s%s' % tuple(tmpList)
  tmpStr = hashlib.sha1(tmpStr).hexdigest()
  return tmpStr == signature

class Response:
  def __init__(self, c=0, m="", s="success"):
    self.code = c
    self.msg = m
    self.status = s
  def toJson(self):
    tmp = {}
    tmp["code"] = self.code
    tmp["msg"] = self.msg
    tmp["status"] = self.status
    return json.dumps(tmp, ensure_ascii=False)

# token过期的异常
class PastDueException(Exception):
  def __init__(self, msg):
    self.msg = msg
  def __str__(self):
    return repr(self.msg)

