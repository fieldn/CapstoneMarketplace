# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0014_merge_20161208_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=1)),
                ('name', models.CharField(default=None, max_length=64)),
                ('description', models.CharField(default=None, max_length=10000)),
                ('project', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ProjectsApp.Project')),
            ],
        ),
    ]
