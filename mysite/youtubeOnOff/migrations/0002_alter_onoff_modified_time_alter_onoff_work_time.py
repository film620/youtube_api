# Generated by Django 4.1.1 on 2022-12-13 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtubeOnOff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onoff',
            name='modified_time',
            field=models.DateTimeField(verbose_name='Modified TIme'),
        ),
        migrations.AlterField(
            model_name='onoff',
            name='work_time',
            field=models.DateTimeField(verbose_name='Work Time'),
        ),
    ]