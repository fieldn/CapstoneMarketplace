# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroupsApp', '0009_comment_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
