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
    d = json.loads(json.dumps(template, default=utils.dumps))
  else:
    d = json.loads(template)
  if d.has_key('__class__'):
    d.pop('__class__')
  if d.has_key('__module__'):
    d.pop('__module__')
  return ET.tostring(utils.dict2xml(ET.Element('xml'), d))