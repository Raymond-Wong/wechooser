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

@csrf_exempt
def login(request):
  if request.method == 'GET':
    return render_to_response('customize/login.html')
  else:
    account = request.POST.get('account')
    password = request.POST.get('password')
    if account=="wechooser" and password=="wechooser":
      return HttpResponse(Response(m="/home").toJson(), content_type='application/json')
    elif account != "wechooser":
      return HttpResponse(Response(c=-1, s="failed", m="账号错误").toJson(), content_type='application/json')
    return HttpResponse(Response(c=-2, s="failed", m="密码错误").toJson(), content_type='application/json')

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
  replyType = request.GET.get('type', 'subscribe')
  if request.method == 'GET':
    wechooser.utils.logger('DEBUG', '返回模板: %s.html' % replyType)
    return render_to_response('customize/%s.html' % replyType, {'active' : replyType})
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
    thumbMediaId = request.POST.get('ThumbMediaId')
    reply.template = json.dumps(VideoTemplate(MediaId=mediaId, Title=title, Description=description, ThumbMediaId=thumbMediaId), default=wechooser.utils.dumps)
  reply.save()
  return HttpResponse(Response(m="保存成功").toJson(), content_type='application/json')

@csrf_exempt
def setKeywordReply(request):
  if request.method == 'GET':
    raise Http404
  # 获取关键词列表
  keywords = json.loads(request.POST.get('keywords', '{}'))
  replys = json.loads(request.POST.get('replys', '[]'))
  name = request.POST.get('name')
  isReplyAll = request.POST.get('isReplyAll')
  rid = request.POST.get('rid', None)
  # 判断当前规则是否在数据库中存在
  rule = None
  try:
    rule = Rule.objects.get(id=rid)
  except Exception:
    rule = Rule()
  # 更新规则
  rule.name = name
  rule.is_reply_all = wechooser.utils.parseBool(isReplyAll)
  # 构造templates
  templates = []
  # 遍历所有返回模板
  for template in replys:
    if template['MsgType'] == 'text':
      templates.append(TextTemplate(Content=template['Content']))
    elif template['MsgType'] == 'image':
      templates.append(ImageTemplate(MediaId=template['MediaId']))
    elif template['MsgType'] == 'voice':
      templates.append(VoiceTemplate(MediaId=template['MediaId']))
    elif template['MsgType'] == 'video':
      templates.append(VideoTemplate(MediaId=template['MediaId'], Title=template['Title'], Description=template['Description'], ThumbMediaId=template['ThumbMediaId']))
    elif template['MsgType'] == 'news':
      mediaId = template['MediaId']
      newsItems = []
      for item in template['item']:
        newsItems.append(NewsItem(Title=item['Title'], Description=item['Description'], Url=item['Url'], PicUrl=item['PicUrl']))
      templates.append(NewsTemplate(MediaId=mediaId, Items=newsItems))
  rule.templates = json.dumps(templates, default=wechooser.utils.dumps)
  rule.save()
  # 规则更新结束，开始更新关键词
  for kw in keywords.keys():
    isFullMatch = keywords[kw]
    # 判断关键词是否在表中
    keyword = None
    try:
      keyword = KeywordReply.objects.get(keyword=kw)
    except Exception:
      keyword = KeywordReply()
      keyword.save()
    keyword.keyword = kw
    keyword.is_fully_match = wechooser.utils.parseBool(isFullMatch)
    keyword.rule_set.add(rule)
    keyword.save()
  # 检验该规则是否有存在无用关键词
  for kw in rule.replys.all():
    # 如果关键词不在当前的关键词列表中
    if kw.keyword not in keywords.keys():
      # 如果该关键词没有指向任何其他规则则可以删除
      if len(kw.rule_set.all()) <= 1:
        wechooser.utils.logger('DEBUG', u'从数据库中删除关键词: %s' % kw.keyword)
        rule.replys.remove(kw)
        kw.delete()
  rule.save()
  return HttpResponse(Response(m="保存成功").toJson(), content_type='application/json')
