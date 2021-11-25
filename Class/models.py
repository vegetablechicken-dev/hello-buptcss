# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class DataOfStudentInClass(models.Model):  # 学生信息（班级中）
    studentUsername = models.CharField(max_length=50, null=False, blank=False)
    # studentNumber = models.IntegerField(null=False, default=1)
    className = models.CharField(max_length=50, null=False)
    # studentEmail = models.CharField(max_length=50, null=False, default='')

    objects = models.Manager()

    def __str__(self):
        return self.studentUsername


class DataOfTeacherInClass(models.Model):  # 教师信息（班级中）
    teacherUsername = models.CharField(max_length=50, null=False, blank=False)
    # teacherNumber = models.IntegerField(null=False, default=1)
    className = models.CharField(max_length=50, null=False)
    # teacherEmail = models.CharField(max_length=50, null=False, default='')

    objects = models.Manager()

    def __str__(self):
        return self.teacherUsername


class InformationOfClass(models.Model):  # 班级信息

    className = models.CharField(max_length=50, null=False, primary_key=True)
    classMaxSize = models.IntegerField(null=False, default=200)
    canJoinOrNot = models.BooleanField(null=False, default=True)
    introduction = models.CharField(max_length=10000, null=True, default='')

    objects = models.Manager()

    def __str__(self):
        return self.className

    def if_can_join(self):
        return self.canJoinOrNot


class ClassHomework(models.Model):  # 班级任务
    className = models.CharField(max_length=50, null=False)
    class_homework = models.TextField()
    homework_describe = models.TextField(default='')
    class_course = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.className
