"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser
from ProjectsApp.models import Project
from UniversitiesApp.models import Course

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    project = models.ForeignKey(Project, default=None)
    course = models.ForeignKey(Course, default=None)
    members = models.ManyToManyField(MyUser)
    
    def __str__(self):
        return self.name
