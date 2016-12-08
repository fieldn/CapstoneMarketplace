"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from CompaniesApp.models import Company
from AuthenticationApp.models import MyUser

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')
    company = models.ForeignKey(Company, default=None)

    # which languages you need to know
    c_lang = models.BooleanField(default=False)
    java_lang = models.BooleanField(default=False)
    python_lang = models.BooleanField(default=False)
    no_lang = models.BooleanField(default=True)

    # which specialties you have
    front_end_spec = models.BooleanField(default=False)
    back_end_spec = models.BooleanField(default=False)
    full_stack_spec = models.BooleanField(default=False)
    mobile_spec = models.BooleanField(default=False)
    no_spec = models.BooleanField(default=True)

    yrs_of_exp = models.IntegerField(default=0)

    # user can only select None if they select no other fields
    # If they selected None, make all other fields false before saving
    def save(self, *args, **kwargs):
        if self.no_lang:
            self.c_lang = self.java_lang = self.python_lang = False
        if self.no_spec:
            self.front_end_spec = self.back_end_spec = self.full_stack_spec = self.mobile_spec = False
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Bookmark(models.Model):
    user = models.ForeignKey(MyUser, default=None)
    project = models.ForeignKey(Project, default=None)
