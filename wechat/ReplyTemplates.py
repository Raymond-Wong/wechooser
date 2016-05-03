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

from abc import ABCMeta, abstractmethod

import wechooser.utils as utils

class Template:
  __metaclass__ = ABCMeta
  def __init__(self, MsgType, ToUserName='', FromUserName='', CreateTime=time.time()):
    self.ToUserName = ToUserName
    self.FromUserName = FromUserName
    self.CreateTime = str(int(CreateTime))
    self.MsgType = MsgType
  def update(self):
    self.CreateTime = str(int(time.time()))
    return self
  def toDic(self):
    self.update()
    ret = {}
    ret['FromUserName'] = self.FromUserName
    ret['ToUserName'] = self.ToUserName
    ret['CreateTime'] = self.CreateTime
    ret['MsgType'] = self.MsgType
    return ret
  @abstractmethod
  def toReply(self):
    pass
  @abstractmethod
  def toSend(self):
    pass

class TextTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='text', Content=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.Content = Content
  def toReply(self):
    dic = self.toDic()
    dic['Content'] = self.Content
    return ET.tostring(utils.dict2xml(ET.Element('xml'), dic), 'utf-8')
  def toSend(self):
    ret = {}
    ret['touser'] = self.ToUserName
    ret['msgtype'] = 'text'
    ret['text'] = {}
    ret['text']['content'] = self.Content
    return ret

class ImageTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='image', MediaId=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.MediaId = MediaId
  def toReply(self):
    dic = self.toDic()
    dic['Image'] = {'MediaId' : self.MediaId}
    return ET.tostring(utils.dict2xml(ET.Element('xml'), dic), 'utf-8')
  def toSend(self):
    ret = {}
    ret['touser'] = self.ToUserName
    ret['msgtype'] = 'image'
    ret['image'] = {}
    ret['image']['media_id'] = self.MediaId
    return ret

class VoiceTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='voice', MediaId=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.MediaId = MediaId
  def toReply(self):
    dic = self.toDic()
    dic['Voice'] = {'MediaId' : self.MediaId}
    return ET.tostring(utils.dict2xml(ET.Element('xml'), dic), 'utf-8')
  def toSend(self):
    ret = {}
    ret['touser'] = self.ToUserName
    ret['msgtype'] = 'voice'
    ret['voice'] = {'media_id' : self.MediaId}
    return ret

class VideoTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='video', MediaId='', Title='', Description='', ThumbMediaId=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.MediaId = MediaId
    self.Title = Title
    self.Description = Description
  def toReply(self):
    dic = self.toDic()
    dic['Video'] = {}
    dic['Video']['Title'] = self.Title
    dic['Video']['Description'] = self.Description
    dic['Video']['MediaId'] = self.MediaId
    return ET.tostring(utils.dict2xml(ET.Element('xml'), dic), 'utf-8')
  def toSend(self):
    ret = {}
    ret['touser'] = self.ToUserName
    ret['msgtype'] = 'video'
    ret['video'] = {'media_id' : self.MediaId}
    ret['video']['title'] = self.Title
    ret['video']['description'] = self.Description
    ret['video']['thumb_media_id'] = self.ThumbMediaId
    return ret

class NewsItem:
  def __init__(self, Title="", Description="", PicUrl="", Url=""):
    self.Title = Title
    self.Description = Description
    self.PicUrl = PicUrl
    self.Url = Url
  def toDic(self):
    ret = {}
    ret['Title'] = self.Title
    ret['Description'] = self.Description
    ret['PicUrl'] = self.PicUrl
    ret['Url'] = self.Url

class NewsTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='news', MediaId='', Items=None):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.Items = Items
    self.MediaId = MediaId
  def toReply(self):
    dic = self.toDic()
    dic['ArticleCount'] = len(self.Items)
    dic['Articles'] = []
    for item in self.Items:
      dic['Articles'].append(item.toDic())
    wechooser.utils.logger('DEBUG', dic)
    return ET.tostring(utils.dict2xml(ET.Element('xml'), dic), 'utf-8')
  def toSend(self):
    ret = {}
    ret['touser'] = self.ToUserName
    ret['msgtype'] = self.MsgType
    ret['news'] = {'articles' : []}
    for item in self.Items:
      ret['news']['articles'].append(item.toDic())
    return ret
