# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class Problem(models.Model):  # 问题
    problem_id = models.AutoField(primary_key=True)
    problem = models.CharField(max_length=500, null=False, default='unknown')
    author = models.CharField(max_length=50, default="admin")
    upload_time = models.DateTimeField(auto_now=True)
    # website_name = models.CharField(max_length=50, default="unknown")
    # title = models.CharField(max_length=500, null=False, default='unknown')
    description = models.TextField()
    input = models.TextField(default='')
    output = models.TextField(default='')
    sample_input = models.TextField(default=100)
    sample_output = models.TextField(default=64)
    time_allowed = models.TextField()  # 时间限制
    memory_allowed = models.TextField()  # 内存限制
    hint = models.TextField()
    answer_authority = models.IntegerField(null=False, default=1)  # 1:public 2.private
    template = models.CharField(max_length=10000, default='')

    input1 = models.TextField(default='')
    output1 = models.TextField(default='')
    input2 = models.TextField(default='')
    output2 = models.TextField(default='')
    input3 = models.TextField(default='')
    output3 = models.TextField(default='')
    input4 = models.TextField(default='')
    output4 = models.TextField(default='')
    input5 = models.TextField(default='')
    output5 = models.TextField(default='')

    objects = models.Manager()

    def __str__(self):
        return self.problem


class ProblemData(models.Model):  # 统计数据
    problem_id = models.IntegerField(null=False, default=1, primary_key=True)
    # title = models.CharField(max_length=500, null=False, default='unknown')
    level = models.IntegerField(default=1)  # 1:very ez 2:ez 3:middle 4:hard 5:very hard
    ac_num = models.IntegerField(default=0)  # ac:accepted
    wa_num = models.IntegerField(default=0)  # wa:wrong answer
    tle_num = models.IntegerField(default=0)  # tle:time limited exceed
    mle_num = models.IntegerField(default=0)  # mle:memory limited exceed
    pe_num = models.IntegerField(default=0)  # pe:presentation error
    re_num = models.IntegerField(default=0)  # re:runtime error
    ce_num = models.IntegerField(default=0)  # ce:compile error
    tag = models.TextField(null=True)
    # score = models.IntegerField(default=100)
    # answer_authority = models.IntegerField(null=False, default=1)  # 1:public 2.private
    # website_name = models.CharField(max_length=50, default="unknown")

    objects = models.Manager()

    def __str__(self):
        return self.problem_id


class ProblemTag(models.Model):  # 问题标签
    tag = models.TextField(null=True)
    tag_num = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.tag

    def tag_number(self):
        return self.tag_num


class Answer(models.Model):  # 回答
    answer_id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=10000, null=False)
    author = models.CharField(max_length=50, null=False)
    upload_date = models.DateTimeField(auto_now=True)
    language = models.IntegerField(null=False, default=1)  # 1.C/C++ 2.Java 3.Python
    # upload_time = models.IntegerField(null=False, default=0)
    problem_id = models.IntegerField(null=False, default=1)

    objects = models.Manager()

    def __str__(self):
        return str(self.problem_id) + self.author

class AnswerResult(models.Model):  # 结果
    answer_id = models.IntegerField(null=False, primary_key=True)
    result1 = models.IntegerField(null=False)  # 1.ac 2.wa 3.tle 4.mle 5.pe 6.re 7.ce
    result2 = models.IntegerField(null=False)
    result3 = models.IntegerField(null=False)
    result4 = models.IntegerField(null=False)
    result5 = models.IntegerField(null=False)
    score = models.IntegerField(null=False, default=0)

    objects = models.Manager()

    def __str__(self):
        return self.score