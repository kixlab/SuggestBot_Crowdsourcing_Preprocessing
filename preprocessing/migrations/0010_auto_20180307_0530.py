# Generated by Django 2.0.2 on 2018-03-07 05:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preprocessing', '0009_auto_20180307_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation_inspection_vote',
            name='batch_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='conversation_inspection_vote',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='conversation_inspection_vote',
            name='qualified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='conversation_inspection_vote',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='conversation_inspection_vote',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='preprocessing.Video'),
        ),
        migrations.AddField(
            model_name='language_inspection_vote',
            name='batch_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='language_inspection_vote',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='language_inspection_vote',
            name='qualified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='language_inspection_vote',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='language_inspection_vote',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='preprocessing.Video'),
        ),
        migrations.AddField(
            model_name='scene_inspection_vote',
            name='batch_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='scene_inspection_vote',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='scene_inspection_vote',
            name='qualified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scene_inspection_vote',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='scene_inspection_vote',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='preprocessing.Video'),
        ),
        migrations.AddField(
            model_name='sound_quality_inspection_vote',
            name='batch_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='sound_quality_inspection_vote',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='sound_quality_inspection_vote',
            name='qualified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sound_quality_inspection_vote',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='sound_quality_inspection_vote',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='preprocessing.Video'),
        ),
        migrations.AlterField(
            model_name='video_quality_inspection_vote',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='preprocessing.Video'),
        ),
    ]
