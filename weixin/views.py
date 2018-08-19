import base64
import os
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import simplejson
import json
from ecdsa import SigningKey

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
                # 密码正确，创建一个json，把响应类型码和正文都返回
                result = {'code': const.HTTP_RESPONSE_TYPE_CODE_LOGIN_SUCCESS, 'content': "登录成功"}
                result = simplejson.dumps(result, cls=QuerySetEncoder)

                # 在models创建一个online字段，如果秘密正确，就判断online是否等于true,如果online，
                # 就离线信息到已经登录的账号上强制离线
                # 如果没有online,则online != online
                return HttpResponse(result)
            else:
                # 密码错误
                result = {'code': const.HTTP_RESPONSE_TYPE_CODE_LOGIN_PASSWORD_ERROR, 'content': "密码错误，请重新输入"}
                result = simplejson.dumps(result, cls=QuerySetEncoder)
                return HttpResponse(result)


def register(request):
    """
    请求注册
    :param request:
    :return: 请求的结果码和结果正文（将封装为Json了）
    """
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


def get_friends_info(request):
    """
    通过登录页面登录进入主页面时候，获取好友信息的请求
    :rtype: object 返回好友信息
    """
    request_content = json.loads(request.body.decode('utf-8'))
    type = request_content.get("type")
    phone = request_content.get("phone")
    if type == const.HTTP_REQUEST_TYPE_CODE_GET_FRIENDS_INFO:  # 再次确认请求类型是否请求好友信息
        person = Person.objects.get(user_phone=phone)  # 找到我的账号，然后查询我账号下的好友
        friends_str = person.friends

        # 如果删除两侧空白字符不为空，说明当前有好友
        if friends_str.strip() != "":
            friends_list = friends_str.split("e")  # 以e分割字符串,获取所有好友列表(好友手机号列表)

            friends_dict = {}

            # 遍历所有好友，取得每个好友的昵称、签名、还有找到头像，并封装到json中，然后返回
            for index, friend_phone in enumerate(friends_list):
                friend = Person.objects.get(user_phone=friend_phone)
                nick_name = friend.nick_name
                personality_signature = friend.personality_signature

                # 二进制方式打开图文件(图片是根据头像的路径+好友手机号+.png)
                f = open('.png'.join(friend_phone.join('upload/image/head_sculpture/')), 'rb')
                head_sculpture_base64 = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
                f.close()

                friend_info_dict = {
                    "nick_name": nick_name,
                    "personality_signature": personality_signature,
                    "head_sculpture_base64": head_sculpture_base64
                }

                friends_dict.update({str(index): friend_info_dict})  # 将单个的好友信息装到好友字典内

            result = {"code": const.HTTP_RESPONSE_TYPE_CODE_GET_FRIENDS_INFO, "content": friends_dict}
            # 最终的结果类似于这样：↓
            # result = {
            #     "code": const.HTTP_RESPONSE_TYPE_CODE_GET_FRIENDS_INFO,
            #     "content": {
            #         "1":{
            #             "nick_name": nick_name,
            #             "personality_signature": personality_signature,
            #             "head_sculpture_base64": head_sculpture_base64
            #             },
            #
            #         "2":{
            #             "nick_name": nick_name,
            #             "personality_signature": personality_signature,
            #             "head_sculpture_base64": head_sculpture_base64
            #             },
            #
            #         "3":{
            #             "nick_name": nick_name,
            #             "personality_signature": personality_signature,
            #             "head_sculpture_base64": head_sculpture_base64
            #             }
            #     }
            # }
            result = simplejson.dumps(result, cls=QuerySetEncoder)
            return HttpResponse(result)
        else:
            result = {"code": const.HTTP_RESPONSE_TYPE_CODE_GET_FRIENDS_INFO_NULL, "content": "你目前没有好友"}
            result = simplejson.dumps(result, cls=QuerySetEncoder)
            return HttpResponse(result)


def add_friends(request):
    # 根据发过来的请求加好友的号码，向那个号码推送一条请求加好友的信息
    # 如果好友返回请求同意添加，就把我的号码添加到好友列表中，并把好友号码添加到我列表中
    # 然后给我回应一个好友添加请求成功，同时请求携带者好友的信息，添加到手机的通讯录列表中
    pass


def search_friends(request):
    # 根据发过来的请求加好友的号码，搜索是否存在那个号码
    # 如果号码存在，则返回那个号码的头像、签名、昵称，并在手机端显示
    # 如果号码不存在，就返回号码不存在
    pass


def send_msg(request):
    """
    发送消息
    :param request:
    """
    # 获取源号码，目标号码，信息，信息类型，并推送到目标号码上
    pass
