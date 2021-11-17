"""OLProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from User import views as User_views
from Course import views as Course_views
from Class import views as Class_views
from Problem import views as Problem_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('update/', User_views.UpdateInfo, name='update'),
    re_path(r'^$', User_views.Homepage, name='home'),
    path('userinfo/', User_views.UserInfo, name='userinfo'),
    path('logout/', User_views.LogOut, name='logout'),
    path('course/', Course_views.CourseType, name='course'),
    path('class/', Class_views.Class, name='class'),
    path('problem/', Problem_views.ProblemList, name='problem'),
    path('course_detail/<str:type>/<str:title>',Course_views.CourseDetail, name='course_detail'),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('problem_detail/<int:id>', Problem_views.ProblemDetail, name='problem_detail'),
    path('create_class/', Class_views.CreateClass, name='create_class'),
    path('class_join/<str:class_name>', Class_views.ClassJoin, name='class_join'),
    path('quit_class/<str:class_name>', Class_views.QuitClass, name='quit_class'),
    path('class/<str:class_name>', Class_views.ClassTask, name='class_task'),
    # path('teacher_class/', Class_views.TeacherClass, name='teacher_class'),
    path('manage_class/<str:class_name>', Class_views.ManageClass, name='manage_class'),
    path('del_task/<int:id>', Class_views.DeleteTask, name='del_task'),
    path('fin_status/<int:task_id>', Class_views.FinStatus, name='fin_status'),
    path('password/', User_views.Password, name='password'),
    path('login_prompt/', User_views.LoginPrompt, name='login_prompt'),
    path('new_course/', User_views.NewCourse, name='new_course'),
    path('new_problem/', User_views.NewProblem, name='new_problem'),

]
