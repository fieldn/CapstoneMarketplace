"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms
from . import models
from UniversitiesApp.models import Course

course_list = Course.objects.all()

class GroupForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput, required=True, max_length=30)
    description = forms.CharField(label='Description',widget=forms.Textarea, required=True, max_length=300)
