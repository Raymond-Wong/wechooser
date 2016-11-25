# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

import hashlib
import time
import json

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from wechooser.utils import Response, send_request
import utils

def getLoginUrl(request):
  # http://www.duiba.com.cn/autoLogin/autologin?uid=test001&credits=100&appKey=jlg88loSQobWDMmGrPLqtmr&sign=fbce303d7ba7ca7b0fe14d576b494769&timestamp=1418625055000
  params = {}
  # params['uid'] = 'test001'
  # params['credits'] = '100'
  params['appKey'] = 'testappkey'
  # params['appKey'] = 'xQQjsycj8jSvNCorMkMkCFSZnqK'
  # params['timestamp'] = str(long(time.time() * 10))
  # params['redirect'] = request.GET.get('dbredirect', None)
  params = utils.filterParam(params)
  params['sign'] = utils.getSignStr(params, 'testappsecret')
  # params['sign'] = utils.getSignStr(params, '4PHcHe2h6myutohuwqywuMHNGYMp')
  # res = send_request('www.duiba.com.cn', '/autoLogin/autologin', 'GET', port=80, params=params, toLoad=False)
  return HttpResponse(Response(c=0, s="success", m=params).toJson(), content_type='application/json')