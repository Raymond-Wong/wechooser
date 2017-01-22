# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from abc import ABCMeta, abstractmethod
from datetime import timedelta, datetime

from django.utils import timezone

from models import Reply, KeywordReply, MenuReply
from customize.models import Task
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
    wechat.utils.update_statistic(params)

# 取消关注自动回复
class UnsubscribeReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
    self.reply_type = 'unsubscribe'
    wechat.utils.update_statistic(params, diff=-1)
  def getReply(self):
    return ''

# 扫描自定义二维码回复事件
class ScanReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
    self.reply_type = 'scan'
  def getReply(self):
    # 调用被邀请事件
    state0, invite_user = invited_by(self.params['user'], self.params)
    state1, namecard = get_template(qrcode_ticket=self.params['Ticket'])
    err_msg = '未知错误'
    if not state0:
      err_msg = invite_user
    elif not state1:
      err_msg = namecard
    if not (state0 and state1):
      ret = TextTemplate(ToUserName=self.params['FromUserName'], FromUserName=self.params['ToUserName'])
      ret.Content = err_msg
      return ret.toReply()
    template = json.loads(namecard.invited_msg, object_hook=wechooser.utils.loads)
    template.FromUserName = self.params['ToUserName']
    template.ToUserName = self.params['FromUserName']
    return template.toReply()

# 事件自动回复
class EventReplyHandler(ReplyHandler):
  def __init__(self, params):
    ReplyHandler.__init__(self, params)
  def getReply(self):
    # 如果是关注事件且没有ticket关键字，则回复关注事件的handler
    if self.params['Event'] == 'subscribe' and not self.params.has_key('Ticket'):
      return SubscribeReplyHandler(self.params).getReply()
    elif self.params['Event'] == 'SCAN':
      reply = ScanReplyHandler(self.params).getReply()
      if self.params['user'].source_type == 3:
        self.params['user'].source_type = 0
        state, namecard = get_template(qrcode_ticket=self.params['Ticket'])
        if state:
          self.params['user'].source_type = 1
          self.params['user'].source = namecard.activity.id
        self.params['user'].save()
      return reply
    elif self.params['Event'] == 'subscribe' and self.params.has_key('Ticket'):
      reply = ScanReplyHandler(self.params).getReply()
      state, namecard = get_template(qrcode_ticket=self.params['Ticket'])
      if state:
        wechat.utils.update_statistic(self.params, aid=namecard.activity.id)
      return reply
    elif self.params['Event'] == 'unsubscribe':
      return UnsubscribeReplyHandler(self.params).getReply()
    try:
      eventKey = self.params['EventKey']
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
    now = datetime.strptime(timezone.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
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
      # 如果要发送的信息的图文信息而且延迟时间大于0，则添加任务
      if template.MsgType == 'news' and template.DelayMins > 0:
        new_task = Task(target_type=2, template_id="keyword_reply_placeholder")
        new_task.run_time = now + timedelta(minutes=int(template.DelayMins))
        news_item = template.Items[0]
        new_task.url = news_item.Url
        new_task.news_item = json.dumps(news_item.toDic())
        new_task.target = wechat.utils.get_user(self.params['FromUserName'], wechat.utils.get_access_token()).id
        new_task.save()
        return ''
      # wechat.utils.sendMsgTo(token, template.toSend())
      # return ''
      return template.toReply()
    # 如果要将该规则中所有信息都回复，则调用客服接口进行回复
    for template in templates:
      template.ToUserName = self.params['FromUserName']
      template.FromUserName = self.params['ToUserName']
      # 如果是图文消息且延迟时间大于0，则延迟发送，否则直接发送
      if template.MsgType == 'news' and template.DelayMins > 0:
        new_task = Task(target_type=2, template_id="keyword_reply_placeholder")
        new_task.run_time = now + timedelta(minutes=int(template.DelayMins))
        news_item = template.Items[0]
        new_task.url = news_item.Url
        new_task.news_item = json.dumps(news_item.toDic())
        new_task.target = wechat.utils.get_user(self.params['FromUserName'], wechat.utils.get_access_token()).id
        new_task.save()
      else:
        wechat.utils.sendMsgTo(token, template.toSend())
    return ''