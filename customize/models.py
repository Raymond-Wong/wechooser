# -*- coding: utf-8 -*-
from django.db import models
from transmit.models import Activity

TASK_STATUS = ((0, u'待执行'), (1, u'成功'), (2, u'取消'), (3, u'失败'), (4, u'处理中'))
TARGET_TYPE = ((0, u'所有'), (1, u'活动'), (2, u'个人'), (3, u'nosend'))
class Task(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  run_time = models.DateTimeField()
  keywords = models.TextField(default='{}')
  url = models.TextField(default='')
  task_name = models.CharField(max_length=30, default='')
  status = models.PositiveIntegerField(default=0, choices=TASK_STATUS)
  template_id = models.TextField(default='')
  template_name = models.TextField(default='')
  target_type = models.PositiveIntegerField(default=0, choices=TARGET_TYPE)
  target = models.PositiveIntegerField(default=0)

RECORD_TYPE = ((0, u'全部'), (1, u'活动'))
class Subscribe_Record(models.Model):
  date = models.DateField(auto_now_add=True)
  subscribe_amount = models.PositiveIntegerField(default=0)
  unsubscribe_amount = models.PositiveIntegerField(default=0)
  total_amount = models.PositiveIntegerField(default=0)
  record_type = models.PositiveIntegerField(choices=RECORD_TYPE, default=0)
  record_target = models.PositiveIntegerField(default=0)