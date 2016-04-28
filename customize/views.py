# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

import wechooser.utils
import wechat.utils

from wechooser.utils import Response
from wechat.ReplyTemplates import *
from wechat.models import *
from wechooser.decorator import *

@has_token
def editMenu(request, token):
  if request.method == 'GET':
    menu = wechat.utils.getMenu(token)
    wechooser.utils.logger('DEBUG', menu)
    return render_to_response('customize/editMenu.html', {'menu' : menu})

def getMaterial(request):
  if request.method == 'GET':
    return render_to_response('customize/getMaterial.html')

@csrf_exempt
def setReply(request):
  if request.method == 'GET':
    return render_to_response('customize/setReply.html')
  replyType = request.GET.get('type')
  if replyType == 'keyword':
    return setKeywordReply(request)
  # 尝试从数据库中获取该类型的模板，如果不存在则新建
  try:
    reply = Reply.objects.get(reply_type=replyType)
  except Exception as e:
    wechooser.utils.logger('ERROR', e)
    reply = Reply()
    reply.reply_type=replyType
  msgType = request.POST.get('MsgType')
  if msgType == 'text':
    content = request.POST.get('Content')
    reply.template = json.dumps(TextTemplate(Content=content), default=wechooser.utils.dumps)
  elif msgType == 'image':
    mediaId = request.POST.get('MediaId')
    reply.template = json.dumps(ImageTemplate(MediaId=mediaId), default=wechooser.utils.dumps)
  elif msgType == 'voice':
    mediaId = request.POST.get('MediaId')
    reply.template = json.dumps(VoiceTemplate(MediaId=mediaId), default=wechooser.utils.dumps)
  elif msgType == 'video':
    mediaId = request.POST.get('MediaId')
    title = request.POST.get('Title')
    description = request.POST.get('Description')
    reply.template = json.dumps(VideoTemplate(MediaId=mediaId, Title=title, Description=description), default=wechooser.utils.dumps)
  reply.save()
  return HttpResponse(Response(m="replyType=%s, msgType=%s" % (replyType, msgType)).toJson())

@csrf_exempt
def setKeywordReply(request):
  pass
