# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 03:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0009_auto_20161208_0346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='no_specialty',
            new_name='no_spec',
        ),
    ]
