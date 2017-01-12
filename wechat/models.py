# -*- coding: utf-8 -*-
import json
from django.db import models

class access_token(models.Model):
  token = models.CharField(max_length=600)
  start_time = models.DateTimeField(auto_now=True)
  end_time = models.DateTimeField()

# 通用自动回复
class Reply(models.Model):
  # 消息类型（image，text，other）
  reply_type = models.CharField(max_length=10, blank=False)
  # 回复内容（json字符串）
  template = models.TextField(blank=False)

class KeywordReply(models.Model):
  # 关键词
  keyword = models.CharField(max_length=30, blank=False, unique=True)
  # 是否全匹配
  is_fully_match = models.BooleanField(default=False)

class Rule(models.Model):
  # 规则名称
  name = models.CharField(max_length=60, blank=False)
  # 回复内容（json字符串）
  templates = models.TextField(blank=False)
  # 是否全部回复
  is_reply_all = models.BooleanField(default=False)
  # 该规则属于的关键词
  replys = models.ManyToManyField(KeywordReply)

class MenuReply(models.Model):
  # 按钮的key值
  mid = models.TextField()
  # 回复
  template = models.TextField(blank=False)

GENDER = ((1, u'male'), (2, u'female'))
SOURCE_TYPE = ((0, u'直接关注'), (1, u'扫码关注'), (2, u'取消关注'))
class User(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  wx_openid = models.CharField(max_length=50, unique=True)
  nickname = models.CharField(max_length=50, default='')
  sex = models.PositiveIntegerField(choices=GENDER, default=1)
  city = models.CharField(max_length=50, default='')
  province = models.CharField(max_length=50, default='')
  country = models.CharField(max_length=50, default='')
  headimgurl = models.TextField(null=True)
  credits = models.PositiveIntegerField(default=0)
  source_type = models.PositiveIntegerField(choices=SOURCE_TYPE, default=0)
  source = models.PositiveIntegerField(default=0)
