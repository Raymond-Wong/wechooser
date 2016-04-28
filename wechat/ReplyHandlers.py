# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from abc import ABCMeta, abstractmethod

from models import Reply, KeywordReply
from ReplyTemplates import *

import wechooser.utils
import wechat.utils

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
    keywordReplys = KeywordReply.objects.all()
    rules = []
    for keywordReply in keywordReplys:
      if keywordReply.keyword in self.params['Content']:
        rules += keywordReply.rule_set.all()
    # 如果没有匹配到任意关键词，则返回默认自动回复
    if len(rules) == 0:
      return DefaultReplyHandler(self.params).getReply()
    # 如果匹配到关键词，则随机从所有匹配到的规则中挑选一个进行回复
    rule = random.choice(rules)
    templates = json.loads(rule.templates, object_hook=wechooser.utils.loads)
    # 如果是从该规则中随机选择一个模板进行回复
    # 则直接返回用自动回复接口进行回复
    if rule.is_reply_all:
      template = random.choice(templates)
      template.ToUserName = self.params['FromUserName']
      template.FromUserName = self.params['ToUserName']
      return template.toReply()
    # 如果要将该规则中所有信息都回复，则调用客服接口进行回复
    token = wechat.utils.get_access_token()
    for template in templates:
      template.ToUserName = self.params['FromUserName']
      template.FromUserName = self.params['ToUserName']
      wechat.utils.sendMsgTo(token, template.toSend())
    return ''