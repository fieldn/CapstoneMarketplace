"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from .forms import GroupForm
from AuthenticationApp.models import Student

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)

        c_lang = True
        java_lang = True
        python_lang = True
        front_end_spec = True
        back_end_spec = True
        full_stack_spec = True
        mobile_spec = True
        yrs_of_exp = 0

        # remove any qualification that a group member doesn't have
        for member in in_group.members.all():
            student = Student.objects.get(user=member)
            c_lang = c_lang and student.c_lang
            java_lang = java_lang and student.java_lang
            python_lang = python_lang and student.python_lang
            front_end_spec = front_end_spec and student.front_end_spec
            back_end_spec = back_end_spec and student.back_end_spec
            full_stack_spec = full_stack_spec and student.full_stack_spec
            mobile_spec = mobile_spec and student.mobile_spec
            yrs_of_exp += student.yrs_of_exp

        # find all projects using skills all group members have
        matchedProjects = []
        for project in models.Project.objects.all():
            if project.c_lang:
                if not c_lang:
                    continue
            if project.java_lang:
                if not java_lang:
                    continue
            if project.python_lang:
                if not python_lang:
                    continue
            if project.front_end_spec:
                if not front_end_spec:
                    continue
            if project.back_end_spec:
                if not back_end_spec:
                    continue
            if project.full_stack_spec:
                if not full_stack_spec:
                    continue
            if project.mobile_spec:
                if not mobile_spec:
                    continue
            if project.yrs_of_exp > yrs_of_exp:
                continue
            matchedProjects.append(project)

        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'projects' : matchedProjects,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        all_courses = request.user.course_set.all()
        if len(all_courses) == 0:
            return render(request, 'classerror.html')
        form = GroupForm()
        context = {
                "form" : form,
                "course_list" : all_courses
                }
        return render(request, 'groupform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    print "Getting here"
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    all_courses = request.user.course_set.all()
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!', "course_list" : all_courses })
                print form.__dict__
                new_group = models.Group(
                        name=form.cleaned_data['name'], 
                        description=form.cleaned_data['description'], 
                        project=None, 
                        course=models.Course.objects.filter(name__exact=form.cleaned_data['course']).get())
                new_group.save()
                new_group.members.add(request.user)
                for item in form.cleaned_data['members'].split('\n'):
                    try:
                        person = models.MyUser.objects.filter(email__exact=item).get()
                        new_group.members.add(person)
                    except:
                        None
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
            else:
                print "form not valid."
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
