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
    wechooser.utils.logger('DEBUG', menu['menu']['button'][0]['name'])
    return render_to_response('customize/editMenu.html', {'menu' : menu['menu']['button']})

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
  if request.method == 'GET':
    raise Http404
  # 获取关键词列表
  params = request.POST.get('Content')
  for kw in params.keys():
    # 检查关键词是否已经存在数据库中
    # 如果不存在则创建
    keyword = None
    try:
      keyword = KeywordReply.objects.get(keyword=kw)
    except Exception:
      keyword = KeywordReply()
    keyword.save()
    # 遍历该关键词的所有规则
    for rule in params[kw]:
      # 如果该规则已经存在数据库中，则更新
      # 如果不存在则新建
      newrule = None
      try:
        newrule = Rule.objects.get(id=rule['id'])
      except Exception:
        newrule = Rule()
      newrule.name = rule['name']
      newrule.is_reply_all = rule['is_reply_all']
      templates = []
      # 遍历所有返回模板
      for template in rule['templates']:
        if template['MsgType'] == 'text':
          templates.append(TextTemplate(Content=template['Content']))
        elif template['MsgType'] == 'image':
          templates.append(ImageTemplate(MediaId=template['MediaId']))
        elif template['MsgType'] == 'voice':
          templates.append(VoiceTemplate(MediaId=template['MediaId']))
        elif template['MsgType'] == 'video':
          templates.append(VideoTemplate(MediaId=template['MediaId'], Title=template['Title'], Description=template['Description']))
      newrule.templates = json.dumps(templates, default=wechooser.utils.dumps)
      newrule.reply = keyword
      newrule.save()
  return HttpResponse(Response().toJson())