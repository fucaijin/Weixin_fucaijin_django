import base64
import os
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import simplejson
import json

from weixin import const  # 自定义的常量的工具类
from weixin.models import Person


class QuerySetEncoder(simplejson.JSONEncoder):
    """
    Encoding QuerySet into JSON format.
    """

    def default(self, object):
        try:
            return serializers.serialize("python", object, ensure_ascii=False)
        except:
            return simplejson.JSONEncoder.default(self, object)


def login(request):
    request_content = json.loads(request.body.decode('utf-8'))
    # request.body 得到的是bytes类型的数据，先解码为str类型，
    # 也就是说request.body.decode()的结果是一个json字符串，此时json.loads（）转为Python字典
    type = request_content.get("type")
    phone = request_content.get("phone")
    password = request_content.get("password")

    if type == const.HTTP_REQUEST_TYPE_CODE_PHONE_LOGIN:
        # 如果是手机登录
        try:
            person = Person.objects.get(user_phone=phone)  # 查询是否存在此号码，存在则获取此号码所在的对象
        except ObjectDoesNotExist:
            # 如果号码不存在
            result = {'code': const.HTTP_RESPONSE_TYPE_CODE_LOGIN_PHONE_NOT_EXIST, 'content': "该手机号码未注册"}
            result = simplejson.dumps(result, cls=QuerySetEncoder)
            return HttpResponse(result)
        else:
            # 手机号存在，判断密码是否正确
            if person.password == password:
                result = {'code': const.HTTP_RESPONSE_TYPE_CODE_LOGIN_SUCCESS, 'content': "登录成功"}
                result = simplejson.dumps(result, cls=QuerySetEncoder)
                return HttpResponse(result)
            else:
                result = {'code': const.HTTP_RESPONSE_TYPE_CODE_LOGIN_PASSWORD_ERROR, 'content': "密码错误，请重新输入"}
                result = simplejson.dumps(result, cls=QuerySetEncoder)
                return HttpResponse(result)


def register(request):
    request_content = json.loads(request.body.decode('utf-8'))
    # request.body 得到的是bytes类型的数据，先解码为str类型，
    # 也就是说request.body.decode()的结果是一个json字符串，此时json.loads（）转为Python字典
    type = request_content.get("type")
    nick_name = request_content.get("nickName")
    user_phone = request_content.get("phone")
    password = request_content.get("password")

    if type == const.HTTP_REQUEST_TYPE_CODE_REGISTER:  # 再次确认请求类型是否是注册
        try:
            Person.objects.get(user_phone=user_phone)  # 从数据库中查询user_phone字段，查询user_phone字段是否含有传过来的user_phone
        except ObjectDoesNotExist:
            # 如果查询数据库中的user_phone字段没有传过来的phone，则会报错然后走到这里
            Person.objects.create(user_phone=user_phone, password=password, nick_name=nick_name)

            # 创建Json对象并进行相应的处理
            result = {'code': const.HTTP_RESPONSE_TYPE_CODE_REGISTER_SUCCESS, 'content': "注册成功"}
            result = simplejson.dumps(result, cls=QuerySetEncoder)

            # 取出上传头像解码
            headPicture = request_content.get("headPicture")
            imgdata = base64.b64decode(headPicture)

            # 判断头像文件夹是否存在,如果不存在则创建
            head_sculpture_dirs = 'upload/image/head_sculpture/'
            if not os.path.exists(head_sculpture_dirs):
                os.makedirs(head_sculpture_dirs)

            # 保存图片
            file = open(head_sculpture_dirs + user_phone + '.png', 'wb')
            file.write(imgdata)
            file.close()

            # 把json传回客户端
            return HttpResponse(result)
        else:
            result = {'code': const.HTTP_RESPONSE_TYPE_CODE_REGISTER_PHONE_REPEAT, 'content': "该手机号码已注册"}
            result = simplejson.dumps(result, cls=QuerySetEncoder)
            return HttpResponse(result)
