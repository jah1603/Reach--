# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-03 10:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_reach', '0003_userprofile_instagram_followers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='instagram',
            new_name='instagram_handle',
        ),
    ]
