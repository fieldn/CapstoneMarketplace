"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from __future__ import unicode_literals
from django.db import models
from AuthenticationApp.models import MyUser
from ProjectsApp.models import Project, Feature
from UniversitiesApp.models import Course

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    project = models.ForeignKey(Project, null=True, default=None)
    course = models.ForeignKey(Course, default=None)
    members = models.ManyToManyField(MyUser, default=None)
    features = models.ManyToManyField(Feature, default=None)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    time = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=100, default="")
    user_type = models.CharField(max_length=100, default="Visitor")
    comment = models.CharField(max_length=500, default="")
    subcomments = models.TextField(default='')
    parent = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
