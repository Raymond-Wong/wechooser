# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import httplib
import urllib
import json
import hashlib
import time
import base64
import re
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404

from wechat.models import access_token
from wechooser.settings import WX_APPID, WX_SECRET
from customize.models import Statistic_Record

APPID = WX_APPID
APPSECRET = WX_SECRET

# 日志
def logger(tp, msg):
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print '[%s][%s]\t%s' % (tp, now, msg)

# 发送请求
# 如果发送请求时服务器返回的是access_token过期的话，就跑出一个PastDueException
def send_request(host, path, method, port=443, params={}, toLoad=True):
  logger('INFO', 'send request:\t[host:%s][path:%s][params:%s]' % (host, path, params))
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
  logger('INFO', 'get response:\t%s' % resStr)
  if toLoad:
    resDict = json.loads(resStr, encoding="utf-8")
    if 'errcode' in resDict.keys() and (resDict['errcode'] == 40001 or resDict['errcode'] == 40014 or resDict['errcode'] == 42001):
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

def filterEmoji(desstr,restr=''):
  try:
    co = re.compile(u'[\U00010000-\U0010ffff]')
  except re.error:
    co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
  return co.sub(restr, desstr)

# 获得图片的完整链接
def appendImageUrl(x):
  from os import environ
  remote = environ.get("APP_NAME", "")
  remote_media_path = "http://wechooser-images.stor.sinaapp.com/"
  IMAGE_BASE_URL = remote_media_path if remote else "/media/"
  if type(x) == dict:
    x["image"] = IMAGE_BASE_URL + x.get("image", "")
  elif type(x) == str or type(x) == unicode:
    x = IMAGE_BASE_URL + x
  else:
    x = "/static/pc/icon/logo.png"
  return x

# 更新数据库
def update_statistic(params, diff=1, aid=None):
  today = timezone.now().date()
  if diff > 0:
    # 设置用户的来源
    params['user'].source_type = 0 if aid is None else 1
    params['user'].source = 0 if aid is None else aid
  else:
    params['user'].source_type = 2
    params['user'].source = 0
  params['user'].save()
  # 设置完整数据
  record = Statistic_Record.objects.filter(date=today).filter(record_type=0)
  if record.count() <= 0:
    record = Statistic_Record(date=today, record_type=0)
  if diff > 0:
    record.subscribe_amount += 1
  else:
    record.unsubscribe_amount += 1
  record.save()
  if diff < 0 and params['user'].source_type == 1:
    aid = params['user'].source
  if aid is not None:
    # 更新活动数据
    record = Statistic_Record.objects.filter(today=today).filter(record_type=0).filter(record_type=1).filter(record_target=aid)
    if record.count() <= 0:
      record = Statistic_Record(date=today, record_type=1, record_target=aid)
    if diff > 0:
      record.subscribe_amount += 1
    else:
      record.unsubscribe_amount += 1
    record.save()
  return True