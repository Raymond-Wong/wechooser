# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
from PIL import Image, ImageDraw, ImageFont
import qrcode

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from wechooser.utils import Response, send_request
from wechooser.decorator import wx_logined
from wechat.models import User
from wechooser.settings import WX_APPID, WX_SECRET, WX_TOKEN
import utils

# 获取名片卡
@wx_logined
def getNameCard(request):
  user = User.objects.get(wx_openid=request.session['user'])
  # 获取用户头像
  headimg = utils.string_to_image(utils.get_head_image(user.headimgurl))
  # # 申明一个图像处理对象
  # processer = utils.PyImageProcesser()
  # # 将用户头像转换成圆形
  # headimg = processer.to_circle(headimg)
  # # 打开背景图片
  # bg_path = '%s/static/transmit/images/bg.jpg' % sys.path[0]
  # bg = Image.open(bg_path).convert('RGBA')
  # # 将用户头像和背景图片结合
  # bg = processer.combine(bg, headimg, (80, 80), (184, 202))
  # # 在上面得到的背景图片的某个垂直位置放置一个水平居中的用户昵称
  # font_path = '%s/static/transmit/fonts/Raleway-Regular.ttf' % sys.path[0]
  # bg = processer.center_text(bg, user.nickname, 290, (20, 20), font_size=24, font_color="white", font=font_path)
  # # 根据用户id生成一个二维码
  # coder = qrcode.QRCode(version=5, border=1)
  # coder.add_data(utils.get_user_url(user))
  # coder.make(fit=True)
  # qr_img = coder.make_image()
  # # 将二维码和背景图片合并
  # bg = processer.combine(bg, qr_img, resize=(120, 120), pos=(165, 495), alpha=False)
  img = headimg
  img = utils.image_to_base64(utils.image_to_string(img))
  return render_to_response('transmit/showImage.html', {'image' : img})
