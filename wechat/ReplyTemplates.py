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
  def toDic(self):
    ret = {}
    ret['FromUserName'] = self.FromUserName
    ret['ToUserName'] = self.ToUserName
    ret['CreateTime'] = self.CreateTime
    ret['MsgType'] = self.MsgType
    self.update()
    return ret

class TextTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='text', Content=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.Content = Content
  def toReply(self):
    dic = self.toDic()
    dic['Content'] = self.Content
    return ET.tostring(utils.dict2xml(ET.Element('xml'), dic), 'utf-8')

class ImageTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='image', MediaId=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.MediaId = MediaId
  def toReply(self):
    dic = self.toDic()
    dic['Image'] = {'MediaId' : self.MediaId}
    return ET.tostring(utils.dict2xml(ET.Element('xml'), dic), 'utf-8')

class VoiceTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='voice', MediaId=''):
    Template.__init__(self, ToUserName=ToUserName, FromUserName=FromUserName, MsgType=MsgType, CreateTime=CreateTime)
    self.MediaId = MediaId
  def toReply(self):
    dic = self.toDic()
    dic['Voice'] = {'MediaId' : self.MediaId}
    return ET.tostring(utils.dict2xml(ET.Element('xml'), dic), 'utf-8')

class VideoTemplate(Template):
  def __init__(self, ToUserName='', FromUserName='', CreateTime=time.time(), MsgType='video', MediaId='', Title='', Description=''):
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