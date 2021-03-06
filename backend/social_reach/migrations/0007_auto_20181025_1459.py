# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-25 14:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_reach', '0006_auto_20181025_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gym',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='kids',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='see_only_gym',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='see_only_non_parents',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='see_only_non_smokers',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='see_only_vegans',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='smoker',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='vegan',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2018, 10, 25, 14, 59, 23, 667234)),
        ),
    ]
