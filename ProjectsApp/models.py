"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from CompaniesApp.models import Company

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')
    company = models.ForeignKey(Company, default=None)

    # TODO Task 3.5: Add fields for project qualifications (minimum required: programming language, years of experience, speciality)

    def __str__(self):
        return self.name
