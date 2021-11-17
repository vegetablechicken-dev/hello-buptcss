# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from User.models import User

import hashlib

def NavProcess(request):  # 上下文处理器必须返回一个字典
    context = {}
    if request.session.get('is_login', None):
        # context['test'] = request.session.get('is_login', None)
        context['login_status'] = 'login'
    else:
        context['login_status'] = 'not_login'

    if request.method == 'GET':
        return context

    if request.method == 'POST':
        if 'login' in request.POST:

            username = request.POST.get('usr1', None)
            password = request.POST.get('pwd1', None)

            try:
                user = User.objects.get(username=username)
            except:
                context['login_err'] = '用户名不存在'
                context['open_login'] = True
                return context

            a = hashlib.md5()
            a.update(password.encode())
            password_md5 = a.hexdigest()

            if password_md5 != user.password:
                # print(password_md5)
                context['login_err'] = '密码错误'
                context['open_login'] = True
                return context

            type_code = user.type

            context['login_result'] = 'success'
            request.session['username'] = username
            request.session['is_login'] = True
            request.session['type'] = type_code

            context['refresh'] = True

            return context

        if 'register' in request.POST:
            context = {}

            username = request.POST.get('usr2', None)
            password = request.POST.get('pwd2', None)
            email = request.POST.get('email2', None)
            type = request.POST.get('type', None)

            b = hashlib.md5()
            b.update(password.encode())
            password_md5 = b.hexdigest()  # 加密后

            UserRepeated = User.objects.filter(username=username)
            if UserRepeated:
                context['register_err'] = '用户名已被使用'
                context['open_reg'] = True
                return context

            EmailRepeated = User.objects.filter(email=email)
            if EmailRepeated:
                context['register_err'] = 'email已被使用'
                context['open_reg'] = True
                return context

            if type == 'teacher':
                type_code = 2
            else:
                type_code = 1

            try:
                user = User.objects.create(username=username, password=password_md5, email=email, type=type_code)
            except Exception as e:
                context['register_err'] = '发生错误'
                context['open_reg'] = True
                return context

            user.save()

            request.session['username'] = username
            request.session['is_login'] = True
            request.session['type'] = type_code
            request.session.set_expiry(86400*2)

            # context['register_result'] = 'success'
            context['refresh'] = True

            return context

    return context


