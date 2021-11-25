# -*- coding: utf-8 -*-
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=36, null=False, blank=False, primary_key=True)
    password = models.CharField(max_length=50, null=False, blank=False)  # MD5存储
    email = models.CharField(max_length=40, null=True, default="")
    exp = models.IntegerField(null=False, default=0)
    introduction = models.CharField(max_length=10000, null=True, default='这个人没有写下简介。')

    type = models.IntegerField(null=False, default=1)  # 1：学生 2：教师

    objects = models.Manager()
    def _str_(self):
        return 'username %s'%(self.username)

class UserLoginData(models.Model):
    username = models.CharField(max_length=36, null=False, blank=False, primary_key=True)
    logintime = models.DateTimeField(auto_now=True)