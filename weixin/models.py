from django.db import models


# python manage.py makemigrations
# python manage.py migrate

class Person(models.Model):
    user_phone = models.CharField(max_length=15)  # 手机号
    password = models.CharField(max_length=50)  # 密码
    nick_name = models.CharField(max_length=50)  # 昵称
    user_id = models.CharField(max_length=30)  # 微信号

    def __str__(self):
        # 此方法相当于Java的.toString方法，直接打印类的时候，会执行此方法
        return self.user_phone
