# Generated by Django 3.2.8 on 2021-11-15 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0004_auto_20211115_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='classhomework',
            name='homework_describe',
            field=models.TextField(default=''),
        ),
    ]
