# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse

from User.models import User
from Class.models import *
from Course.models import *
from Problem.models import *

import hashlib



def UpdateInfo(request):
    if request.session.get('is_login'):
        CurrentUserName = request.session.get('username')
        context = {}
        if CurrentUserName:
            context['user'] = User.objects.get(username=CurrentUserName)

            if request.method == 'GET':
                return render(request, 'UserInfo.html', context)

        if request.method == 'POST':
            NewInfo = User.objects.get(username=CurrentUserName)

            NewInfo.username = request.POST.get('username')
            if User.objects.get(username=CurrentUserName).username != NewInfo.username:
                IsRepeated = User.objects.filter(username=NewInfo.username)
                if IsRepeated: #判断有无重复
                    # return HttpResponse("<script>alert('用户名已存在!');</script>")
                    context['update_result'] = '用户名已被使用'
                    context['alert_type'] = 'error'
                    return render(request, 'UserInfo.html', context)

            NewInfo.email = request.POST.get('email')
            if User.objects.get(username=CurrentUserName).email != NewInfo.email:
                IsRepeated = User.objects.filter(email=NewInfo.email)
                if IsRepeated: #判断有无重复
                    # return HttpResponse("<script>alert('email已存在！');window.location.go(-1);</script>")
                    context['update_result'] = 'email已被使用'
                    context['alert_type'] = 'error'
                    return render(request, 'UserInfo.html', context)

            NewInfo.introduction = request.POST.get('introduce')

            # NewInfo.classes = User.objects.get(id=CurrentUserId).classes
            # NewInfo.picture = User.objects.get(id=CurrentUserId).picture

            NewInfo.save()

            # return redirect("/my")
            context['user'] = User.objects.get(username=CurrentUserName)
            context['update_result'] = '更新成功'
            context['alert_type'] = 'success'
            return render(request, 'UserInfo.html', context)

        else:
            return redirect('/login_prompt')

def Password(request):
    if request.session.get('is_login'):
        context = {}
        UserName = request.session.get('username')
        if request.method == 'POST':
            Prev = request.POST.get('prev')
            New = request.POST.get('new')

            a = hashlib.md5()
            a.update(Prev.encode())
            Prev_MD5 = a.hexdigest()  # 加密后

            b = hashlib.md5()
            b.update(New.encode())
            New_MD5 = b.hexdigest()

            if Prev_MD5 == User.objects.get(username=UserName).password:
                User.objects.filter(username=UserName).update(password=New_MD5)
                context['alert_type'] = 'success'
                context['update_result'] = '修改成功'
            else:
                context['alert_type'] = 'error'
                context['update_result'] = '原密码不正确'

        return render(request, 'password.html', context)

    else:
        return redirect('/login_prompt')


def Homepage(request):
    context = {}
    if request.session.get('is_login'):
        username = request.session.get('username')
        context['welcome'] = 'Welcome, ' + username
    else:
        context['welcome'] = 'Welcome to our website!'
    return render(request, 'home.html', context)




def UserInfo(request):
    if request.session.get('is_login'):
        context = {}
        UserName = request.session.get('username')
        CurrentUser = User.objects.get(username=UserName)
        if request.session.get('type') == 2:
            context['username'] = UserName
            context['cou_num'] = Course.objects.filter(author=UserName).count()
            context['pro_num'] = Problem.objects.filter(author=UserName).count()

            return render(request, 'teacher_index.html', context)

        else:
            # 获取提交数
            CurrentUser.submit = Answer.objects.filter(author=UserName).count()

            # 获取通过数
            AnswerList = Answer.objects.filter(author=UserName)
            SolveCnt = 0
            for answer in AnswerList:
                try:
                    res = AnswerResult.objects.get(answer_id=answer.answer_id)
                    if res.score == 100:
                        SolveCnt += 1
                except:
                    pass
            CurrentUser.solve = SolveCnt

            context['user'] = CurrentUser

            MyClass = DataOfStudentInClass.objects.filter(studentUsername=UserName)
            for Class in MyClass:
                Class.task_list = ClassHomework.objects.filter(className=Class.className)
                for task in Class.task_list:
                    task.from_class = Class.className
                    course = task.class_course
                    task.course_type = Course.objects.get(title=course).course_type
                    try:
                        problem = Course.objects.get(title=course).problem_href
                    except:
                        task.fin_status = '无题目要求'
                        break
                    if problem:
                        ProblemList = problem.split('|')
                        for problem in ProblemList:  # 判断题目
                            AllAnswer = Answer.objects.filter(author=UserName, problem_id=int(problem))
                            ProblemsFin = True

                            IsFin = False
                            break_status = 0
                            for answer in AllAnswer:  # 判断回答
                                try:
                                    result = AnswerResult.objects.get(answer_id=answer.answer_id)
                                    if result.score == 100:
                                        IsFin = True
                                        break
                                except:
                                    task.fin_status = '判题中'
                                    break_status = 1
                                    break

                            if not IsFin:
                                ProblemsFin = False

                            if break_status:
                                break
                            else:
                                if ProblemsFin:
                                    task.fin_status = '已完成'
                                else:
                                    task.fin_status = '未完成'

            context['class_list'] = MyClass

            return render(request, 'Userinfo_index.html', context)

    else:
        return redirect('/login_prompt')


def LogOut(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出
        return redirect("/")
    request.session.flush()
    return redirect("/")

def LoginPrompt(request):
    return render(request, 'login_prompt.html')

def NewCourse(request):
    if request.session.get('is_login'):
        context = {}
        UserName = request.session.get('username')
        if request.method == 'POST':
            CourseTitle = request.POST.get('course_title', None)
            CourseContent = request.POST.get('course_content', None)
            CourseType = request.POST.get('course_type', None)
            CourseProblem = request.POST.get('course_question', None)

            IsRepeated = Course.objects.filter(title=CourseTitle)
            if IsRepeated:
                return JsonResponse({'res': '课程标题已存在'})

            Course.objects.create(title=CourseTitle, content=CourseContent, course_type=CourseType, problem_href=CourseProblem, author=UserName)
            return JsonResponse({'res': 'OK'})

        PublicProList = Problem.objects.filter(author='admin').order_by('problem_id')
        PrivateProList = Problem.objects.filter(author=UserName).order_by('problem_id')

        context['problem_list'] = PrivateProList | PublicProList

        return render(request, 'new_course.html', context)

    else:
        raise Http404

def NewProblem(request):
    if request.session.get('is_login'):
        UserName = request.session.get('username')
        if request.method == 'POST':
            ProblemTitle = request.POST.get('question_title')
            ProblemDescription = request.POST.get('question_descripition')
            InputDes = request.POST.get('input_descripition')
            OutputDes = request.POST.get('output_descripition')
            InputSample = request.POST.get('input')
            OutputSample = request.POST.get('output')
            Input1 = request.POST.get('input01')
            Output1 = request.POST.get('output01')
            Input2 = request.POST.get('input02')
            Output2 = request.POST.get('output02')
            Input3 = request.POST.get('input03')
            Output3 = request.POST.get('output03')
            Input4 = request.POST.get('input04')
            Output4 = request.POST.get('output04')
            Input5 = request.POST.get('input05')
            Output5 = request.POST.get('output05')
            Level = int(request.POST.get('level'))

            New = Problem.objects.create(problem=ProblemTitle, author=UserName, description=ProblemDescription, input=InputDes,\
                                   output=OutputDes, sample_input=InputSample, sample_output=OutputSample, input1=Input1,\
                                   output1=Output1, input2=Input2, output2=Output2, input3=Input3, output3=Output3,      \
                                   input4=Input4, output4=Output4, input5=Input5, output5=Output5)
            ProblemData.objects.create(problem_id=New.problem_id, level=Level)
            return JsonResponse({'res':1})
        return render(request, 'new_problem.html')
    else:
        raise Http404