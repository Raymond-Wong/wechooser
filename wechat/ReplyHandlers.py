# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from abc import ABCMeta, abstractmethod

from models import Reply, KeywordReply, MenuReply
from ReplyTemplates import *

import wechooser.utils
import wechat.utils
from transmit.views import invited_by, get_template

class ReplyHandler:
  __metaclass__ = ABCMeta
  def __init__(self, params):
    self.params = params

  def getReply(self):
    try:
      reply = Reply.objects.get(reply_type=self.reply_type).template
      reply = json.loads(reply, object_hook=wechooser.utils.loads)
      reply.FromUserName = self.params['ToUserName']
      reply.ToUserName = self.params['FromUserName']
      # 所有回复都用客服发送接口进行发送
      # token = wechat.utils.get_access_token()
      # wechat.utils.sendMsgTo(token, reply.toSend())
      # return ''
      return reply.toReply()
    except Exception, e:
      wechooser.utils.logger('ERROR', '回复错误: %s' % e)
      return ''

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

# 扫描自定义二维码回复事件
class ScanReplyHandler(ReplyHandler):
  def getReply(self):
    # 调用被邀请事件
    state, invite_user = invited_by(self.params['user'], self.params)
    ret = TextTemplate(ToUserName=self.params['FromUserName'], FromUserName=self.params['ToUserName'])
    if state:
      state, namecard = get_template(qrcode_ticket=self.params['Ticket'])
      if state:
        try:
          ret.Content = namecard.invited_msg % invite_user.nickname
        except:
          ret.Content = namecard.invited_msg
    else:
      ret.Content = invite_user
    return ret.toReply()

# 事件自动回复
class EventReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    # 如果是关注事件且没有ticket关键字，则回复关注事件的handler
    if self.params['Event'] == 'subscribe' and not self.params.has_key('Ticket'):
      return SubscribeReplyHandler(self.params).getReply()
    elif self.params['Event'] == 'SCAN' or (self.params['Event'] == 'subscribe' and self.params.has_key('Ticket')):
      return ScanReplyHandler(self.params).getReply()
    eventKey = self.params['EventKey']
    try:
      reply = MenuReply.objects.get(mid=eventKey)
      template = json.loads(reply.template, object_hook=wechooser.utils.loads)
      template.FromUserName = self.params['ToUserName']
      template.ToUserName = self.params['FromUserName']
      # wechat.utils.sendMsgTo(wechat.utils.get_access_token(), template.toSend())
      # return ''
      return template.toReply()
    except Exception, e:
      return ''

# 文本自动回复
class TextReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    keywordReplys = KeywordReply.objects.all()
    rules = []
    for keywordReply in keywordReplys:
      if not keywordReply.is_fully_match and keywordReply.keyword in self.params['Content']:
        rules += keywordReply.rule_set.all()
      elif keywordReply.is_fully_match and keywordReply.keyword == self.params['Content']:
        rules += keywordReply.rule_set.all()
    # 如果没有匹配到任意关键词，则返回默认自动回复
    if len(rules) == 0:
      return DefaultReplyHandler(self.params).getReply()
    # 如果匹配到关键词，则随机从所有匹配到的规则中挑选一个进行回复
    rule = random.choice(rules)
    templates = json.loads(rule.templates, object_hook=wechooser.utils.loads)
    # 如果是从该规则中随机选择一个模板进行回复
    # 则直接返回用自动回复接口进行回复
    token = wechat.utils.get_access_token()
    if not rule.is_reply_all or len(templates) < 2:
      template = random.choice(templates)
      template.ToUserName = self.params['FromUserName']
      template.FromUserName = self.params['ToUserName']
      # wechat.utils.sendMsgTo(token, template.toSend())
      # return ''
      return template.toReply()
    # 如果要将该规则中所有信息都回复，则调用客服接口进行回复
    for template in templates:
      template.ToUserName = self.params['FromUserName']
      template.FromUserName = self.params['ToUserName']
      wechat.utils.sendMsgTo(token, template.toSend())
    return ''