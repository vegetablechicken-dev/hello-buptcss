from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from Class.models import *
from Course.models import *
from Problem.models import *
from User.models import *

# Create your views here.
def Class(request):
    if request.session.get('is_login'):
        context = {}
        if request.session.get('type') == 2:  # 教师
            UserName = request.session.get('username')
            MyClass = DataOfTeacherInClass.objects.filter(teacherUsername=UserName)
            for Class in MyClass:
                Class.num = DataOfStudentInClass.objects.filter(className=Class.className).count() \
                            + DataOfTeacherInClass.objects.filter(className=Class.className).count()

            context['class_list'] = MyClass

            if request.method == 'POST':
                SearchValue = request.POST.get('search_name', None)
                SearchList = InformationOfClass.objects.filter(className__contains=SearchValue, canJoinOrNot=1)
                for Class in SearchList:
                    Class.num = DataOfStudentInClass.objects.filter(className=Class.className).count() \
                                + DataOfTeacherInClass.objects.filter(className=Class.className).count()
                    if DataOfTeacherInClass.objects.filter(teacherUsername=UserName, className=Class.className):
                        Class.is_joined = True

                context['search_result'] = SearchList

            return render(request, 'teacher_class.html', context)

        else:
            UserName = request.session.get('username')
            MyClass = DataOfStudentInClass.objects.filter(studentUsername=UserName)
            for Class in MyClass:
                Class.num = DataOfStudentInClass.objects.filter(className=Class.className).count()\
                            + DataOfTeacherInClass.objects.filter(className=Class.className).count()

            context['class_list'] = MyClass

            if request.method == 'POST':
                SearchValue = request.POST.get('search_name', None)
                SearchList = InformationOfClass.objects.filter(className__contains=SearchValue, canJoinOrNot=1)
                for Class in SearchList:
                    Class.num = DataOfStudentInClass.objects.filter(className=Class.className).count() \
                                + DataOfTeacherInClass.objects.filter(className=Class.className).count()
                    if DataOfStudentInClass.objects.filter(studentUsername=UserName, className=Class.className):
                        Class.is_joined = True

                context['search_result'] = SearchList

        return render(request, 'class.html', context)

    else:
        return redirect('/login_prompt')



def CreateClass(request):
    if request.session.get('type') == 2:  # 教师
        if request.method == 'POST':
            UserName = request.session.get('username')

            ClassName = request.POST.get('class_name', None)
            ifjoin = request.POST.get('ifjoin', None)
            ClassMaxSize = request.POST.get('max_number', None)
            Introduction = request.POST.get('class_intro', None)

            if ifjoin == '否':
                CanJoinOrNot = 0
            else:
                CanJoinOrNot = 1

            ClassRepeated = InformationOfClass.objects.filter(className=ClassName)
            if ClassRepeated:
                return JsonResponse({'res': '班级名已存在'})

            NewClass = InformationOfClass.objects.create(className=ClassName, classMaxSize=ClassMaxSize,canJoinOrNot=CanJoinOrNot, introduction=Introduction)
            NewClass.save()
            return JsonResponse({'res': '创建成功', 'username': UserName})

        return render(request, 'create_class.html')

    else:
        return redirect('/home')


def ClassJoin(request, class_name):
    if request.session.get('is_login'):
        if InformationOfClass.objects.get(className=class_name).canJoinOrNot:
            if request.session.get('type') == 2:
                UserName = request.session.get('username')
                IsJoined = DataOfTeacherInClass.objects.filter(teacherUsername=UserName, className=class_name)
                if not IsJoined:
                    NewData = DataOfTeacherInClass.objects.create(teacherUsername=UserName, className=class_name)
                    NewData.save()

            else:
                UserName = request.session.get('username')
                IsJoined = DataOfStudentInClass.objects.filter(studentUsername=UserName, className=class_name)
                if not IsJoined:
                    NewData = DataOfStudentInClass.objects.create(studentUsername=UserName, className=class_name)
                    NewData.save()

        ClassNum = DataOfStudentInClass.objects.filter(className=class_name).count() + DataOfTeacherInClass.objects.filter(className=class_name).count()
        Classinfo = InformationOfClass.objects.get(className=class_name)
        if ClassNum >= Classinfo.classMaxSize:
            Classinfo.canJoinOrNot = False
            Classinfo.save()

    return redirect('/class/')

def QuitClass(request, class_name):
    if request.session.get('is_login'):
        if request.session.get('type') == 2:
            UserName = request.session.get('username')
            DataOfTeacherInClass.objects.filter(teacherUsername=UserName, className=class_name).delete()

        else:
            UserName = request.session.get('username')
            DataOfStudentInClass.objects.filter(studentUsername=UserName, className=class_name).delete()

    return redirect('/class/')

def ClassTask(request, class_name):
    context = {}
    if request.session.get('is_login'):
            UserName = request.session.get('username')
            TaskList = ClassHomework.objects.filter(className=class_name)

            for task in TaskList:
                # 获取完成进度 如果course对应题目都完成 则为完成
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

            context['task_list'] = TaskList

    return render(request, 'class_task.html', context)

def ManageClass(request, class_name):
    # 是否在班级内
    if request.session.get('is_login'):
        if request.session.get('type') == 2:  # 教师
            if request.method == 'POST':
                TaskName = request.POST.get('task_name')
                TaskContent = request.POST.get('task_content')
                ClassCourse = request.POST.get('class_course')

                ClassHomework.objects.create(className=class_name, class_homework=TaskName, homework_describe=TaskContent, class_course=ClassCourse)

            context = {}
            UserName = request.session.get('username')
            IsJoined = DataOfTeacherInClass.objects.filter(teacherUsername=UserName, className=class_name)
            if not IsJoined:
                return redirect('/class')
            else:
                # 教师列表 学生列表
                TeacherList = DataOfTeacherInClass.objects.filter(className=class_name)
                for member in TeacherList:
                    try:
                        member.email = User.objects.get(username=member.teacherUsername).email
                    except:
                        member.email = 'No data'
                context['teacher_list'] = TeacherList

                StuList = DataOfStudentInClass.objects.filter(className=class_name)
                for member in StuList:
                    try:
                        member.email = User.objects.get(username=member.studentUsername).email
                        member.exp = str(User.objects.get(username=member.studentUsername).exp)
                    except:
                        member.email = 'No data'
                        member.exp = 'No data'
                context['student_list'] = StuList

                TaskList = ClassHomework.objects.filter(className=class_name)
                for task in TaskList:
                    task.course_type = Course.objects.get(title=task.class_course).course_type
                context['task_list'] = TaskList

                PublicCourseList = Course.objects.filter(author='admin').order_by('upload_time')
                PrivateCourseList = Course.objects.filter(author=UserName).order_by('upload_time')
                context['course_list'] = PrivateCourseList | PublicCourseList

            return render(request, 'manage_class.html', context)

        else:
            raise Http404()

    else:
        return redirect('/login_prompt')





def DeleteTask(request, id):
    if request.session.get('is_login'):
        if request.session.get('type') == 2:
            UserName = request.session.get('username')
            try:
                ClassName = ClassHomework.objects.get(id=id).className
            except:
                raise Http404()

            IsJoined = DataOfTeacherInClass.objects.filter(teacherUsername=UserName, className=ClassName)
            if IsJoined:
                ClassHomework.objects.filter(id=id).delete()

        return redirect('/manage_class/' + ClassName)

    else:
        return redirect('/login_prompt')

def FinStatus(request, task_id):
    if request.session.get('is_login'):
        if request.session.get('type') == 2:
            context = {}
            UserName = request.session.get('username')
            try:
                ClassName = ClassHomework.objects.get(id=task_id).className
            except:
                raise Http404()

            IsJoined = DataOfTeacherInClass.objects.filter(teacherUsername=UserName, className=ClassName)
            if IsJoined:
                StuList = DataOfStudentInClass.objects.filter(className=ClassName)
                task = ClassHomework.objects.get(id=task_id)
                for i in StuList:
                    i.email = User.objects.get(username=i.studentUsername).email

                    # task.course_type = Course.objects.get(title=task.class_course).course_type
                    try:
                        problems = Course.objects.get(title=task.class_course).problem_href
                    except:
                        fin_status = '无题目要求'
                        break
                    if problems:
                        ProblemList = problems.split('|')
                        for problem in ProblemList:  # 判断题目
                            AllAnswer = Answer.objects.filter(author=i.studentUsername, problem_id=int(problem))
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
                                    fin_status = '判题中'
                                    break_status = 1
                                    break

                            if not IsFin:
                                ProblemsFin = False

                            if break_status:
                                break
                            else:
                                if ProblemsFin:
                                    fin_status = '已完成'
                                else:
                                    fin_status = '未完成'

                    i.is_fin = fin_status

                context['list'] = StuList

                StuCnt = 0
                FinCnt = 0
                for i in StuList:
                    StuCnt += 1
                    if i.is_fin == '已完成':
                        FinCnt += 1

                try:
                    FinRate = "{:.1%}".format(FinCnt / StuCnt)
                except ZeroDivisionError:
                    FinRate = '0.0%'

                context['fin_rate'] = FinRate
                context['fin_num'] = FinCnt
                context['stu_num'] = StuCnt

                return render(request, 'fin_status.html', context)

        else:
            raise Http404()

    else:
        return redirect('/login_prompt')
