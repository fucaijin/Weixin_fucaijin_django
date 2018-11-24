import datetime
import json

from django.db import models


# 在更改models文件后执行以下两行代码，更新数据库结构
# python3 manage.py makemigrations
# python3 manage.py migrate

class Person(models.Model):
    user_phone = models.CharField(max_length=15, null=False)  # 手机号,不可为空
    password = models.CharField(max_length=50, null=False)  # 密码
    nick_name = models.CharField(max_length=50, null=False)  # 昵称
    user_id = models.CharField(max_length=30, default="")  # 微信号,可为空
    personality_signature = models.CharField(max_length=60, default="")  # 个性签名(经过查询，可以填写60个字符/30个中文字符)
    area = models.CharField(max_length=60, default="中国")  # 地区，默认为中国
    sex = models.CharField(max_length=6, default="")  # 性别(male,female)
    birthday = models.CharField(max_length=10, default="")  # 生日 可为空，格式为1991-01-01
    qq = models.CharField(max_length=12, default="")  # qq号(经过查询，最大有12位)

    # 每个手机号有11个数字 + 1个分隔符 = 12个数字，每个号码可以添加2000个好友 = 2000 * 12 = 24000个字符
    friends = models.CharField(max_length=24000, default="")  # 好友列表，以字符串存储，以e(end)为分割符

    def __str__(self):
        # 此方法相当于Java的.toString方法，直接打印类的时候，会执行此方法
        return self.user_phone
