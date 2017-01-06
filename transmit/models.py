# -*- coding: utf-8 -*-
from django.db import models
from wechat.models import User

# 名片模板
HEAD_SHAPE = ((0, 'circle'), (1, 'square'))
GCM = ((0, 'text'), (1, 'image'), (2, 'menu'), (3, 'keyword'))
class Name_Card(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  bg = models.TextField(default='/static/transmit/images/bg.jpg')
  head_shape = models.PositiveIntegerField(choices=HEAD_SHAPE, default=0)
  head_diameter = models.FloatField(default=0.178)
  head_x = models.FloatField(default=0.409)
  head_y = models.FloatField(default=0.2525)
  name_fontsize = models.PositiveIntegerField(default=24)
  name_padding = models.PositiveIntegerField(default=20)
  name_y = models.FloatField(default=0.3625)
  qrcode_size = models.FloatField(default=0.2667)
  qrcode_x = models.FloatField(default=0.3667)
  qrcode_y = models.FloatField(default=0.6188)
  target = models.PositiveIntegerField(default=1)
  invited_msg = models.TextField(default='')
  goal_msg = models.TextField(default='')
  gain_card_method = models.PositiveIntegerField(default=3, choices=GCM)
  keyword = models.TextField(default='')
  mid = models.TextField(default='')

# 活动类
RELEASE_STATE = ((0, 'unreleased'), (1, 'released'))
class Activity(models.Model):
  release_state = models.PositiveIntegerField(choices=RELEASE_STATE, default=0)
  create_time = models.DateTimeField(auto_now_add=True)
  last_update_time = models.DateTimeField(auto_now=True)
  name = models.CharField(max_length=30, default='')
  name_card = models.OneToOneField(Name_Card)

# 用户和活动的关系
class Participation(models.Model):
  activity = models.ForeignKey(Activity)
  user = models.ForeignKey(User, related_name='participate_activity')
  invited_by = models.ForeignKey(User, null=True, related_name='invite_participate_activity')