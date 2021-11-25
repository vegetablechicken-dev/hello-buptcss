from django.http import Http404
from django.shortcuts import render, redirect

from Course.models import Course
from Problem.models import *


def CourseType(request):
    return render(request, 'course.html')


def CourseDetail(request, type, title):
    context = {}
    context['type'] = type
    context['list'] = Course.objects.filter(author='admin', course_type=type).order_by('upload_time')
    if title == 'default':
        try:
            title = context['list'][0]
        except:
            raise Http404("Course not found")

    try:
        CurrentCourse = Course.objects.get(title=title)
        context['course'] = CurrentCourse
    except:
        raise Http404("Course not found")

    if CurrentCourse.problem_href:
        context['no_problem'] = False
        if request.session.get('is_login'):
            UserName = request.session.get('username')
            ProblemIdList = CurrentCourse.problem_href.split('|')
            FinList = []
            UnfinList = []
            for pro in ProblemIdList:
                try:
                    CurrentProblem = Problem.objects.get(problem_id=pro)
                    AllAnswer = Answer.objects.filter(author=UserName, problem_id=pro)

                    IsFin = False
                    for answer in AllAnswer:  # 判断回答
                        try:
                            result = AnswerResult.objects.get(answer_id=answer.answer_id)
                            if result.score == 100:
                                IsFin = True
                                break
                        except:
                            pass

                    if IsFin:
                        FinList.append(CurrentProblem)
                    else:
                        UnfinList.append(CurrentProblem)

                except:
                    pass

            context['fin_list'] = FinList
            context['unfin_list'] = UnfinList

        else:
            ProblemIdList = CurrentCourse.problem_href.split('|')
            ProblemList = []
            for pro in ProblemIdList:
                try:
                    CurrentProblem = Problem.objects.get(problem_id=pro)
                    ProblemList.append(CurrentProblem)
                except:
                    pass
            context['unfin_list'] = ProblemList

    else:
        context['no_problem'] = True


    return render(request, 'course_detail.html', context)
