# Generated by Django 2.0.2 on 2018-06-18 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_labeling', '0032_auto_20180618_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='frame_task_checkbox',
            name='survey_result',
            field=models.CharField(default='', max_length=20000),
        ),
        migrations.AddField(
            model_name='frame_task_checkbox_confidence',
            name='survey_result',
            field=models.CharField(default='', max_length=20000),
        ),
        migrations.AddField(
            model_name='frame_task_radio',
            name='survey_result',
            field=models.CharField(default='', max_length=20000),
        ),
    ]