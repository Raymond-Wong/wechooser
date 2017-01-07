# -*- coding: utf-8 -*-
from django.db import models
from transmit.models import Activity

TASK_STATUS = ((0, u'待执行'), (1, u'成功'), (2, u'取消'), (3, u'失败'))
TARGET_TYPE = ((0, u'所有'), (1, u'活动'), (2, u'个人'))
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

