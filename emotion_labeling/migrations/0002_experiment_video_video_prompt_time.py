# Generated by Django 2.0.2 on 2018-03-20 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_labeling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment_video',
            name='video_prompt_time',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
