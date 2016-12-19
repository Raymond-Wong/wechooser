# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import httplib
import urllib
import json
import hashlib
import time
import base64
import eyed3
import os
import StringIO
import requests
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.utils import timezone

from wechat.models import access_token, User, KeywordReply
from wechooser.utils import Response, PastDueException
from wechooser.settings import WX_APPID, WX_SECRET
import wechooser.utils

APPID = WX_APPID
APPSECRET = WX_SECRET

# 获取数据库中access_token的接口
def get_access_token():
  tokens = access_token.objects.order_by('-start_time')
  now = datetime.now()
  if len(tokens) <= 0 or now > tokens[0].end_time:
    most_recent_token = update_token()
  else:
    most_recent_token = tokens[0]
  return most_recent_token

# 当数据库中access_token失效以后用于更新token的接口
def update_token():
  params = {
    'grant_type': 'client_credential',
    'appid': APPID,
    'secret': APPSECRET
  }
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/token'
  method = 'GET'
 
  res = wechooser.utils.send_request(host, path, method, params=params)
  if not res[0]:
    return False
  if res[1].get('errcode'):
    return False
  token = res[1].get('access_token')
  starttime = datetime.now()
  expires_in = timedelta(seconds=int(res[1].get('expires_in')))
  endtime = starttime + expires_in
  token_record = access_token.objects.order_by('-start_time')
  if len(token_record) > 0:
    token_record = token_record[0]
  else:
    token_record = access_token()
  token_record.token = token
  token_record.end_time = endtime
  token_record.save()
  wechooser.utils.logger('DEBUG', u'updating the access token in database: %s' % token_record.token)
  return token_record


# 回复文本信息
def replyMsgTo(_from, _to, createTime, tp, content):
  resp = {}
  resp['FromUserName'] = _from
  resp['ToUserName'] = _to
  resp['CreateTime'] = createTime
  resp['MsgType'] = tp
  resp['Content'] = content
  return HttpResponse(ET.tostring(wechooser.utils.dict2xml(ET.Element('xml'), resp), 'utf-8'))

# 发送文本信息
def sendMsgTo(token, params):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/message/custom/send?access_token='
  method = 'POST'
  wechooser.utils.logger('DEBUG', '发送一条客服消息: %s' % params)
  res = wechooser.utils.send_request(host=host, path=path + token.token, method=method, port=443, params=params)
  return res

def getMaterial(token, tp, offset, count):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/material/batchget_material?access_token='
  method = 'POST'
  params = {'type' : tp, 'offset' : offset, 'count' : count}
  res = wechooser.utils.send_request(host, path + token.token, method, port=443, params=params)
  if res[0]:
    return res[1]
  return {}

def getMaterialCount(token, tp):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/material/get_materialcount'
  method = 'GET'
  params = {'access_token' : token.token}
  res = wechooser.utils.send_request(host, path, method, port=443, params=params)
  if res[0]:
    return res[1][tp + '_count']
  return -1

# 获取菜单接口
def getMenu(token):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/menu/get'
  method = 'GET'
  params = {'access_token' : token.token}
  res = wechooser.utils.send_request(host, path, method, port=443, params=params)
  if res[0]:
    return res[1]
  return None


# 验证信息是否从微信发送过来
def verify(token, timestamp, nonce, signature):
  tmpList = [token, timestamp, nonce]
  tmpList.sort()
  tmpStr = '%s%s%s' % tuple(tmpList)
  tmpStr = hashlib.sha1(tmpStr).hexdigest()
  return tmpStr == signature

# 将素材中的图片url转换成base64编码
def imgUrl2base64(token, materials):
  for count, item in enumerate(materials['item']):
    imgTypeIndex = item['url'].find('wx_fmt')
    imgType = item['url'][imgTypeIndex + 7:]
    mediaId = item['media_id']
    media = getMaterialContent(token, mediaId)
    materials['item'][count]['ori_url'] = materials['item'][count]['url']
    materials['item'][count]['url'] = 'data:image/' + imgType + ';base64,' + base64.b64encode(media)
  return materials

def getNewsInfo(token, materials):
  for i, item in enumerate(materials['item']):
    for j, newsItem in enumerate(item['content']['news_item']):
      imgTypeIndex = newsItem['thumb_url'].find('wx_fmt')
      imgType = newsItem['thumb_url'][imgTypeIndex + 7:]
      mediaId = newsItem['thumb_media_id']
      media = getMaterialContent(token, mediaId)
      materials['item'][i]['content']['news_item'][j]['img'] = 'data:image/' + imgType + ';base64,' + base64.b64encode(media)
      print 'wechat.utils:154', newsItem['url']
  return materials

def getVoiceLen(token, materials):
  for count, item in enumerate(materials['item']):
    # voice = getMaterialContent(token, item['media_id'])
    # name = str(time.time()) + '.mp3';
    # tmpFile = open(name, 'w')
    # tmpFile.write(voice)
    # tmpFile.close()
    materials['item'][count]['length'] = "00:60"
    # os.remove(name)
  return materials

def getVideoInfo(token, materials):
  for count, item in enumerate(materials['item']):
    video = getMaterialContent(token, item['media_id'], toLoad=True)
    materials['item'][count]['description'] = video['description']
    materials['item'][count]['down_url'] = video['down_url']
    materials['item'][count]['title'] = video['title']
  return materials

# 获取永久素材
def getMaterialContent(token, mediaId, toLoad=False):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/material/get_material?access_token='
  method = 'POST'
  params = {'media_id' : mediaId}
  res = wechooser.utils.send_request(host, path + token.token, method, port=443, params=params, toLoad=toLoad)
  if res[0]:
    return res[1]
  return None

def getBase64Img(mediaId, oriUrl):
  imgTypeIndex = oriUrl.find('wx_fmt')
  imgType = oriUrl[imgTypeIndex + 7:]
  token = get_access_token()
  media = getMaterialContent(token, mediaId)
  return 'data:image/' + imgType + ';base64,' + base64.b64encode(media)

def getOneVoiceLen(mediaId):
  return '00:60'

def getOneVideoInfo(template):
  token = get_access_token()
  video = getMaterialContent(token, template['MediaId'], toLoad=True)
  template['VideoName'] = video['title']
  template['VideoTitle'] = video['title']
  template['VideoDesc'] = video['description']
  return template

# 获取关注用户列表
def getUserList(token, next=None):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/user/get'
  method = 'GET'
  params = {'access_token' : token.token}
  if next is not None:
    params['next_openid'] = next
  res = wechooser.utils.send_request(host, path, method, port=443, params=params)
  if res[0]:
    if res[1].has_key('next_openid') and res[1]['next_openid'] != '':
      user_list = res[1]['data']['openid']
      user_list.extend(getUserList(token, res[1]['next_openid']))
      return user_list
    if res[1]['count'] == 0:
      return []
    return res[1]['data']['openid']
  return None

# 获取用户对象
def get_user(openid, token):
  user = None
  try:
    user = User.objects.get(wx_openid=openid)
    if timezone.now() > user.qrcode_expire_time:
      state, qrcode = update_user_qrcode(user, token)
      user.qrcode_url = qrcode[0]
      user.qrcode_ticket = qrcode[1]
      user.qrcode_expire_time = qrcode[2]
      user.save()
    return True, user
  except:
    # 获取用户基本信息
    state, user = update_user(openid, token)
    if not state:
      return False, None
    # 创建用户二维码
    state, qrcode = update_user_qrcode(user, token)
    user.qrcode_url = qrcode[0]
    user.qrcode_ticket = qrcode[1]
    user.qrcode_expire_time = qrcode[2]
    user.save()
    return state, user

def update_user_qrcode(user, token):
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/qrcode/create?access_token='
  method = 'POST'
  params = {}
  params['expire_seconds'] = 2592000
  params['action_name'] = 'QR_SCENE'
  params['action_info'] = {"scene": {"scene_id": user.id}}
  expire_time = timezone.now() + timedelta(seconds=2592000)
  res = wechooser.utils.send_request(host, path + token.token, method, port=443, params=params, toLoad=True)
  if not res[0]:
    return False, None
  res = res[1]
  url = res['url']
  ticket = res['ticket']
  return True, (url, ticket, expire_time)

# 更新数据库中user的信息
def update_user(openid, token):
  user = None
  try:
    user = User.objects.get(wx_openid=openid)
  except:
    user = User()
  params = {}
  params['access_token'] = token.token
  params['openid'] = openid
  params['lang'] = 'zh_CN'
  res = wechooser.utils.send_request('api.weixin.qq.com', '/cgi-bin/user/info', 'GET', params=params)
  if not res[0]:
    return False, HttpResponse(Response(c=2, m="login failed: get user from wechat info failed").toJson(), content_type='application/json')
  userInfo = res[1]
  user.wx_openid = userInfo['openid']
  user.nickname = wechooser.utils.filterEmoji(userInfo['nickname'])
  user.sex = userInfo['sex']
  user.province = userInfo['province']
  user.city = userInfo['city']
  user.country = userInfo['country']
  user.headimgurl = userInfo['headimgurl']
  user.save()
  print 'openid: %s, nickname: %s, id: %s' % (openid, userInfo['nickname'], user.id)
  return True, user

# 上传临时素材
def upload_tmp_material(filename, data, mtype, token):
  params = {}
  params['access_token'] = token.token
  params['type'] = mtype
  url = 'https://api.weixin.qq.com/cgi-bin/media/upload'
  url = '?'.join([url, urllib.urlencode(params)])
  files = {'media' : (filename, data, 'multipart/form-data')}
  resp = requests.post(url, files=files)
  return resp.json()

# 发送模板消息
def send_template_msg(touser, template_id, url, data):
  token = get_access_token()
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/message/template/send?access_token=' + token.token
  method = 'POST'
  params = {'touser' : touser, 'template_id' : template_id, 'url' : url}
  params['data'] = data
  res = wechooser.utils.send_request(host, path, method, port=443, params=params)
  print res
  return res[0]

# 判断是否有击中任何关键词规则
def is_hit_rules(text):
  keywordReplys = KeywordReply.objects.all()
  rules = []
  for keywordReply in keywordReplys:
    if not keywordReply.is_fully_match and keywordReply.keyword in text:
      rules += keywordReply.rule_set.all()
    elif keywordReply.is_fully_match and keywordReply.keyword == text:
      rules += keywordReply.rule_set.all()
  # 如果没有匹配到任意关键词，则返回默认自动回复
  return len(rules) > 0
