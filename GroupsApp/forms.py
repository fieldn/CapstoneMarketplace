"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms
from . import models
from UniversitiesApp.models import Course

course_list = Course.objects.all()

class GroupForm(forms.Form):
    name = forms.CharField(label='name', required=False, max_length=30)
    description = forms.CharField(label='description', required=False, max_length=300)
    course = forms.CharField(label='course', required=False)
    members = forms.CharField(label='members', required=False)


class CommentForm(forms.Form):
    comment = forms.CharField(label='Text', max_length=500)
