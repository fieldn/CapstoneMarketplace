# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0006_auto_20161208_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='interests',
            field=models.CharField(default=b'None', max_length=200),
        ),
    ]
