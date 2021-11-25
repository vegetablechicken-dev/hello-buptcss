import time

from django.contrib.sites import requests
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from Problem.models import *
from User.models import *

# Create your views here.
def ProblemList(request):
    context = {}
    ProblemList = Problem.objects.all().order_by('problem_id')
    for i in ProblemList:
        try:
            data = ProblemData.objects.get(problem_id=i.problem_id)

            try:
                i.pass_rate = "{:.1%}".format(data.ac_num / (data.ac_num + data.wa_num))
            except ZeroDivisionError:
                i.pass_rate = '0.0%'

            level = data.level
            if level == 1:
                i.level = 'very ez'
            elif level == 2:
                i.level= 'ez'
            elif level == 3:
                i.level ='middle'
            elif level == 4:
                i.level = 'hard'
            elif level == 5:
                i.level = 'very hard'
            else:
                i.level = 'No data'
        except:
            i.pass_rate = '0.0%'
            i.level = 'No data'

    context['list'] = ProblemList
    return render(request, 'problem.html', context)

def ProblemDetail(request, id):
    context = {}
    try:
        pro = Problem.objects.get(problem_id=id)
        data = ProblemData.objects.get(problem_id=id)
        try:
            pro.pass_rate = "{:.1%}".format(data.ac_num / (data.ac_num + data.wa_num))
        except ZeroDivisionError:
            pro.pass_rate = '0.0%'

        level = ProblemData.objects.get(problem_id=id).level
        if level == 1:
            pro.level = 'very ez'
        elif level == 2:
            pro.level = 'ez'
        elif level == 3:
            pro.level = 'middle'
        elif level == 4:
            pro.level = 'hard'
        elif level == 5:
            pro.level = 'very hard'
        else:
            pro.level = 'No data'

    except:
        raise Http404()

    context['pro'] = pro

    if request.method == 'POST':
        if request.session.get('is_login'):
            UserName = request.session.get('username')
            LangaugeName = request.POST.get('lanuage')
            Code = request.POST.get('code_content')

            if LangaugeName == 'C/C++':
                Language = 1
                LanCode = 'cpp'
            elif LangaugeName == 'Java':
                Language = 2
                LanCode = 'java'
            elif LangaugeName == 'Python':
                Language = 3
                LanCode = 'py'
            else:
                Language = 4
                LanCode = 'error'

            NewAnswer = Answer.objects.create(answer=Code, author=UserName, language=Language, problem_id=id)

            NewResult = AnswerResult.objects.create(answer_id=NewAnswer.answer_id, result1=0, result2=0, result3=0, result4=0, result5=0)

            while True:
                time.sleep(0.5)
                NewResult = AnswerResult.objects.get(answer_id=NewAnswer.answer_id)
                Res1 = NewResult.result1
                Res2 = NewResult.result2
                Res3 = NewResult.result3
                Res4 = NewResult.result4
                Res5 = NewResult.result5
                if Res1 and Res2 and Res3 and Res4 and Res5:
                    break

            if Res1 == 1:
                Score1 = '20'
            else:
                Score1 = '0'

            if Res2 == 1:
                Score2 = '20'
            else:
                Score2 = '0'

            if Res3 == 1:
                Score3 = '20'
            else:
                Score3 = '0'

            if Res4 == 1:
                Score4 = '20'
            else:
                Score4 = '0'

            if Res5 == 1:
                Score5 = '20'
            else:
                Score5 = '0'

            NewResult.score = int(Score1) + int(Score2) + int(Score3) + int(Score4) + int(Score5)
            NewResult.save()

            return JsonResponse({"t1":Score1, "t2":Score2, "t3":Score3, "t4":Score4, "t5":Score5})

        else:
            return redirect('/login_prompt')

    return render(request, 'problem_detail.html', context)