# -*- coding: utf-8 -*-
from django.db import models

TASK_STATUS = ((0, u'待执行'), (1, u'成功'), (2, u'取消'), (3, u'失败'))
class Task(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  run_time = models.DateTimeField()
  keywords = models.TextField(default='{}')
  url = models.TextField(default='')
  task_name = models.CharField(max_length=30, default='')
  status = models.PositiveIntegerField(default=0, choices=TASK_STATUS)
  template_id = models.TextField(default='')
  template_name = models.TextField(default='')

