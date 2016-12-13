# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import hashlib
import time
import json
import urllib
import datetime

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from wechooser.utils import Response, send_request
from wechooser.decorator import wx_logined, is_logined
from models import Order, Credit_Record
from wechat.models import User
from wechooser.settings import DB_APPID, DB_APPSECRET, CREDITS_DIFF
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
  user = None
  # 判断用户是否存在
  try:
    user = User.objects.get(wx_openid=request.GET.get('uid', None))
  except:
    return HttpResponse(json.dumps(dict(status='fail', errorMessage='用户不存在', credits=0)), content_type="application/json")
  # 判断签名是否正确
  sign = request.GET.get('sign', None)
  params = utils.request2dict(request.GET, ['appKey', 'uid', 'credits', 'timestamp', 'description', 'orderNum', \
    'type', 'facePrice', 'actualPrice', 'ip', 'waitAudit', 'params'])
  t_sign = utils.getSignStr(params, DB_APPSECRET)
  if sign != t_sign:
    return HttpResponse(json.dumps(dict(status='fail', errorMessage='签名匹配失败', credits=0)), content_type="application/json")
  appKey = request.GET.get('appKey', None)
  if appKey != DB_APPID:
    return HttpResponse(json.dumps(dict(status='fail', errorMessage='appKey匹配失败', credits=0)), content_type="application/json")
  # 创建一个新订单
  order = Order(user=user)
  order.credits = request.GET.get('credits', None)
  order.timestamp = request.GET.get('timestamp', None)
  order.description = request.GET.get('description', None)
  order.orderNum = request.GET.get('orderNum', None)
  order.otype = request.GET.get('type', None)
  order.facePrice = request.GET.get('facePrice', None)
  order.actualPrice = request.GET.get('actualPrice', None)
  order.ip = request.GET.get('ip', None)
  order.waitAudit = request.GET.get('waitAudit', None)
  order.params = request.GET.get('params', None)
  order.save()
  # 更新用户积分
  user.credits = user.credits - int(order.credits)
  user.save()
  params = dict(status='ok', errorMessage='兑换成功', credits=user.credits, bizId=order.orderNum)
  return HttpResponse(json.dumps(params), content_type="application/json")

# 兑换成功后的通知处理
def notify(request):
  order = None
  try:
    order = Order.objects.get(orderNum=request.GET.get('orderNum', None))
  except:
    return HttpResponse('fail')
  # 如果订单已经处理过了就返回ok
  if order.status != 1:
    return HttpResponse('ok')
  success = True if request.GET.get('success', 'false') == 'true' else False
  # 检查签名
  # sign = request.GET.get('sign', None)
  # params = utils.request2dict(request.GET, \
  #   ['appKey', 'timestamp', 'success', 'errorMessage', 'orderNum', 'bizId'])
  # t_sign = utils.getSignStr(params, DB_APPSECRET)
  # if sign != t_sign:
  #   success = False
  # 检查appKey
  appKey = request.GET.get('appKey', None)
  if appKey != DB_APPID:
    success = False
  if success:
    order.status = 2
  else:
    order.status = 3
    user = order.user
    user.credits = user.credits + order.credits
    user.save()
  order.save()
  return HttpResponse('ok')

# 签到
@wx_logined
def signin(request):
  user = User.objects.get(wx_openid=request.session['user'])
  # 判断当前用户当天是否已签到
  begin = utils.first_time_of_day(timezone.now().date())
  end = utils.first_time_of_day(timezone.now().date() + datetime.timedelta(days=1))
  signins = user.credit_record_set.filter(credit_type=2).filter(create_time__gte=begin).filter(create_time__lt=end)
  if signins.count() > 0:
    return render_to_response('duiba/signin.html', {'user' : user, 'msg' : '当天已签到, 签到时间为%s' % signins[0].create_time.strftime('%Y-%m-%d %H:%M:%S')})
  # 创建签到记录
  signin = Credit_Record(credit_type=2)
  signin.user = user
  signin.credit_diff = CREDITS_DIFF
  signin.save()
  # 增加用户积分
  user.credits += CREDITS_DIFF
  user.save()
  return render_to_response('duiba/signin.html', {'user' : user, 'msg' : '签到成功'})

@is_logined
def checkCredit(request):
  action = request.GET.get('action', 'records')
  if action == 'records':
    return checkCreditRecords(request)
  elif action == 'orders':
    return checkCreditOrder(request)
  raise Http404

def checkCreditRecords(request):
  credit_records = Credit_Record.objects.order_by('-create_time')
  return render_to_response('duiba/checkCreditRecords.html', {'records' : credit_records, 'type' : 'records'})

def checkCreditOrder(request):
  pass

