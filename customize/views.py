# -*- coding: utf-8 -*-
import sys
import json

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

def editMenu(request):
  if request.method == 'GET':
    return render_to_response('editMenu.html')