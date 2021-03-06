# Generated by Django 2.0.2 on 2018-03-06 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(default='', max_length=200)),
                ('video_url', models.CharField(default='', max_length=200)),
                ('fully_inspected', models.BooleanField(default=False)),
                ('passed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Video_inspection_vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_quality', models.BooleanField(default=False)),
                ('sound_quality', models.BooleanField(default=False)),
                ('language', models.BooleanField(default=False)),
                ('conversation', models.BooleanField(default=False)),
                ('scene', models.BooleanField(default=False)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preprocessing.Video')),
            ],
        ),
    ]
