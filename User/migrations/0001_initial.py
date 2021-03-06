# Generated by Django 3.2.8 on 2021-11-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=40, null=True)),
                ('exp', models.IntegerField(default=0)),
                ('introduction', models.CharField(default='', max_length=10000, null=True)),
                ('type', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginData',
            fields=[
                ('username', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('logintime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
