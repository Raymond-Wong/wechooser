# -*- coding: utf-8 -*-
import urllib2
import cookielib
import base64
import random
import qrcode
import StringIO
from PIL import Image, ImageDraw, ImageFont

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

# 将一个图像的字符串转换成PIL的图片
def string_to_image(buf):
  return Image.open(StringIO.StringIO(buf))

# 将一个PIL的图片对象转换成一个文件字符串
def image_to_string(img, format='jpeg'):
  output = StringIO.StringIO()
  img.save(output, format)
  buf = output.getvalue()
  output.close()
  return buf

# 图像处理类
class PyImageProcesser:
  # 构造函数
  def __init__(self):
    self.id = random.randint(0, 100)
  # 截取出图片的中心的正方形部分
  def smart_square(self, img):
    size = img.size
    radius = min(size[:2])
    if size[0] != size[1]:
      cropBox = [None, None, None, None]
      cropBox[0] = 0 if size[1] > size[0] else ((size[0] - size[1]) / 2)
      cropBox[1] = 0 if size[0] > size[1] else ((size[1] - size[0]) / 2)
      cropBox[2] = cropBox[0] + radius
      cropBox[3] = cropBox[1] + radius
      img = img.crop(tuple(cropBox))
    return img
  # 将图像切割成圆形
  def to_circle(self, img):
    # 如果图像的色彩模式不为RGBA，则转换为RGBA
    if img.mode != 'RGBA':
      img = img.convert('RGBA')
    img = self.smart_square(img)
    radius = min(img.size)
    circle = Image.new('L', (radius, radius), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius, radius), fill=255)
    alpha = Image.new('L', (radius, radius), 255)
    alpha.paste(circle, (0, 0))
    img.putalpha(alpha)
    return img
  # 将img2粘贴在图片1上
  def combine(self, img1, img2, resize=None, pos=None, alpha=True):
    # 如果需要缩放
    if resize:
      img2 = img2.resize(resize)
    pos = (0, 0) if not pos else pos
    if alpha:
      img1.paste(img2, pos, img2)
    else:
      img1.paste(img2, pos)
    return img1
  # 在图片上添加文字
  def draw_text(self, img, text, pos=(0, 0), font='./Deng.ttf', font_size=20, font_color=(0, 0, 0, 1)):
    font = ImageFont.truetype(font, font_size)
    draw = ImageDraw.Draw(img)
    draw.text(pos, text, font=font, fill=font_color)
    return img
  # 在图片的某个具体高度写入一行居中的字体
  def center_text(self, img, text, y, padding=(0, 0), font='./Deng.ttf', font_size=20, font_color=(0, 0, 0, 1)):
    font_family = ImageFont.truetype(font, font_size)
    # ellipsis
    to_long = False
    while font_family.getsize(text + '...')[0] > (img.size[0] - sum(padding)):
      to_long = True
      text = text[:-2]
    text = text + ('...' if to_long else '')
    # 设置位置
    x = (img.size[0] - sum(padding) - font_family.getsize(text)[0]) / 2 + padding[0]
    img = self.draw_text(img, text, (x, y), font, font_size, font_color)
    return img

# 获取用户的邀请链接
def get_user_url(user):
  return 'www.baidu.com'

if __name__ == '__main__':
  # 假装用户头像已经获取到了
  img = Image.open('./faces.png')
  # 申明一个图像处理对象
  processer = PyImageProcesser()
  # 将用户头像转换成圆形
  img = processer.to_circle(img)
  # 打开背景图片
  bg = Image.open('bg.jpg').convert('RGBA')
  # 将用户头像和背景图片结合
  bg = processer.combine(bg, img, (80, 80), (184, 202))
  # 在上面得到的背景图片的某个垂直位置放置一个水平居中的用户昵称
  bg = processer.center_text(bg, u"用户昵称", 290, (20, 20), font_size=24, font_color="white")
  # 根据用户id生成一个二维码
  coder = qrcode.QRCode(version=5, border=1)
  coder.add_data('http://www.baidu.com')
  coder.make(fit=True)
  qr_img = coder.make_image()
  # 将二维码和背景图片合并
  bg = processer.combine(bg, qr_img, resize=(120, 120), pos=(165, 495), alpha=False)
  bg.show()