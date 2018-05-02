# Generated by Django 2.0.2 on 2018-05-02 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_labeling', '0017_experiment_video_video_hit_dict'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion_Label_Baseline',
            fields=[
                ('emotion_label_meta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='emotion_labeling.Emotion_label_Meta')),
                ('experiment_video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emotion_labeling.Experiment_Video')),
            ],
            bases=('emotion_labeling.emotion_label_meta',),
        ),
    ]
