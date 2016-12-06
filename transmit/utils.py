# -*- coding: utf-8 -*-
import urllib2
import cookielib
import base64

# 根据url获取用户头像
def get_head_image(url):
  try:
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    operate = opener.open(req)
    data = operate.read()
    return data
  except Exception, e:
    print e
    return None

# 将图片文件转换成base64字符串
def image_to_base64(image):
  return 'data:image/jpg;base64,' + base64.b64encode(image)