# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
from abc import ABCMeta, abstractmethod

from models import Reply
from ReplyTemplates import *

class ReplyHandler:
  __metaclass__ = ABCMeta
  def __init__(self, params):
    self.params = params

  @abstractmethod
  def getReply():
    pass

class DefaultReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply():
    return HttpResponse('')

class ImageReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)

  def getReply():
    return HttpResponse('')

class EventReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply():
    if self.params['Event'] == 'subscribe':
      return SubscribeReplyHanlder(self.params).getReply()

class TextReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply():
    return HttpResponse('')

class SubscribeReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply():
    return HttpResponse(toReply(Reply.objects.get(reply_type='subscribe')))

