# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CommentsApp', '0003_remove_comment_comment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='subcomments',
            field=models.TextField(default=''),
        ),
    ]
