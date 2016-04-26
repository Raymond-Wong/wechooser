# -*- coding: utf-8 -*-
import json
from django.db import models

class access_token(models.Model):
  token = models.CharField(max_length=600)
  start_time = models.DateTimeField(auto_now=True)
  end_time = models.DateTimeField()

class ReplyTemplate(models.Model):
  msgType = models.CharField(max_length=100, primary_key=True)
  content = models.TextField()