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
    return ''

# 未处理类型自动回复
class DefaultReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    return ''

# 图片自动回复
class ImageReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    return ''

# 关注自动回复
class SubscribeReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    xml = toReply(_to=self.params['FromUserName'], _from=self.params['ToUserName'], template=Reply.objects.get(reply_type='subscribe').template)
    wechooser.utils.logger('DEBUG', 'reply content: ' + xml)
    return xml

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
    return ''