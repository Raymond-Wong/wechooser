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

from wechooser.utils import Response
import utils

def getLoginUrl(request):
  params = {}
  params['uid'] = 'raymond'
  params['credits'] = 100
  params['appKey'] = 'xQQjsycj8jSvNCorMkMkCFSZnqK'
  params['timestamp'] = int(time.time() * 10)
  params['redirect'] = request.GET.get('dbredirect', None)
  params['sign'] = utils.getSignStr(params, '4PHcHe2h6myutohuwqywuMHNGYMp')
  return HttpResponse(Response(c=0, s="success", m=params).toJson(), content_type='application/json')