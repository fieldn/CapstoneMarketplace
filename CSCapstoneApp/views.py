"""CSCapstone Views

Created by Harris Christiansen on 9/18/16.
"""
from django.shortcuts import render
from AuthenticationApp.models import MyUser
from UniversitiesApp.models import Course, University

def getIndex(request):

    # get list of relevant materials by user type
    courses = None
    groups = None
    projects = None
    if request.user != None:
        try:
            if request.user.is_student:
                try:
                    courses = request.user.course_set.all()
                except:
                    pass
                try:
                    groups = request.user.group_set.all()
                except:
                    pass
            if request.user.is_teacher:
                try:
                    courses = request.user.university_set.all().first().course_set.all()
                except:
                    pass
            if request.user.is_engineer:
                try:
                    projects = request.user.company_set.all().first().project_set.all()
                except:
                    pass
        except:
            pass

    return render(request, 'index.html', {
        'userObj' : request.user,
        'courses' : courses,
        'groups' : groups,
        'projects' : projects,
        })

def getTable(request):
    return render(request, 'table.html')

def getForm(request):
    return render(request, 'form.html')
