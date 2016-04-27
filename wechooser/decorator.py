# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import httplib
import urllib
import json
import hashlib
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404

# from wechat.models import access_token

from utils import *
import wechat.utils

APPID = 'wxfd6b432a6e1e6d48'
APPSECRET = 'fc9428a6b0aa1a27aecd5850871580cb'
TOKEN = 'wechooser'

# 获取access_token的修饰器
def has_token(view):
  tokens = access_token.objects.order_by('-start_time')
  now = datetime.now()
  if len(tokens) <= 0 or now > tokens[0].end_time:
    most_recent_token = wechat.utils.update_token()
  else:
    most_recent_token = tokens[0]
  def do_has_token(request, *args, **kwargs):
    return view(request, most_recent_token, *args, **kwargs)
  return do_has_token

def is_verified(view):
  def verified(request, *args, **kwargs):
    if wechat.utils.verify(TOKEN, request.GET.get('timestamp', None), request.GET.get('nonce', None), request.GET.get('signature', None)):
      return view(request, *args, **kwargs)
    else:
      raise Http404
  return verified