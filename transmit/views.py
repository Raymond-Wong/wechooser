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

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from wechooser.utils import Response, send_request
from wechooser.decorator import wx_logined, has_token
from wechat.models import User
from models import Name_Card
from wechooser.settings import WX_APPID, WX_SECRET, WX_TOKEN
import utils
import wechat.utils

# 获取名片卡
@csrf_exempt
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
  user.qrcode_url = '用户名片效果预览二维码'
  user.nickname = u'用户昵称'
  state, img = get_name_card(user, card)
  img = utils.image_to_base64(img)
  return HttpResponse(Response(m=img).toJson(), content_type='application/json')

# 获取达到邀请人数后的人数目标
def getGoalMsg(request):
  user = request.GET.get('id', None)
  try:
    user = User.objects.get(wx_openid=user)
  except:
    raise Http404
  state, namecard = get_template()
  if not user.user_set.count() >= namecard.target:
    raise Http404
  return render_to_response('transmit/getGoalMsg.html', {'msg' : namecard.goal_msg})

@has_token
def index(request, token):
  # 获取图片模板
  templates = Name_Card.objects.order_by('-create_time')
  template = None
  if len(templates) <= 0:
    template = Name_Card()
  else:
    template = templates[0]
  # 获取菜单
  clickbtns = []
  menuParent = wechat.utils.getMenu(token)
  if menuParent is not None:
    menu = menuParent['menu']['button']
    print '*' * 20, '\n', menu, '\n', '*' * 20
    for flBtn in menu:
      if flBtn.has_key('type') and flBtn['type'] == 'click':
        clickbtns.append({'name' : flBtn['name'], 'mid' : flBtn['key']})
      else:
        if len(flBtn['sub_button']) > 0:
          for slBtn in flBtn['sub_button']:
            if slBtn['type'] == 'click':
              clickbtns.append({'name' : slBtn['name'], 'mid' : slBtn['key']})
  return render_to_response('transmit/transmit.html', {'active' : 'transmit', 'template' : template, 'menu' : clickbtns})

@csrf_exempt
def save(request):
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
  card.invited_msg = request.POST.get('invited_msg', '')
  card.goal_msg = request.POST.get('goal_msg', '')
  card.gain_card_method = request.POST.get('gain_card_method', 'text')
  card.mid = request.POST.get('mid', '')
  card.keyword = request.POST.get('keyword', '')
  card.save()
  return HttpResponse(Response(m="保存成功").toJson(), content_type="application/json")

def get_name_card(user, template=None):
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
  size = (int(template.head_diameter), int(template.head_diameter))
  pos = (int(template.head_x), int(template.head_y))
  bg = processer.combine(bg, headimg, size, pos)
  # 在上面得到的背景图片的某个垂直位置放置一个水平居中的用户昵称
  font_path = '%s/static/transmit/fonts/deng.ttf' % sys.path[0]
  y = int(template.name_y)
  pos = (int(template.name_padding), int(template.name_padding))
  font_size = int(template.name_fontsize)
  bg = processer.center_text(bg, user.nickname, y, pos, font_size=font_size, font_color="white", font=font_path)
  # 根据用户id生成一个二维码
  coder = qrcode.QRCode(version=5, border=1)
  coder.add_data(user.qrcode_url)
  coder.make(fit=True)
  qr_img = coder.make_image()
  # 将二维码和背景图片合并
  size = (int(template.qrcode_size), int(template.qrcode_size))
  pos = (int(template.qrcode_x), int(template.qrcode_y))
  bg = processer.combine(bg, qr_img, resize=size, pos=pos, alpha=False)
  return True, utils.image_to_string(bg)

# 获取名片的mediaid
def get_name_card_mediaid(user, token):
  # 获取namecard图片对象
  state, namecard = get_name_card(user)
  if not state:
    return False, None
  # 上传临时素材获取mediaid
  timestamp = str(int(time.time() * 1000))
  filename = '%s_%s.jpg' % (user.wx_openid, timestamp)
  resp = wechat.utils.upload_tmp_material(filename, StringIO.StringIO(namecard), 'image', token)
  return True, resp['media_id']

# 用户被其他用户邀请的事件
def invited_by(user, dictionary):
  # 如果用户已经被邀请过了
  if user.invited_by:
    return False, '已接受过邀请'
  invite_user = None
  try:
    invite_user = User.objects.get(qrcode_ticket=dictionary['Ticket'])
  except:
    return False, '邀请用户不存在'
  # 如果邀请人和被邀请人是同一个人则返回错误
  if user.wx_openid == invite_user.wx_openid:
    return False, '只能邀请其他用户'
  user.invited_by = invite_user
  user.save()
  # 检查邀请用户是否达到目标值
  state, namecard = get_template()
  if invite_user.user_set.count() >= namecard.target:
    data = {'name' : {'value' : '成功到达邀请人数', 'color' : '#173177'}, 'remark' : {'value' : '点击以获取资料链接', 'color' : '#173177'}}
    wechat.utils.send_template_msg(invite_user.wx_openid, 'Fp7HTtkro57Zk6TXa176vb159uLsld0qEHYH3ro5pAI', 'http://wechooser.applinzi.com/transmit/getGoalMsg?id=%s' % invite_user.wx_openid, data)
  # 给邀请用户加积分
  credit_diff = 10
  if invite_user.user_set.count() <= 50:
    cr = Credit_Record(credit_type=1, user=invite_user, credit_diff=credit_diff)
    cr.save()
    invite_user.credits += credit_diff
    invite_user.save()
  return True, invite_user

def get_template():
  card = Name_Card.objects.order_by('-create_time')
  if len(card) > 0:
    return True, card[0]
  return False, Name_Card()

# 判断当前的消息是否复合获取图片的要求
def is_getting_card(dictionary):
  state, card = get_template()
  # 如果获取图片的要求是1
  if card.gain_card_method == 1 and dictionary['MsgType'] == 'image':
    return True
  elif card.gain_card_method == 2 and dictionary['MsgType'] == 'event' and dictionary['EventKey'] == card.mid:
    return True
  elif card.gain_card_method == 3 and dictionary['MsgType'] == 'text' and dictionary['Content'] == card.keyword:
    return True
  elif card.gain_card_method == 0 and dictionary['MsgType'] == 'text' and not wechat.utils.is_hit_rules(dictionary['Content']):
    return True
  return False
