#coding:utf-8

class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

import sys
sys.modules[__name__] = _const()

const = _const

# 要定义统一管理的常量写在这里

# 请求
const.HTTP_REQUEST_TYPE_CODE_REGISTER = 11                  # 请求注册
const.HTTP_REQUEST_TYPE_CODE_PHONE_LOGIN = 13               # 登录请求
const.HTTP_REQUEST_TYPE_CODE_GET_FRIENDS_INFO = 15          # 请求好友信息

# 响应
const.HTTP_RESPONSE_TYPE_CODE_REGISTER_SUCCESS = 12         # 注册成功
const.HTTP_RESPONSE_TYPE_CODE_REGISTER_PHONE_REPEAT = 14    # 注册手机号重复，注册失败
const.HTTP_RESPONSE_TYPE_CODE_LOGIN_PHONE_NOT_EXIST = 16    # 请求登录，但手机号尚未注册
const.HTTP_RESPONSE_TYPE_CODE_LOGIN_PASSWORD_ERROR = 18     # 请求登录，但密码错误
const.HTTP_RESPONSE_TYPE_CODE_LOGIN_SUCCESS = 20            # 请求登录，且登录成功
const.HTTP_RESPONSE_TYPE_CODE_GET_FRIENDS_INFO = 22         # 从登陆页面登陆进主页面后请求获取好友信息的响应码，表示请求到了好友信息
const.HTTP_RESPONSE_TYPE_CODE_GET_FRIENDS_INFO_NULL = 24    # 从登陆页面登陆进主页面后请求获取好友信息的响应码，表示没有好友

# const.LOGIN_SUCCESS = 15  #
# const.LOGIN_SUCCESS = 16  #
# const.LOGIN_SUCCESS = 17  #
# const.LOGIN_SUCCESS = 18  #
# const.LOGIN_SUCCESS = 19  #
# const.LOGIN_SUCCESS = 20  #
