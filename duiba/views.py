# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

import hashlib
import time
import json
import urllib

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from wechooser.utils import Response, send_request
from wechooser.decorator import wx_logined
from models import User, Order
from wechooser.settings import DB_APPID, DB_APPSECRET
import utils

@wx_logined
def autoLogin(request):
  user = User.objects.get(wx_openid=request.session['user'])
  params = {}
  params['uid'] = user.wx_openid
  params['credits'] = user.credits
  params['appKey'] = DB_APPID
  params['timestamp'] = str(long(time.time() * 1000))
  params['redirect'] = request.GET.get('dbredirect', None)
  params = utils.filterParam(params)
  params['sign'] = utils.getSignStr(params, DB_APPSECRET)
  return redirect('http://www.duiba.com.cn/autoLogin/autologin?%s' % urllib.urlencode(params))

def debuctCredit(request):
  uid = request.GET.get('uid', None)
  credits = request.GET.get('credits', None)
  appKey = request.GET.get('appKey', None)
  timestamp = request.GET.get('timestamp', None)
  description = request.GET.get('description', None)
  orderNum = request.GET.get('orderNum', None)
  otype = request.GET.get('type', None)
  facePrice = request.GET.get('facePrice', None)
  actualPrice = request.GET.get('actualPrice', None)
  ip = request.GET.get('ip', None)
  waitAudit = request.GET.get('waitAudit', None)
  params = request.GET.get('params', None)
  sign = request.GET.get('sign', None)
  print uid, credits, appKey, timestamp, description, orderNum, otype, facePrice, actualPrice, ip, waitAudit, params, sign
  params = dict(status='ok', errorMessage='兑换成功', credits=99, bizId=timestamp)
  return HttpResponse(json.dumps(params), content_type="application/json")

def notify(request):
  appKey = request.GET.get('appKey', None)
  timestamp = request.GET.get('timestamp', None)
  success = request.GET.get('success', False)
  errorMessage = request.GET.get('errorMessage', None)
  orderNum = request.GET.get('orderNum', None)
  bizId = request.GET.get('bizId', None)
  sign = request.GET.get('sign', None)
  print appKey, timestamp, success, errorMessage, orderNum, bizId, sign
  return HttpResponse('ok')