# Generated by Django 3.2.8 on 2021-11-11 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataofstudentinclass',
            name='studentEmail',
        ),
    ]