"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from .forms import GroupForm
import json
from django.http import HttpResponse
from AuthenticationApp.models import Student
from .models import Comment, Group

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

        matchedProjects = []
        if in_group.project == None:

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

def getGroupFormUpdate(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        group_name = request.get('group_name', 'None')
        all_courses = request.user.course_set.all()
        form = GroupForm()
        context = {
                "form" : form,
                "course_list" : all_courses
                }
        return render(request, 'groupformupdate.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def updateGroupForm(request):
    if request.user.is_authenticated():
        if request.method == 'GET' :
            form = forms.GroupForm()
            group_id = request.GET.get('id', 'None')
            group = models.Group.objects.get(id__exact=group_id)
            group_name = group.name
            group_desc = group.description
            group_course = group.course
            group_members = group.members.all()
            context = {
                    'form' : form,
                    'group_id' : group_id,
                    'group_name' : group_name,
                    'group_desc' : group_desc,
                    'group_course' : group_course,
                    'group_members' : group_members,
                    }
            return render(request, 'groupformupdate.html', context)
        elif request.method == 'POST' :
            print 'request name is post'
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                group_id = request.GET.get('id', 'None')
                print group_id
                group = models.Group.objects.get(id__exact=group_id)
                setattr(group, 'name', form.cleaned_data['name'])
                setattr(group, 'description', form.cleaned_data['description'])
                for item in form.cleaned_data['members'].split('\n'):
                    try:
                        person = models.MyUser.objects.filter(email__exact=item).get()
                        if person in new_group.members.all():
                            pass
                        else:
                            group.members.add(person)
                    except:
                        pass
                group.save()
                context = {
                        'page_name' : 'Update Group',
                        'name' : form.cleaned_data['name'],
                        'action' : 'updated'
                        }
                '''print context.name'''
                return render(request, 'groupformsuccess.html', context)
            else:
                form = forms.GroupForm()
                print "form not valid."
        if request.method == 'UPDATE' :
            print 'request name is update'
        else:
            form = forms.GroupForm()
            return render(request, 'groupform.html')
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
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    all_courses = request.user.course_set.all()
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!', "course_list" : all_courses })
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
                    'page_name' : 'Create A Group',
                    'name' : form.cleaned_data['name'],
                    'action' : 'created'
                }
                return render(request, 'groupformsuccess.html', context)
            else:
                print "form not valid."
            form = forms.GroupForm()
            return render(request, 'groupform.html', {'page_name':'Create A Group'})
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

def removeGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)

        if not request.user.is_student:
            return render(request, 'group.html', context = {
                'group' : in_group,
                'userIsMember': False,
                })

        if not request.user in in_group.members.all():
            return render(request, 'group.html', context = {
                'group' : in_group,
                'userIsMember': False,
                })

        if len(in_group.members.all()) > 1:
            return render(request, 'group.html', context = {
                'group' : in_group,
                'userIsMember': True,
                })

        in_group.delete()

        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def acceptProject(request):
    if request.user.is_authenticated():
        in_project_name = request.GET.get('project', 'None')
        in_project = models.Project.objects.get(name__exact=in_project_name)
        in_group_name = request.GET.get('group', 'None')
        in_group = models.Group.objects.get(name__exact=in_group_name)
        setattr(in_group, 'project', in_project)
        in_group.save()

        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

# Everything below is for the comment section

def getCommentByID(s):
    return models.Comment.objects.get(id=s)

def isInt(s):
    try:
        int(s)
        return True
    except:
        return False

def serialize(c):
    return {
        'id' : c.id,
        'time' : str(c.time),
        'comment' : c.comment,
        'subcomments' : [serialize(getCommentByID(s)) for s in c.subcomments.split(',') if isInt(s)]
    }

def getComments(request):
    gr = Group.objects.get(name=request.GET.get('name' or None))
    group_comments = gr.comment_set.all().filter(parent=True)
    comments_list = list(group_comments)
    j = json.dumps({'list' : map(serialize, comments_list)})
    context = {'comments' : j, 'group_id' : gr.id}
    return render(request, 'gComments.html', context)

def gAddComment(request):
    if request.method == 'POST':
        try:
            identifier = int(request.POST.get('id', default=-1))
            comment = request.POST['comment']
            comments_list = list(models.Comment.objects.all())
            parent = next((c for c in comments_list if c.id == identifier), None)
            group_id = request.POST['group_id']

            new_comment = models.Comment(user=request.user, comment=comment, parent=parent==None, group_id=group_id)
            new_comment.save()
            if parent != None:
                parent.subcomments += ',' + str(new_comment.id)
                parent.save();
            response_data = { 'error' : 'success' }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        except KeyError:
            pass
