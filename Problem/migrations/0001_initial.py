# Generated by Django 3.2.8 on 2021-11-13 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Answer',
        #     fields=[
        #         ('answer_id', models.AutoField(primary_key=True, serialize=False)),
        #         ('answer', models.CharField(max_length=10000)),
        #         ('author', models.CharField(max_length=50)),
        #         ('upload_date', models.DateTimeField(auto_now=True)),
        #         ('problem_id', models.IntegerField(default=1)),
        #     ],
        # ),
        migrations.CreateModel(
            name='AnswerResult',
            fields=[
                ('answer_id', models.IntegerField(primary_key=True, serialize=False)),
                ('result1', models.IntegerField()),
                ('result2', models.IntegerField()),
                ('result3', models.IntegerField()),
                ('result4', models.IntegerField()),
                ('result5', models.IntegerField()),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('problem_id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('problem', models.CharField(default='unknown', max_length=500)),
                ('author', models.CharField(default='admin', max_length=50)),
                ('upload_time', models.DateTimeField(auto_now=True)),
                ('website_name', models.CharField(default='unknown', max_length=50)),
                ('description', models.TextField()),
                ('input', models.TextField()),
                ('output', models.TextField()),
                ('sample_input', models.TextField()),
                ('sample_output', models.TextField()),
                ('time_allowed', models.TextField()),
                ('memory_allowed', models.TextField()),
                ('hint', models.TextField()),
                ('answer_authority', models.IntegerField(default=1)),
                ('template', models.CharField(default='', max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='ProblemData',
            fields=[
                ('problem_id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1)),
                ('ac_num', models.IntegerField(default=0)),
                ('wa_num', models.IntegerField(default=0)),
                ('tle_num', models.IntegerField(default=0)),
                ('mle_num', models.IntegerField(default=0)),
                ('pe_num', models.IntegerField(default=0)),
                ('re_num', models.IntegerField(default=0)),
                ('ce_num', models.IntegerField(default=0)),
                ('tag', models.TextField(null=True)),
                ('score', models.IntegerField(default=100)),
                ('answer_authority', models.IntegerField(default=1)),
                ('website_name', models.CharField(default='unknown', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProblemTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.TextField(null=True)),
                ('tag_num', models.IntegerField(default=0)),
            ],
        ),
    ]
