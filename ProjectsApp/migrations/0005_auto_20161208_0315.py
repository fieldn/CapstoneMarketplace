# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0004_project_languages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='languages',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
