# -*- coding: utf-8 -*-
from django.db import models
from wechat.models import User

ORDER_STATUS = ((1, u'processing'), (2, u'ok'), (3, u'fail'))
class Order(models.Model):
  user = models.ForeignKey(User)
  credits = models.PositiveIntegerField()
  timestamp = models.CharField(max_length=15)
  description = models.TextField(default='')
  orderNum = models.CharField(max_length=50)
  otype = models.CharField(max_length=50)
  facePrice = models.PositiveIntegerField()
  actualPrice = models.PositiveIntegerField()
  ip = models.CharField(max_length=20)
  waitAudit = models.BooleanField(default=False)
  params = models.TextField(null=True)
  status = models.PositiveIntegerField(choices=ORDER_STATUS, default=1)

# 签到记录
class Sign_In(models.Model):
  date = models.DateField(auto_now_add=True)
  users = models.ManyToManyField(User)
