# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
from abc import ABCMeta, abstractmethod

from models import Reply
from ReplyTemplates import *

import wechooser.utils

class ReplyHandler:
  __metaclass__ = ABCMeta
  def __init__(self, params):
    self.params = params

  @abstractmethod
  def getReply(self):
    return HttpResponse('')

# 未处理类型自动回复
class DefaultReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    return HttpResponse('')

# 图片自动回复
class ImageReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    return HttpResponse('')

# 关注自动回复
class SubscribeReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    # reply = json.loads(Reply.objects.get(reply_type='subscribe').template, object_hook=wechooser.utils.loads)
    # reply.FromUserName = params['ToUserName']
    # reply.ToUserName = params['FromUserName']
    xml = toReply(_to=params['FromUserName'], _from=params['fromUserName'], Reply.objects.get(reply_type='subscribe').template)
    logger('DEBUG', 'reply content: ' + ET.tostring(xml, 'utf-8'))
    return HttpResponse(ET.tostring(xml, 'utf-8'))

# 事件自动回复
class EventReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    if self.params['Event'] == 'subscribe':
      return SubscribeReplyHandler(self.params).getReply()

# 文本自动回复
class TextReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    return HttpResponse('')