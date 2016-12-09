"""
UniversitiesApp Forms

Created by Jacob Dunbar on 11/5/2016.
"""
from django import forms
from .models import Course

class UniversityForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    photo = forms.ImageField(label='Photo')
    description = forms.CharField(label='Description', max_length=300)
    website = forms.CharField(label='Website', max_length = 300)

class CourseForm(forms.Form):
    tag = forms.CharField(label='Tag', max_length=10)
    name = forms.CharField(label='Name', max_length=50)
    description = forms.CharField(label='Description', max_length=300)

class AddStudentForm(forms.Form):
    students = forms.CharField(label='Students', max_length=1024)

class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'tag', 'description')
