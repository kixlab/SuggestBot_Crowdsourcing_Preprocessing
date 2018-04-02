# Generated by Django 2.0.2 on 2018-03-29 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_labeling', '0008_auto_20180328_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion_Label_Component_Process',
            fields=[
                ('emotion_label_meta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='emotion_labeling.Emotion_label_Meta')),
                ('smiling', models.BooleanField(default=False)),
                ('mouth_opening', models.BooleanField(default=False)),
                ('mouth_closing', models.BooleanField(default=False)),
                ('mouth_tensing', models.BooleanField(default=False)),
                ('frown', models.BooleanField(default=False)),
                ('tears', models.BooleanField(default=False)),
                ('eyes_opening', models.BooleanField(default=False)),
                ('eyes_closing', models.BooleanField(default=False)),
                ('volume_increasing', models.BooleanField(default=False)),
                ('volume_decreasing', models.BooleanField(default=False)),
                ('v_trembling', models.BooleanField(default=False)),
                ('v_assertive', models.BooleanField(default=False)),
                ('g_abrupt', models.BooleanField(default=False)),
                ('moving_towards', models.BooleanField(default=False)),
                ('withdrawing', models.BooleanField(default=False)),
                ('against', models.BooleanField(default=False)),
                ('silence', models.BooleanField(default=False)),
                ('short_utterance', models.BooleanField(default=False)),
                ('long_utterance', models.BooleanField(default=False)),
                ('s_melody', models.BooleanField(default=False)),
                ('s_disturbance', models.BooleanField(default=False)),
                ('s_tempo', models.BooleanField(default=False)),
                ('shiver', models.BooleanField(default=False)),
                ('pale', models.BooleanField(default=False)),
                ('breathing_slow', models.BooleanField(default=False)),
                ('breathing_faster', models.BooleanField(default=False)),
                ('sweating', models.BooleanField(default=False)),
                ('blushing', models.BooleanField(default=False)),
                ('cognitive', models.CharField(default='', max_length=10000)),
                ('motivational', models.CharField(default='', max_length=10000)),
                ('experiment_video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emotion_labeling.Experiment_Video')),
            ],
            bases=('emotion_labeling.emotion_label_meta',),
        ),
    ]
