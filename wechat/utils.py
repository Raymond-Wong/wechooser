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

APPID = 'wxa9e7579ea96fd669'
APPSECRET = '684b3b6d705db03dfda263b64412b1cd'

def logger(tp, msg):
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print '[%s][%s]\t%s' % (tp, now, msg)

def get_access_token():
  tokens = access_token.objects.order_by('-start_time')
  now = datetime.now()
  if len(tokens) <= 0 or now > tokens[0].end_time:
    logger('DEBUG', u'更新数据库中的access token')
    most_recent_token = update_token()
  else:
    most_recent_token = tokens[0]
  return most_recent_token

def update_token():
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
  token_record = access_token.objects.order_by('-start_time')[0]
  token_record.token = token
  token_record.end_time = endtime
  token_record.save()
  return token_record

def send_request(host, path, method, port=443, params={}):
  client = httplib.HTTPSConnection(host, port)
  if method == 'GET':
    path = '?'.join([path, urllib.urlencode(params)])
    client.request(method, path)
  else:
    client.request(method, path, urllib.urlencode(params))
  res = client.getresponse()
  if not res.status == 200:
    return False, res.status
  return True, json.loads(res.read())

def replyMsgTo(_from, _to, createTime, tp, content):
  resp = {}
  resp['FromUserName'] = _from
  resp['ToUserName'] = _to
  resp['CreateTime'] = createTime
  resp['MsgType'] = tp
  resp['Content'] = content
  return HttpResponse(ET.tostring(dict2xml(ET.Element('xml'), resp), 'utf-8'))

def sendMsgTo(token, _to, msgType, content):
  params = {
    'touser' : _to,
    'msgtype' : msgType,
    'text' : {
      'content' : content
    }
  }
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/message/custom/send?access_token=' + token
  method = 'POST'
  return send_request(host, path, method, params)


def xml2dict(root):
  dictionary = {}
  for child in root:
    if child.text:
      dictionary[child.tag] = child.text
    else:
      dictionary[child.tag] = xml2dict(child)
  return dictionary

def dict2xml(root, d):
  if isinstance(d, dict):
    for key in d.keys():
      child = ET.SubElement(root, key)
      child = dict2xml(child, d[key])
  else:
    root.text = d
  return root

def verify(token, timestamp, nonce, signature):
  tmpList = [token, timestamp, nonce]
  tmpList.sort()
  tmpStr = '%s%s%s' % tuple(tmpList)
  tmpStr = hashlib.sha1(tmpStr).hexdigest()
  return tmpStr == signature
