# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class DataOfStudentInClass(models.Model):
    studentUsername = models.CharField(max_length=50, null=False, blank=False)
    studentNumber = models.IntegerField(null=False, default=1)
    className = models.CharField(max_length=50, null=False)
    studentEmail = models.CharField(max_length=50, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.studentUsername


class DataOfTeacherInClass(models.Model):
    teacherUsername = models.CharField(max_length=50, null=False, blank=False)
    teacherNumber = models.IntegerField(null=False, default=1)
    className = models.CharField(max_length=50, null=False)
    teacherEmail = models.CharField(max_length=50, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.teacherUsername


class InformationOfClass(models.Model):

    className = models.CharField(max_length=50, null=False, primary_key=True)
    classMaxSize = models.IntegerField(null=False, default=200)
    canJoinOrNot = models.BooleanField(null=False, default=True)
    introduction = models.CharField(max_length=10000, null=True, default='')

    objects = models.Manager()

    def __str__(self):
        return self.className

    def if_can_join(self):
        return self.canJoinOrNot


class ClassHomework(models.Model):
    className = models.CharField(max_length=50, null=False, primary_key=True)
    class_homework = models.TextField()
    class_course = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.className
