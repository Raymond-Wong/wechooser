# -*- coding: utf-8 -*-

import os
import hashlib

# 获取duiba的签名规则
def getSignStr(params, appSecret):
  paramsList = []
  for k in params.keys():
    if params[k]:
      paramsList.append(params[k])
  paramsList.append(appSecret)
  paramsList = sorted(paramsList)
  sortedParamsStr = ''.join(paramsList)
  encoder = hashlib.md5()
  encoder.update(sortedParamsStr)
  return encoder.hexdigest()