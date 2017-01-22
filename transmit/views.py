# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
from PIL import Image, ImageDraw, ImageFont
import qrcode
import time
import StringIO
import json
import re
from datetime import timedelta, datetime

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone

from wechooser.utils import Response, send_request
from wechooser.decorator import wx_logined, has_token, is_logined
from duiba.models import Credit_Record
from wechat.models import User
from wechat.ReplyTemplates import *
from models import Name_Card, Activity, Participation
from customize.models import Task
from wechooser.settings import WX_APPID, WX_SECRET, WX_TOKEN
import utils
import wechat.utils
import wechooser.utils
from django.template import Context, Template

@is_logined
def activity_list(request):
  released = Activity.objects.filter(release_state=1)
  unreleased = Activity.objects.filter(release_state=0)
  # 设置一个假用户
  user = User()
  user.headimg = '%s/static/transmit/images/headimg.jpg' % sys.path[0]
  user.nickname = u'用户昵称'
  for index, item in enumerate(released):
    state, img = get_name_card(user, item.name_card)
    if state:
      released[index].name_card_img = utils.image_to_base64(img)
  for index, item in enumerate(unreleased):
    state, img = get_name_card(user, item.name_card)
    if state:
      unreleased[index].name_card_img = utils.image_to_base64(img)
  return render_to_response('transmit/activity_list.html', {'active' : 'activity', 'released' : released, 'unreleased' : unreleased})

# 显示名片
@wx_logined
def showNameCard(request):
  user = User.objects.get(wx_openid=request.session['user'])
  if Activity.objects.filter(id=request.GET.get('aid', '0')).count() < 0:
    return HttpResponse(Response(c=1, m="活动不存在").toJson(), content_type="application/json")
  activity = Activity.objects.get(id=request.GET.get('aid'))
  participate = Participation.objects.filter(user=user).filter(activity=activity)
  if participate.count() > 0:
    participate = participate[0]
  else:
    participate = Participation(user=user, activity=activity)
    state, qrcode = wechat.utils.update_user_qrcode(user, activity, token)
    if not state:
      return HttpResponse(Response(c=1, m="生成邀请二维码失败").toJson(), content_type="application/json")
    participate.qrcode_url = qrcode[0]
    participate.qrcode_ticket = qrcode[1]
    participate.save()
  state, img = get_name_card(user, activity.name_card, participate)
  return render_to_response('transmit/showNameCard.html', {'image' : utils.image_to_base64(img)})

@csrf_exempt
@is_logined
def release(request):
  aid = request.POST.get('aid', None)
  if aid is None or Activity.objects.filter(id=aid).count() <= 0:
    return HttpResponse(Response(c=1, m='待发布活动不存在').toJson(), content_type='application/json')
  activity = Activity.objects.get(id=aid)
  activity.release_state = 1
  activity.save()
  return HttpResponse(Response().toJson(), content_type='application/json')

@csrf_exempt
@is_logined
def delete(request):
  aid = request.POST.get('aid', None)
  if aid is None or Activity.objects.filter(id=aid).count() <= 0:
    return HttpResponse(Response(c=1, m='待删除活动不存在').toJson(), content_type='application/json')
  activity = Activity.objects.get(id=aid)
  # 删除活动相关的名片
  activity.name_card.delete()
  # 删除活动相关的任务
  tasks = Task.objects.filter(target_type__in=[1, 3]).filter(target=activity.id)
  for task in tasks:
    task.delete()
  # 删除和活动相关的用户关系
  participates = activity.participation_set.all()
  for p in participates:
    p.delete()
  activity.delete()
  return HttpResponse(Response().toJson(), content_type='application/json')

# 获取名片卡
@csrf_exempt
@is_logined
def getNameCard(request):
  card = Name_Card()
  bg = request.POST.get('bg', None)
  card.bg = bg if bg is not None else card.bg
  head_diameter = request.POST.get('head_diameter', None)
  card.head_diameter = head_diameter if head_diameter is not None else card.head_diameter
  head_x = request.POST.get('head_x', None)
  card.head_x = head_x if head_x is not None else card.head_x
  head_y = request.POST.get('head_y', None)
  card.head_y = head_y if head_y is not None else card.head_y
  name_fontsize = request.POST.get('name_fontsize', None)
  card.name_fontsize = name_fontsize if name_fontsize is not None else card.name_fontsize
  name_y = request.POST.get('name_y', None)
  card.name_y = name_y if name_y is not None else card.name_y
  qrcode_x = request.POST.get('qrcode_x', None)
  card.qrcode_x = qrcode_x if qrcode_x is not None else card.qrcode_x
  qrcode_y = request.POST.get('qrcode_y', None)
  card.qrcode_y = qrcode_y if qrcode_y is not None else card.qrcode_y
  qrcode_size = request.POST.get('qrcode_size', None)
  card.qrcode_size = qrcode_size if qrcode_size is not None else card.qrcode_size
  target = request.POST.get('target', None)
  card.target = target if target is not None else card.target
  user = User()
  user.headimg = '%s/static/transmit/images/headimg.jpg' % sys.path[0]
  user.nickname = u'用户昵称'
  state, img = get_name_card(user, card)
  img = utils.image_to_base64(img)
  return HttpResponse(Response(m=img).toJson(), content_type='application/json')

# 获取达到邀请人数后的人数目标
def getGoalMsg(request):
  user = request.GET.get('id', None)
  activity = request.GET.get('aid', None)
  try:
    user = User.objects.get(wx_openid=user)
    activity = Activity.objects.get(id=activity)
  except Exception, e:
    raise Http404
  state, namecard = get_template(aid=activity.id)
  if Participation.objects.filter(invited_by=user).filter(activity=activity).count() < namecard.target:
    raise Http404
  return render_to_response('transmit/getGoalMsg.html', {'msg' : namecard.goal_msg})

@is_logined
@has_token
def activity_set(request, token):
  # 获取图片模板
  activity = None
  if request.GET.has_key('aid') and Activity.objects.filter(id=request.GET.get('aid')).count() == 1:
    activity = Activity.objects.get(id=request.GET.get('aid'))
    template = activity.name_card
    url = 'http://' + request.get_host() + '/transmit/showNameCard?aid=' + str(activity.id)
    action = 'update'
  else:
    template = Name_Card()
    url = '暂未生效'
    action = 'add'
  templates = wechat.utils.get_template_msg_list(token)
  for temp_msg in templates:
    temp_msg['keywords'] = re.findall('{{.+\.DATA}}.*', temp_msg['content'])
    temp_msg['keywords'] = map(lambda x:x.replace('{{', '').replace('.DATA}}', ''), temp_msg['keywords'])
    temp_msg['keywords_json'] = json.dumps(temp_msg['keywords'])
  # 处理达成目标后的回复消息
  tasks = None
  if activity:
    tasks = Task.objects.filter(target_type=3).filter(target=activity.id)
    for task in tasks:
      task.run_time = (task.run_time - task.create_time).seconds / 60
      task.keywords = json.loads(task.keywords)
      task.news_item = json.loads(task.news_item)
  # 处理接受邀请后的回复消息
  if template.invited_msg != '':
    invited_msg = json.loads(template.invited_msg)
    if invited_msg['MsgType'] == 'image':
      invited_msg['ImageUrl'] = wechat.utils.getBase64Img(oriUrl=invited_msg['OriUrl'], mediaId=invited_msg['MediaId'])
    elif invited_msg['MsgType'] == 'voice':
      invited_msg['VoiceLen'] = wechat.utils.getOneVoiceLen(mediaId=invited_msg['MediaId'])
    elif invited_msg['MsgType'] == 'news':
      for news in invited_msg['Items']:
        news['ImageUrl'] = wechat.utils.getBase64Img(oriUrl=news['PicUrl'], mediaId=news['MediaId'])
    template.invited_msg = json.dumps(invited_msg)
  return render_to_response('transmit/activity_set.html', {'achieve_msg_list' : tasks, 'templates' : templates, 'action' : action, 'active' : 'activity', 'template' : template, 'url' : url, 'activity' : activity})

@csrf_exempt
@is_logined
def save(request):
  aid = request.GET.get('aid', None)
  activity = None
  card = None
  action = None
  if aid is None or Activity.objects.filter(id=aid).count() <= 0:
    card = Name_Card()
    activity = Activity()
    action = 'add'
  else:
    activity = Activity.objects.get(id=aid)
    card = activity.name_card
    action = 'update'
  # 创建卡片
  bg = request.POST.get('bg', None)
  card.bg = bg if bg is not None else card.bg
  head_diameter = request.POST.get('head_diameter', None)
  card.head_diameter = head_diameter if head_diameter is not None else card.head_diameter
  head_x = request.POST.get('head_x', None)
  card.head_x = head_x if head_x is not None else card.head_x
  head_y = request.POST.get('head_y', None)
  card.head_y = head_y if head_y is not None else card.head_y
  name_fontsize = request.POST.get('name_fontsize', None)
  card.name_fontsize = name_fontsize if name_fontsize is not None else card.name_fontsize
  name_y = request.POST.get('name_y', None)
  card.name_y = name_y if name_y is not None else card.name_y
  qrcode_x = request.POST.get('qrcode_x', None)
  card.qrcode_x = qrcode_x if qrcode_x is not None else card.qrcode_x
  qrcode_y = request.POST.get('qrcode_y', None)
  card.qrcode_y = qrcode_y if qrcode_y is not None else card.qrcode_y
  qrcode_size = request.POST.get('qrcode_size', None)
  card.qrcode_size = qrcode_size if qrcode_size is not None else card.qrcode_size
  target = request.POST.get('target', None)
  card.target = target if target is not None else card.target
  card.invite_msg = request.POST.get('invite_msg', '')
  # 处理回复模板
  invited_msg = request.POST.get('invited_msg', '')
  invited_msg = json.loads(invited_msg)
  if invited_msg['MsgType'] == 'text':
    invited_msg = TextTemplate(Content=invited_msg['Content'])
  elif invited_msg['MsgType'] == 'image':
    invited_msg = ImageTemplate(MediaId=invited_msg['MediaId'], OriUrl=invited_msg['OriUrl'])
  elif invited_msg['MsgType'] == 'voice':
    invited_msg = VoiceTemplate(MediaId=invited_msg['MediaId'], VoiceName=invited_msg['VoiceName'])
  elif invited_msg['MsgType'] == 'video':
    invited_msg = VideoTemplate(MediaId=invited_msg['MediaId'], Title=invited_msg['Title'], Description=invited_msg['Description'])
  elif invited_msg['MsgType'] == 'news':
    newsItems = []
    for item in invited_msg['item']:
      newsItems.append(NewsItem(MediaId=item['MediaId'], Title=item['Title'], Description=item['Description'], Url=item['Url'], PicUrl=item['PicUrl']))
    invited_msg = NewsTemplate(MediaId=invited_msg['MediaId'], Items=newsItems)
  card.invited_msg = json.dumps(invited_msg, default=wechooser.utils.dumps)
  card.gain_card_method = request.POST.get('gain_card_method', 'text')
  card.mid = request.POST.get('mid', '')
  card.keyword = request.POST.get('keyword', '')
  # 创建活动
  activity.name = request.POST.get('name', '')
  # 保存
  card.save()
  activity.name_card = card
  activity.save()
  # 保存活动的达成目标消息
  achieve_msg_list = request.POST.get('achieveMsg', [])
  if len(achieve_msg_list) == 0:
    return HttpResponse(Response(c=1, m="活动至少有一条达成目标回复消息").toJson(), content_type="application/json")
  achieve_msg_list = json.loads(achieve_msg_list)
  now = timezone.now()
  used_tasks = []
  for achieve_msg in achieve_msg_list:
    task = None
    if achieve_msg.has_key('id'):
      task = Task.objects.get(id=achieve_msg['id'])
    else:
      task = Task(target=activity.id)
    task.task_name = achieve_msg['task_name']
    task.create_time = now
    task.run_time = now + timedelta(minutes=int(achieve_msg['run_time']))
    task.keywords = json.dumps(achieve_msg['keywords'])
    task.url = achieve_msg['url']
    task.template_id = achieve_msg['template_id']
    task.template_name = achieve_msg['template_name']
    task.target_type = '3'
    task.target = activity.id
    task.news_item = achieve_msg['news_item']
    task.news_item['url'] = task.url
    task.news_item = json.dumps(task.news_item)
    task.save()
    used_tasks.append(task.id)
  # 删除无用回复消息
  for task in Task.objects.filter(target_type=3).filter(target=activity.id):
    if task.id not in used_tasks:
      task.delete()
  # 返回活动id和url
  ret = {}
  ret['action'] = action
  ret['aid'] = activity.id
  ret['url'] = 'http://wechooser.applinzi.com/transmit/showNameCard?aid=%d' % activity.id
  return HttpResponse(Response(m=json.dumps(ret)).toJson(), content_type="application/json")

def get_name_card(user, template=None, participate=None):
  # 如果调用参数时未提供模板，则从数据库中查询最新保存的模板
  if template == None:
    templates = Name_Card.objects.order_by('-create_time')
    if len(templates) <= 0:
      return False, None
    else:
      template = templates[0]
  # 获取用户头像
  try:
    headimg = utils.string_to_image(utils.get_head_image(user.headimgurl, 96))
  except:
    headimg = Image.open(user.headimg)
  # 申明一个图像处理对象
  processer = utils.PyImageProcesser()
  # 将用户头像转换成圆形
  headimg = processer.to_circle(headimg)
  # 打开背景图片
  try:
    # 尝试从本地打开背景图片
    bg_path = sys.path[0] + template.bg
    bg = Image.open(bg_path).convert('RGBA')
  except:
    # 如果打开失败，则从网络上下载背景图片
    bg = utils.string_to_image(utils.download_image(template.bg))
  # 将用户头像和背景图片结合
  size = (bg.size[0] * float(template.head_diameter), bg.size[0] * float(template.head_diameter))
  pos = (bg.size[0] * float(template.head_x), bg.size[1] * float(template.head_y))
  bg = processer.combine(bg, headimg, size, pos)
  # 在上面得到的背景图片的某个垂直位置放置一个水平居中的用户昵称
  font_path = '%s/static/transmit/fonts/deng.ttf' % sys.path[0]
  y = bg.size[1] * float(template.name_y)
  pos = (int(template.name_padding), int(template.name_padding))
  font_size = int(template.name_fontsize)
  bg = processer.center_text(bg, user.nickname, y, pos, font_size=font_size, font_color="white", font=font_path)
  # 根据用户id生成一个二维码
  coder = qrcode.QRCode(version=5, border=1)
  if participate == None:
    participate = Participation(qrcode_url='用户名片效果预览二维码')
  coder.add_data(participate.qrcode_url)
  coder.make(fit=True)
  qr_img = coder.make_image()
  # 将二维码和背景图片合并
  size = (bg.size[0] * float(template.qrcode_size), bg.size[0] * float(template.qrcode_size))
  pos = (bg.size[0] * float(template.qrcode_x), bg.size[1] * float(template.qrcode_y))
  bg = processer.combine(bg, qr_img, resize=size, pos=pos, alpha=False)
  return True, utils.image_to_string(bg)

# 获取名片的mediaid
def get_name_card_mediaid(user, aid, token):
  # 获取namecard图片对象
  if Activity.objects.filter(id=aid).count() <= 0:
    return False, None
  activity = Activity.objects.get(id=aid)
  # 获取用户和活动的关系
  participate = Participation.objects.filter(activity=activity).filter(user=user)
  # 如果用户没有还没有参加活动
  if participate.count() <= 0:
    participate = Participation(user=user, activity=activity)
    state, qrcode = wechat.utils.update_user_qrcode(user, activity, token)
    if not state:
      return False, None
    participate.qrcode_url = qrcode[0]
    participate.qrcode_ticket = qrcode[1]
    participate.save()
  else:
    participate = participate[0]
  state, namecard = get_name_card(user, template=activity.name_card, participate=participate)
  if not state:
    return False, None
  # 上传临时素材获取mediaid
  timestamp = str(int(time.time() * 1000))
  filename = '%s_%s.jpg' % (user.wx_openid, timestamp)
  resp = wechat.utils.upload_tmp_material(filename, StringIO.StringIO(namecard), 'image', token)
  return True, resp['media_id']

# 用户被其他用户邀请的事件
def invited_by(user, dictionary):
  # 获取participate
  participate = Participation.objects.filter(qrcode_ticket=dictionary['Ticket'])
  if participate.count() <= 0:
    return False, '邀请链接已失效'
  participate = participate[0]
  # 如果用户邀请自己
  if participate.user == user:
    return False, '不能邀请自己'
  invite_user = participate.user
  if user.source_type != 3:
    if (timezone.now() - invite_user.last_interact_time).total_seconds() <= (48 * 60 * 60):
      warn = TextTemplate(ToUserName=invite_user.wx_openid, FromUserName=dictionary['ToUserName'], Content="温馨提示，邀请新关注的用户才可以参加本次活动哦！")
      wechat.utils.sendMsgTo(wechat.utils.get_access_token(), warn.toSend())
    return False, '只有新关注用户才能接受活动邀请'
  # 如果用户已经被邀请过了
  new_participate = Participation.objects.filter(user=user).filter(activity=participate.activity)
  if new_participate.count() > 0:
    new_participate = new_participate[0]
    if new_participate.invited_by != None:
      return False, '当前用户已接受过邀请'
  else:
    new_participate = Participation(user=user, activity=participate.activity)
    state, qrcode = wechat.utils.update_user_qrcode(user, participate.activity, wechat.utils.get_access_token())
    if not state:
      return False, '参与活动失败'
    new_participate.qrcode_url = qrcode[0]
    new_participate.qrcode_ticket = qrcode[1]
  new_participate.invited_by = invite_user
  new_participate.save()
  # 检查邀请用户是否达到目标值
  state, namecard = get_template(aid=participate.activity.id)
  if not state:
    return False, namecard
  if Participation.objects.filter(invited_by=invite_user).filter(activity=participate.activity).count() == namecard.target:
    now = datetime.strptime(timezone.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
    print '用户%s的完成活动%s的时间为%s' % (invite_user.nickname, participate.activity.name, now.strftime("%Y-%m-%d %H:%M:%S"))
    now = now + timedelta(seconds=60)
    # 获取这个活动的所有延迟发送任务
    msg_list = Task.objects.filter(target_type=3).filter(target=participate.activity.id)
    for msg in msg_list:
      # 如果消息为立即发送，则直接发送
      if msg.run_time == msg.create_time:
        if (invite_user.last_interact_time - timezone.now()).total_seconds() <= 48 * 60 * 60:
          news_item = json.loads(msg.news_item)
          wechat.utils.send_news_item_msg(wechat.utils.get_access_token(), invite_user.wx_openid, news_item)
        else:
          wechat.utils.send_template_msg(invite_user.wx_openid, msg.template_id, msg.url, json.loads(msg.keywords))
        continue
      task = Task(news_item=msg.news_item, keywords=msg.keywords, url=msg.url, task_name=msg.task_name, template_id=msg.template_id, template_name=msg.template_name, target_type=2)
      task.run_time = now + (msg.run_time - msg.create_time)
      task.run_time = task.run_time.replace(second=0).replace(microsecond=0)
      task.target = invite_user.id
      task.save()
  elif (invite_user.last_interact_time - timezone.now()).total_seconds() <= 48 * 60 * 60:
    remain = namecard.target - Participation.objects.filter(invited_by=invite_user).filter(activity=participate.activity).count()
    msg = Template(namecard.invite_msg).render(Context(dict(username=user.nickname, remain=remain, activity=participate.activity.name)))
    msg = TextTemplate(ToUserName=invite_user.wx_openid, FromUserName=dictionary['ToUserName'], Content=msg)
    wechat.utils.sendMsgTo(wechat.utils.get_access_token(), msg.toSend())
  # 给邀请用户加积分
  credit_diff = 10
  if Participation.objects.filter(invited_by=invite_user).filter(activity=participate.activity).count() <= 50:
    cr = Credit_Record(credit_type=1, user=invite_user, credit_diff=credit_diff)
    cr.save()
    invite_user.credits += credit_diff
    invite_user.save()
  return True, invite_user

def get_template(aid=None, qrcode_ticket=None):
  if aid is not None:
    activity = Activity.objects.filter(id=aid)
    if activity.count() <= 0:
      return False, '活动不存在'
    return True, activity[0].name_card
  elif qrcode_ticket is not None:
    participate = Participation.objects.filter(qrcode_ticket=qrcode_ticket)
    if participate.count() <= 0:
      return False, '邀请链接已失效'
    activity = participate[0].activity
    return True, activity.name_card
  return False, '查找不到活动卡片'

# 判断当前的消息是否复合获取图片的要求
def is_getting_card(dictionary):
  if dictionary['MsgType'] != 'text':
    return False, None
  activitys = Activity.objects.filter(release_state=1).order_by('-create_time')
  for activity in activitys:
    if dictionary['Content'] == activity.name_card.keyword:
      return True, activity.id
  return False, None
