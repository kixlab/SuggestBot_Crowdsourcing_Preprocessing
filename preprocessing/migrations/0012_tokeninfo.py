# Generated by Django 2.0.2 on 2018-03-13 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preprocessing', '0011_auto_20180313_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default='', max_length=200)),
                ('wid', models.CharField(default='', max_length=200)),
                ('aid', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
