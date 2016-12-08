"""AuthenticationApp Forms

Created by Naman Patwari on 10/4/2016.
"""
from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=10000) 
