# -*- coding: utf-8 -*-
from django.db import models

# 名片模板
HEAD_SHAPE = ((0, 'circle'), (1, 'square'))
class Name_Card(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  bg = models.TextField(default='/static/transmit/images/bg.jpg')
  head_shape = models.PositiveIntegerField(choices=HEAD_SHAPE, default=0)
  head_diameter = models.PositiveIntegerField(default=80)
  head_x = models.PositiveIntegerField(default=184)
  head_y = models.PositiveIntegerField(default=202)
  name_fontsize = models.PositiveIntegerField(default=24)
  name_padding = models.PositiveIntegerField(default=20)
  name_y = models.PositiveIntegerField(default=290)
  qrcode_size = models.PositiveIntegerField(default=120)
  qrcode_x = models.PositiveIntegerField(default=165)
  qrcode_y = models.PositiveIntegerField(default=495)
