from django.db import models

# Create your models here.
class Course(models.Model):  # 课程
    title = models.CharField(max_length=100, null=False, primary_key=True)
    content = models.TextField()
    problem_href = models.TextField(default="")  # 存problem_id 有多个时，以|分隔
    upload_time = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, null=True, default='admin')
    course_type = models.CharField(max_length=12, null=False, default='Others')  # C CPP Python Java

    objects = models.Manager()

    def __str__(self):
        return self.title


class CourseTypeTag(models.Model):  # 课程标签
    course_type_tag = models.CharField(max_length=24, null=False, default='study', primary_key=True)

    objects = models.Manager()

    def __str__(self):
        return self.course_type_tag