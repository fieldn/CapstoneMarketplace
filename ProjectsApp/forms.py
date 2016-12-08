"""AuthenticationApp Forms

Created by Naman Patwari on 10/4/2016.
"""
from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=10000) 

    choices = (('C', 'C'), ('Java', 'Java'), ('Python', 'Python'), ('None', 'None'))
    languages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices)

    combined_years_of_experience = forms.IntegerField(min_value=0)

    choices2 = (('Front_end', 'Front end'), ('Back_end', 'Back end'), ('Full_stack', 'Full stack'), ('Mobile', 'Mobile'), ('None', 'None'))
    specialty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices2)
