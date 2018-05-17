# Generated by Django 2.0.2 on 2018-05-16 05:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_labeling', '0020_auto_20180502_0439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion_Distribution_Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Emotion_Distribution_Meta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=0)),
                ('distribution', models.CharField(default='', max_length=20000)),
                ('wid', models.CharField(default='', max_length=200)),
                ('aid', models.CharField(default='', max_length=200)),
                ('task_start_time', models.DateTimeField(default=datetime.datetime.now)),
                ('task_end_time', models.DateTimeField(default=datetime.datetime.now)),
                ('experiment_video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emotion_labeling.Experiment_Video')),
            ],
        ),
    ]