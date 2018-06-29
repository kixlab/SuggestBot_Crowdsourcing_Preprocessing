# Generated by Django 2.0.2 on 2018-06-29 06:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_labeling', '0034_frame_task_radio_confidence'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frame_Gold_Data_Checkbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_time', models.DateTimeField(default=datetime.datetime.now)),
                ('start_time', models.DateTimeField(default=datetime.datetime.now)),
                ('gen_time', models.DateTimeField(default=datetime.datetime.now)),
                ('frame_confidences', models.CharField(default='', max_length=20000)),
                ('no_field_reasoning', models.CharField(default='', max_length=20000)),
                ('wid', models.CharField(default='', max_length=2000)),
                ('aid', models.CharField(default='', max_length=2000)),
                ('task_sub_id', models.IntegerField(default='-1')),
                ('token', models.CharField(default='', max_length=200)),
                ('frame_sentence', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='emotion_labeling.Frame_Sentence')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Frame_Gold_Data_Checkbox_Confidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_time', models.DateTimeField(default=datetime.datetime.now)),
                ('start_time', models.DateTimeField(default=datetime.datetime.now)),
                ('gen_time', models.DateTimeField(default=datetime.datetime.now)),
                ('frame_confidences', models.CharField(default='', max_length=20000)),
                ('no_field_reasoning', models.CharField(default='', max_length=20000)),
                ('wid', models.CharField(default='', max_length=2000)),
                ('aid', models.CharField(default='', max_length=2000)),
                ('task_sub_id', models.IntegerField(default='-1')),
                ('token', models.CharField(default='', max_length=200)),
                ('frame_sentence', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='emotion_labeling.Frame_Sentence')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Frame_Sentence_GT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence_id', models.IntegerField(default=-1)),
            ],
        ),
    ]
