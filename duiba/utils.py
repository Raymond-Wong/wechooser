# -*- coding: utf-8 -*-

import os
import hashlib

# 获取duiba的签名规则
def getSignStr(p, appSecret):
  params = p.copy()
  params['appSecret'] = appSecret
  params = sorted(params.iteritems(), key=lambda x:x[0], reverse=False)
  paramsList = map(lambda x:x[1], params)
  sortedParamsStr = ''.join(paramsList)
  encoder = hashlib.md5()
  encoder.update(sortedParamsStr)
  return encoder.hexdigest()

# 将参数中为空的key过滤掉
def filterParam(params):
  for k in params.keys():
    if not params[k]:
      params.pop(k)
  return params

# 将请求中的参数变成字典
def request2dict(request, keys):
  ret = {}
  for k in keys:
    if request.get(k, None):
      ret[k] = request.get(k, None)
  return ret