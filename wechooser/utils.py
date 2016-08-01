# -*- coding: utf-8 -*-
import httplib
import urllib
import json
import hashlib
import time
import base64
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404

from wechat.models import access_token

# 测试平台
# APPID = 'wxfd6b432a6e1e6d48'
# APPSECRET = 'fc9428a6b0aa1a27aecd5850871580cb'
# 订阅号
# APPID = 'wxa9e7579ea96fd669'
# APPSECRET = '684b3b6d705db03dfda263b64412b1cd'
# 服务号
APPID = 'wx466a0c7c6871bc8e'
APPSECRET = 'aa06e2a00ce7dcae1d5e975e5217c478'

# 日志
def logger(tp, msg):
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print '[%s][%s]\t%s' % (tp, now, msg)

# 发送请求
# 如果发送请求时服务器返回的是access_token过期的话，就跑出一个PastDueException
def send_request(host, path, method, port=443, params={}, toLoad=True):
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
  resStr = res.read()
  if toLoad:
    resDict = json.loads(resStr, encoding="utf-8")
    if 'errcode' in resDict.keys() and resDict['errcode'] == 40001:
      raise PastDueException('access token past due')
    if 'errcode' in resDict.keys() and resDict['errcode'] != 0:
      return False, resDict
    return True, resDict
  else:
    return True, resStr

# 将xml解析成字典
def xml2dict(root):
  dictionary = {}
  for child in root:
    if isinstance(dictionary, dict) and not dictionary.has_key(child.tag):
      if child.text:
        dictionary[child.tag] = child.text
      else:
        dictionary[child.tag] = xml2dict(child)
    else:
      if isinstance(dictionary, dict) and not isinstance(dictionary[child.tag], list):
        dictionary = [{child.tag : dictionary[child.tag]}]
      if child.text:
        dictionary.append({child.tag : child.text})
      else:
        dictionary.append({child.tag : xml2dict(child)})
  return dictionary

# 将字典解析成xml
def dict2xml(root, d):
  if isinstance(d, dict):
    for key in d.keys():
      child = ET.SubElement(root, key)
      child = dict2xml(child, d[key])
  elif isinstance(d, list):
    for item in d:
      for key in item.keys():
        child = ET.SubElement(root, key)
        child = dict2xml(child, item[key])
  else:
    if isinstance(d, int) or isinstance(d, float):
      d = str(d)
    root.text = d
  return root

# 让自定义类能够被json dumps处理的函数
def dumps(obj):
  # 把obj转换成dict类型的对象
  d = { '__class__':obj.__class__.__name__, 
        '__module__':obj.__module__,
  }
  d.update(obj.__dict__)
  return d

# 让自定义类能够被json loads处理的函数
def loads(d):
  if '__class__' in d:
    class_name = d.pop('__class__')
    module_name = d.pop('__module__')
    module = __import__(module_name)
    module = module.ReplyTemplates
    class_ = getattr(module,class_name)
    args = dict((key.encode('utf8'),value) for key,value in d.items())
    inst = class_(**args)
  else:
    inst = d
  return inst

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

def parseBool(string):
  if string == 'True':
    return True
  elif string == 'False':
    return False
  return None

def prettyTime(sec):
  # ret = ''
  # if sec <= 60:
  #   if sec >= 10:
  #     return "00:" + str(sec)
  #   else:
  #     return "00:0" + str(sec)
  # sec = sec % 60
  # mini = int(sec / 60)
  # if mini <= 60:
  #   if mini >= 10:
  #     mini = str(mini)
  #   else:
  #     mini = "0" + str(mini)
  #   if sec >= 10:
  #     sec = str(sec)
  #   else:
  #     sec = "0" + str(sec)
  #   return mini + ":" + sec
  return "00:60"
