# Generated by Django 3.2.8 on 2021-11-15 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0002_remove_dataofstudentinclass_studentemail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataofstudentinclass',
            name='studentNumber',
        ),
        migrations.RemoveField(
            model_name='dataofteacherinclass',
            name='teacherEmail',
        ),
        migrations.RemoveField(
            model_name='dataofteacherinclass',
            name='teacherNumber',
        ),
    ]