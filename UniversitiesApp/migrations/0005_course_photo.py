# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniversitiesApp', '0004_auto_20161108_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='photo',
            field=models.ImageField(default=0, upload_to=b'static/courseimages'),
        ),
    ]
