# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import re

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import wechooser.utils
import wechat.utils

from wechooser.utils import Response
from wechat.ReplyTemplates import *
from wechat.models import *
from transmit.models import Activity, Participation
from models import Task
from wechooser.decorator import *

@has_token
def test(request, token):
  print wechat.utils.getUserList(token)
  return render_to_response('customize/test.html')

@is_logined
def index(request):
  return HttpResponseRedirect('/reply?type=subscribe')

@is_logined
def logout(request):
  request.session['is_logined'] = False
  return HttpResponseRedirect('/login')

@csrf_exempt
def login(request):
  if request.method == 'GET':
    return render_to_response('customize/login.html')
  else:
    account = request.POST.get('account')
    password = request.POST.get('password')
    if account=="wechooser" and password=="wechooser":
      request.session['is_logined'] = True
      return HttpResponse(Response(m="/reply?type=subscribe").toJson(), content_type='application/json')
    elif account != "wechooser":
      return HttpResponse(Response(c=-1, s="failed", m="账号错误").toJson(), content_type='application/json')
    return HttpResponse(Response(c=-2, s="failed", m="密码错误").toJson(), content_type='application/json')

@csrf_exempt
@is_logined
@has_token
def editMenuHandler(request, token):
  try:
    return editMenu(request, token)
  except Exception, e:
    return HttpResponse(Response(c=-1, m='未知错误: %s' % e).toJson(), content_type='application/json')

def editMenu(request, token):
  if request.method == 'GET':
    menuParent = wechat.utils.getMenu(token)
    if menuParent == None:
      return render_to_response('customize/menu.html', {'active' : 'menu', 'menu' : json.dumps([])})
    menu = menuParent['menu']['button']
    for flBtn in menu:
      if flBtn.has_key('type') and flBtn['type'] == 'click':
        flBtn['mid'] = flBtn['key']
        flBtn['reply'] = getMenuReplyTemplate(flBtn['mid'])
      else:
        if len(flBtn['sub_button']) > 0:
          for slBtn in flBtn['sub_button']:
            if slBtn['type'] == 'click':
              slBtn['mid'] = slBtn['key']
              slBtn['reply'] = getMenuReplyTemplate(slBtn["mid"])
    return render_to_response('customize/menu.html', {'active' : 'menu', 'menu' : json.dumps(menu)})
  else:
    # 如果是post请求则保存菜单
    return saveMenu(request, token)

def getMenuReplyTemplate(mid):
  try:
    template = json.loads(MenuReply.objects.get(mid=mid).template)
    if template['MsgType'] == 'image':
      template['ImageUrl'] = wechat.utils.getBase64Img(oriUrl=template['OriUrl'], mediaId=template['MediaId'])
    elif template['MsgType'] == 'voice':
      template['VoiceLen'] = wechat.utils.getOneVoiceLen(mediaId=template['MediaId'])
    elif template['MsgType'] == 'news':
      for news in template['Items']:
        news['ImageUrl'] = wechat.utils.getBase64Img(oriUrl=news['PicUrl'], mediaId=news['MediaId'])
    return template
  except Exception:
    return 'undefined'

def deleteMenu(token):
   # 发请求更改菜单
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/menu/delete?access_token='
  method = 'POST'
  res = wechooser.utils.send_request(host, path + token.token, method, port=443, params={})
  if res[0]:
    MenuReply.objects.all().delete()
    # 将保存成功的讯息传回前端
    return HttpResponse(Response(m='删除菜单成功').toJson(), content_type='application/json')
  return HttpResponse(Response(c=-1, m=res[1]).toJson(), content_type='application/json')

def saveMenu(request, token):
  menuBtns = json.loads(request.POST.get('menu'))
  if len(menuBtns) == 0:
    return deleteMenu(token)
  replys = {}
  for i, flBtn in enumerate(menuBtns):
    if len(flBtn['sub_button']) > 0:
      menuBtns[i]['sub_button'] = flBtn['sub_button']
      for j, slBtn in enumerate(menuBtns[i]['sub_button']):
        if slBtn['type'] == 'click':
          replys[str(int(slBtn['mid']))] = slBtn['reply']
        if slBtn.has_key('reply'):
          menuBtns[i]['sub_button'][j].pop('reply')
        if slBtn.has_key('mid'):
          slBtn.pop('mid')
    else:
      if flBtn['type'] == 'click':
        replys[str(int(flBtn['mid']))] = flBtn['reply']
      if flBtn.has_key('reply'):
        flBtn.pop('reply')
    if flBtn.has_key('mid'):
      flBtn.pop('mid')
  # 发请求更改菜单
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/menu/create?access_token='
  method = 'POST'
  params = {'button' : menuBtns}
  res = wechooser.utils.send_request(host, path + token.token, method, port=443, params=params)
  # 如果创建菜单成功,则将菜单中需要回复的内容存进数据库中
  if res[0]:
    # 将menu的key和reply存入数据库中
    for key in replys.keys():
      # 处理返回模板
      replyRecord = None;
      try:
        replyRecord = MenuReply.objects.get(mid=key)
      except Exception:
        replyRecord = MenuReply(mid=key)
      reply = replys[key]
      if reply['MsgType'] == 'image':
        replyRecord.template = json.dumps(ImageTemplate(MediaId=reply['MediaId'], OriUrl=reply['OriUrl']), default=wechooser.utils.dumps)
      elif reply['MsgType'] == 'voice':
        replyRecord.template = json.dumps(VoiceTemplate(MediaId=reply['MediaId'], VoiceName=reply["VoiceName"]), default=wechooser.utils.dumps)
      elif reply['MsgType'] == 'video':
        replyRecord.template = json.dumps(VideoTemplate(MediaId=reply['MediaId'], Title=reply['Title'], Description=reply['Description']), default=wechooser.utils.dumps)
      elif reply['MsgType'] == 'text':
        replyRecord.template = json.dumps(TextTemplate(Content=reply['Content']), default=wechooser.utils.dumps)
      elif reply['MsgType'] == 'news':
        newsItems = []
        for item in reply['item']:
          newsItems.append(NewsItem(MediaId=item['MediaId'], Title=item['Title'], Description=item['Description'], Url=item['Url'], PicUrl=item['PicUrl']))
        replyRecord.template = json.dumps(NewsTemplate(MediaId=reply['MediaId'], Items=newsItems), default=wechooser.utils.dumps)
      replyRecord.save()
    # 将MenuReply表中多余的按钮去除
    for reply in MenuReply.objects.all():
      if reply.mid not in replys.keys():
        reply.delete()
    # 将保存成功的讯息传回前端
    return HttpResponse(Response().toJson(), content_type='application/json')
  return HttpResponse(Response(c=-1, m=res[1]).toJson(), content_type='application/json')

@csrf_exempt
@is_logined
def setReplyHandler(request):
  try:
    return setReply(request)
  except PastDueException:
    return HttpResponse(Response(c=-1, m='access token过期').toJson(), content_type='application/json')
  except Exception, e:
    return HttpResponse(Response(c=-1, m='未知错误: %s' % e).toJson(), content_type='application/json')

def setReply(request):
  replyType = request.GET.get('type', 'subscribe')
  if request.method == 'GET':
    template = ''
    try:
      template = Reply.objects.get(reply_type=replyType).template
    except Exception:
      if replyType == 'keyword':
        return setKeywordReply(request)
      return render_to_response('customize/%s.html' % replyType, {'active' : replyType, 'template' : ''})
    template = json.loads(template)
    if template['MsgType'] == 'image':
      template['ImageUrl'] = wechat.utils.getBase64Img(oriUrl=template['OriUrl'], mediaId=template['MediaId'])
    if template['MsgType'] == 'voice':
      template['VoiceLen'] = wechat.utils.getOneVoiceLen(mediaId=template['MediaId'])
    return render_to_response('customize/%s.html' % replyType, {'active' : replyType, 'template' : json.dumps(template)})
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
    oriUrl = request.POST.get('OriUrl')
    reply.template = json.dumps(ImageTemplate(MediaId=mediaId, OriUrl=oriUrl), default=wechooser.utils.dumps)
  elif msgType == 'voice':
    mediaId = request.POST.get('MediaId')
    voiceName = request.POST.get('VoiceName')
    reply.template = json.dumps(VoiceTemplate(MediaId=mediaId, VoiceName=voiceName), default=wechooser.utils.dumps)
  elif msgType == 'video':
    mediaId = request.POST.get('MediaId')
    title = request.POST.get('Title')
    description = request.POST.get('Description')
    reply.template = json.dumps(VideoTemplate(MediaId=mediaId, Title=title, Description=description), default=wechooser.utils.dumps)
  reply.save()
  return HttpResponse(Response(m="保存成功").toJson(), content_type='application/json')

@csrf_exempt
def setKeywordReply(request):
  if request.method == 'GET':
    rules = Rule.objects.all().order_by('-id')
    retRule = []
    for rule in rules:
      newRule = {'id' : rule.id, 'name' : rule.name, 'is_reply_all' : rule.is_reply_all, 'keywords' : []}
      keywords = rule.replys.all()
      for kw in keywords:
        newRule['keywords'].append({'keyword' : kw.keyword, 'is_fully_match' : kw.is_fully_match})
      newRule['totalAmount'] = newRule['textAmount'] = newRule['imageAmount'] = newRule['voiceAmount'] = newRule['videoAmount'] = newRule['newsAmount'] = 0
      templates = json.loads(rule.templates)
      for template in templates:
        newRule['%sAmount' % template['MsgType']] += 1
        newRule['totalAmount'] += 1
        if template['MsgType'] == 'image':
          template['ImageUrl'] = wechat.utils.getBase64Img(oriUrl=template['OriUrl'], mediaId=template['MediaId'])
        elif template['MsgType'] == 'voice':
          template['VoiceLen'] = wechat.utils.getOneVoiceLen(mediaId=template['MediaId'])
        elif template['MsgType'] == 'news':
          for news in template['Items']:
            news['ImageUrl'] = wechat.utils.getBase64Img(oriUrl=news['PicUrl'], mediaId=news['MediaId'])
      newRule['templates'] = templates
      retRule.append(newRule)
    return render_to_response('customize/keyword.html', {'active' : 'keyword', 'rules' : retRule})
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
      templates.append(ImageTemplate(MediaId=template['MediaId'], OriUrl=template['OriUrl']))
    elif template['MsgType'] == 'voice':
      templates.append(VoiceTemplate(MediaId=template['MediaId'], VoiceName=template['VoiceName']))
    elif template['MsgType'] == 'video':
      templates.append(VideoTemplate(MediaId=template['MediaId'], Title=template['Title'], Description=template['Description']))
    elif template['MsgType'] == 'news':
      mediaId = template['MediaId']
      newsItems = []
      for item in template['item']:
        newsItems.append(NewsItem(MediaId=item['MediaId'], Title=item['Title'], Description=item['Description'], Url=item['Url'], PicUrl=item['PicUrl']))
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
        rule.replys.remove(kw)
        kw.delete()
  rule.save()
  return HttpResponse(Response(m=rule.id).toJson(), content_type='application/json')

# 删除回复的接口
@csrf_exempt
def deleteReply(request):
  replyType = request.GET.get('type', 'subscribe')
  if replyType != 'keyword':
    Reply.objects.get(reply_type=replyType).delete()
  else:
    rid = request.GET.get('rid', None)
    try:
      rule = Rule.objects.get(id=rid)
    except Exception:
      return HttpResponse(Response(m='').toJson(), content_type='application/json')
    for kw in rule.replys.all():
      rule.replys.remove(kw)
      # 如果该关键词没有与其他关键词存在关联,则删除
      if len(kw.rule_set.all()) <= 0:
        kw.delete()
    rule.delete()
  return HttpResponse(Response(m='').toJson(), content_type='application/json')

@csrf_exempt
@is_logined
@has_token
def addTaskHandler(request, token):
  if request.method == 'GET':
    aid = request.GET.get('aid', None)
    templates = wechat.utils.get_template_msg_list(token)
    for template in templates:
      template['keywords'] = re.findall('{{.+\.DATA}}.*', template['content'])
      template['keywords'] = map(lambda x:x.replace('{{', '').replace('.DATA}}', ''), template['keywords'])
      template['keywords_json'] = json.dumps(template['keywords'])
      # template['keywords'] = json.dumps(template['keywords'])
    if aid:
      return render_to_response('customize/task_add.html', {'active' : 'activity', 'aid' : aid, 'templates' : templates})
    return render_to_response('customize/task_add.html', {'active' : 'task', 'templates' : templates})
  action = request.POST.get('action', None)
  if action not in ['add', 'cancel']:
    return HttpResponse(Response(c=1, m="操作类型错误").toJson(), content_type="application/json")
  if action == 'add':
    return addTask(request)
  return cancelTask(request)

def addTask(request):
  activity = Activity.objects.filter(id=request.POST.get('aid', 0))
  if activity.count() > 0:
    activity = activity[0]
  else:
    activity = None
  task_list = request.POST.get('task_list', None)
  keywords = request.POST.get('keywords', None)
  url = request.POST.get('url', None)
  template_id = request.POST.get('template_id', None)
  template_name = request.POST.get('template_name', None)
  if task_list is None or keywords is None or template_name is None or url is None or template_id is None:
    return HttpResponse(Response(c=2, m='参数不足').toJson(), content_type='application/json')
  task_list = json.loads(task_list)
  for (task_name, run_time) in task_list.iteritems():
    task = Task(template_name=template_name, task_name=task_name, run_time=run_time, keywords=keywords, url=url, template_id=template_id)
    if activity != None:
      task.target = activity.id
      task.target_type = 1
    task.save()
  return HttpResponse(Response(c=0, m="添加任务成功").toJson(), content_type='application/json')

def cancelTask(request):
  tid = request.POST.get('tid', None)
  task = None
  try:
    task = Task.objects.get(id=tid)
  except:
    return HttpResponse(Response(c=1, m="待取消任务不存在").toJson(), content_type='application/json')
  if task.run_time <= timezone.now() or task.status != 0:
    return HttpResponse(Response(c=2, m="无法取消已执行的任务").toJson(), content_type='application/json')
  task.status = 2
  task.save()
  return HttpResponse(Response(c=0, m='任务取消成功').toJson(), content_type='application/json')

def taskHandler(request):
  aid = request.GET.get('aid', 0)
  activity = Activity.objects.filter(id=aid)
  if activity.count() <= 0:
    tasks = Task.objects.filter(target_type=0).order_by('-create_time')
    active = 'task'
  else:
    tasks = Task.objects.filter(target_type=1).filter(target=aid).order_by('-create_time')
    active = 'activity'
  for index, task in enumerate(tasks):
    tasks[index].keywords = json.loads(task.keywords)
  if active == 'task':
    return render_to_response('customize/task_list.html', {'active' : active, 'tasks' : tasks})
  return render_to_response('customize/task_list.html', {'active' : active, 'tasks' : tasks, 'aid' : aid})

def list_statistic(request):
  activity_list = Activity.objects.order_by('-create_time')
  return render_to_response('customize/statistic_list.html', {'active' : 'statistic', 'activity_list' : activity_list})