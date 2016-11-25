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
import utils

def getLoginUrl(request):
  params = {}
  params['uid'] = 'test001'
  params['credits'] = '100'
  params['appKey'] = 'xQQjsycj8jSvNCorMkMkCFSZnqK'
  params['timestamp'] = str(long(time.time() * 1000))
  params['redirect'] = request.GET.get('dbredirect', None)
  params = utils.filterParam(params)
  params['sign'] = utils.getSignStr(params, '4PHcHe2h6myutohuwqywuMHNGYMp')
  return redirect('http://www.duiba.com.cn/autoLogin/autologin?%s' % urllib.urlencode(params))