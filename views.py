# -*- coding: utf-8 -*-
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from .models import InformationOfClass, DataOfStudentInClass, DataOfTeacherInClass
from .permissions import ManagerOnly
from .serializers import ClassInfoSerializers, ClassStudentInfoSerializers, ClassTeacherInfoSerializers


# Create your views here.
class ClassesDataView(viewsets.ModelViewSet):
    queryset = InformationOfClass.objects.all()
    serializer_class = ClassInfoSerializers
    permission_classes = ()
    filter_fields = ('className',)
    search_fields = ('className',)
    permission_classes = (ManagerOnly,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    pagination_class = LimitOffsetPagination
    throttle_scope = 'post'


class ClassesDataAPIView(APIView):
    queryset = InformationOfClass.objects.all()
    serializer_class = ClassInfoSerializers

    @staticmethod
    def post(request, format=None):
        user_type = request.session.get('user_type', 1)
        if user_type != 2 and user_type != 3:
            return Response("You are not admin", status=HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        serializer = ClassInfoSerializers(data=data)  #
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Create successfully", status=HTTP_200_OK)
        return Response("failed creating", status=HTTP_400_BAD_REQUEST)


class DelClassAPIView(APIView):
    queryset = InformationOfClass.objects.all()
    serializer_class = ClassInfoSerializers

    @staticmethod
    def delete_info(request, format=None):
        user_type = request.session.get('user_type', 1)
        if user_type != 2 and user_type != 3:
            return Response("You are not admin", status=HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        name_of_classes = data["className"]
        if InformationOfClass.objects.filter(className__exact=name_of_classes):
            if InformationOfClass.objects.filter(className__exact=name_of_classes).delete():
                return Response("Delete successfully", status=HTTP_200_OK)
        else:
            return Response("Already Deleted", status=HTTP_200_OK)

        return Response("Delete failed", status=HTTP_400_BAD_REQUEST)


class StudentsDataView(viewsets.ModelViewSet):
    queryset = DataOfStudentInClass.objects.all()
    serializer_class = ClassStudentInfoSerializers
    filter_fields = ('studentUsername', 'studentNumber', 'className', 'studentEmail')
    search_fields = ('studentUsername', 'studentNumber', 'studentEmail')
    filter_backends = (SearchFilter, DjangoFilterBackend)
    pagination_class = LimitOffsetPagination
    throttle_scope = 'post'


class StudentDataAPIView(APIView):
    queryset = DataOfStudentInClass.objects.all()
    serializer_class = ClassStudentInfoSerializers

    @staticmethod
    def post(request, format=None):
        data = request.data.copy()
        student_name = data["studentUsername"]
        classes_name = data["className"]
        student_email = data["studentEmail"]
        number = data["studentNumber"]

        serializer = ClassStudentInfoSerializers(data=data)
        if serializer.is_valid(raise_exception=True):
            if DataOfStudentInClass.objects.filter(studentUsername__exact=student_name, className__exact=classes_name,
                                                   studentNumber__exact=number):
                return Response("Repeat join", HTTP_200_OK)
            serializer.save()
            return Response("Join successfully", status=HTTP_200_OK)

        return Response("Join failed", status=HTTP_400_BAD_REQUEST)


class DelStudentAPIView(APIView):
    queryset = DataOfStudentInClass.objects.all()
    serializer_class = ClassStudentInfoSerializers

    @staticmethod
    def delete_student(request, format=None):
        user_type = request.session.get('user_type', 1)
        if user_type != 2 and user_type != 3:
            return Response("You are not admin", status=HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        name_of_student = data["studentUsername"]
        if DataOfStudentInClass.objects.filter(studentUsername__exact=name_of_student):
            if InformationOfClass.objects.filter(studentUsername__exact=name_of_student).delete():
                return Response("Delete successfully", status=HTTP_200_OK)
        else:
            return Response("Already Deleted", status=HTTP_200_OK)

        return Response("Delete failed", status=HTTP_400_BAD_REQUEST)


class StudentQuitClassesAPIView(APIView):
    queryset = DataOfStudentInClass.objects.all()
    serializer_class = ClassStudentInfoSerializers

    @staticmethod
    def student_quit(request, format=None):
        user_type = request.session.get('user_type', 1)
        if user_type != 1:
            return Response("You can't quit the class", status=HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        name_of_student = data["studentUsername"]
        if DataOfStudentInClass.objects.filter(studentUsername__exact=name_of_student):
            if InformationOfClass.objects.filter(studentUsername__exact=name_of_student).delete():
                return Response("Quit successfully", status=HTTP_200_OK)
        else:
            return Response("Already quited", status=HTTP_200_OK)

        return Response("Quit failed", status=HTTP_400_BAD_REQUEST)
