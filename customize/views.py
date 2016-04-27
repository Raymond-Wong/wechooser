# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

import wechooser.utils as utils

def editMenu(request):
  if request.method == 'GET':
    return render_to_response('customize/editMenu.html')

# def getMaterial(request):
#   if request.method == 'GET':
#     return HttpResponse('customize/getMaterial.html')