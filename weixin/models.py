import json

from django.db import models


# python manage.py makemigrations
# python manage.py migrate

class Person(models.Model):
    user_phone = models.CharField(max_length=15)  # 手机号
    password = models.CharField(max_length=50)  # 密码
    nick_name = models.CharField(max_length=50)  # 昵称
    user_id = models.CharField(max_length=30)  # 微信号
    personality_signature = models.CharField(max_length=60)  # 个性签名(经过查询，可以填写60个字符/30个中文字符)

    # 每个手机号有11个数字 + 1个分隔符 = 12个数字，每个号码可以添加2000个好友 = 2000 * 12 = 24000个字符
    friends = models.CharField(max_length=24000)  # 好友列表，以字符串存储，以e(end)为分割符

    def __str__(self):
        # 此方法相当于Java的.toString方法，直接打印类的时候，会执行此方法
        return self.user_phone
