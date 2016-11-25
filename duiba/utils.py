# -*- coding: utf-8 -*-

import os
import hashlib

# 获取duiba的签名规则
def getSignStr(params, appSecret):
  paramsList = params.values()
  paramsList.append(appSecret)
  paramsList = sorted(paramsList)
  sortedParamsStr = ''.join(paramsList)
  print sortedParamsStr
  encoder = hashlib.md5()
  encoder.update(sortedParamsStr)
  return encoder.hexdigest()

# 将参数中为空的key过滤掉
def filterParam(params):
  for k in params.keys():
    if not params[k]:
      params.pop(k)
  return params