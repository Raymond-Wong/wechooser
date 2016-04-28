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

  def getReply(self):
    reply = Reply.objects.get(reply_type=self.reply_type).template
    reply = json.loads(reply, object_hook=wechooser.utils.loads)
    reply.FromUserName = self.params['ToUserName']
    reply.ToUserName = self.params['FromUserName']
    return reply.toReply()

# 未处理类型自动回复
class DefaultReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
    self.reply_type = 'default'

# 图片自动回复
class ImageReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
    self.reply_type = 'image'

# 关注自动回复
class SubscribeReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
    self.reply_type = 'subscribe'

# 事件自动回复
class EventReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    if self.params['Event'] == 'subscribe':
      return SubscribeReplyHandler(self.params).getReply()
    else:
      return DefaultReplyHandler(self.params).getReply()

# 文本自动回复
class TextReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    return ''