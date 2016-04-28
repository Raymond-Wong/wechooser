# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import json
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

import wechooser.utils as utils

class Template:
  def __init__(self, MsgType, ToUserName='', FromUserName='', CreateTime=time.time()):
    self.ToUserName = ToUserName
    self.FromUserName = FromUserName
    self.CreateTime = str(int(CreateTime))
    self.MsgType = MsgType
  def update(self):
    self.CreateTime = str(int(time.time()))
    return self

class TextTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='text', Content=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.Content = Content

class ImageTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='image', MediaId=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.MediaId = MediaId

class VoiceTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='voice', MediaId=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.MediaId = MediaId

class VideoTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='video', MediaId='', Title='', Description=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.MediaId = MediaId
    self.Title = Title
    self.Description = Description

# 将template转换成使用客服接口发送的xml
def toReply(template):
  if isinstance(template, ReplyTemplate):
    d = json.loads(json.dumps(template, default=dumps))
  else:
    d = json.loads(template)
  if d.has_key('__class__'):
    d.pop('__class__')
  if d.has_key('__module__'):
    d.pop('__module__')
  return ET.tostring(utils.dict2xml(ET.Element('xml'), d))

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

    class_ = getattr(module,class_name)

    args = dict((key.encode('utf8'),value) for key,value in d.items())

    inst = class_(**args)
  else:
    inst = d
  return inst
