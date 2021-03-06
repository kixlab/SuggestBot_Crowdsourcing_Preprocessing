# Generated by Django 2.0.2 on 2018-03-21 06:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_labeling', '0003_auto_20180320_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion_check_experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualified', models.BooleanField(default=False)),
                ('end_time', models.DateTimeField(default=datetime.datetime.now)),
                ('start_time', models.DateTimeField(default=datetime.datetime.now)),
                ('wid', models.CharField(default='', max_length=200)),
                ('aid', models.CharField(default='', max_length=200)),
                ('emotion_label', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emotion_labeling.Emotion_label_experiment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
