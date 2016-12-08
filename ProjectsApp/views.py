"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render

from . import models
from .forms import ProjectForm
from AuthenticationApp.models import Engineer
from .models import Project

from datetime import datetime

def getProjects(request):
	projects_list = Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
	return render(request, 'project.html')

def getProjectForm(request):
    if request.user.is_authenticated():
        return render(request, 'projectform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addProject(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                # make sure that the user is an engineer
                if not request.user.is_engineer:
                    return render(request, 'projectform.html', {'error' : 'Only engineers can create classes!'})

                # make sure the engineer belongs to a company
                engineer = Engineer.objects.get(user__exact=request.user)
                if len(request.user.company_set.all()) == 0:
                    return render(request, 'projectform.html', {'error' : 'Engineer must be associated with a company!'})

                # check that the project's name is unique
                name = form.cleaned_data['name']
                try:
                    if Project.objects.get(name__exact=name).exists():
                        return render(request, 'projectform.html', {'error' : 'Error: That project name already exists!'})
                except:
                    pass

                # create a new project
                new_project = Project(name=name,
                    description= form.cleaned_data['description'],
                    created_at = datetime.now(),
                    updated_at = datetime.now(),
                    company = request.user.company_set.all()[0],
                    )
                new_project.save()
                return render(request, 'projects.html')
            else:
                return render(request, 'projectform.html', {'error' : 'Undefined Error!'})
        else:
            form = forms.ProjectForm()
            return render(request, 'projectform.html')
        # render error page if user is not logged in
    return render(request, 'autherror.html')

def getBookmarks(request):
    bookmark_list = models.Bookmark.objects.filter(user__exact = request.user)
    return render(request, 'bookmarks.html', {
        'bookmarks': bookmark_list,
    })

def addBookmark(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_project = models.Project.objects.get(name__exact=in_name)

        new_bookmark = models.Bookmark(user=request.user,
            project=in_project)
        new_bookmark.save()

        context = {'name': in_name,
            'bookmarked' : True,
            }

        return render(request, 'project.html', context)
    return render(request, 'autherror.html')

def removeBookmark(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_project = models.Project.objects.get(name__exact=in_name)

        bookmark = models.Bookmark.objects.filter(projet=in_project)
        bookmark.delete()

        context = {'name': in_name,
            'bookmarked' : False,
            }

        return render(request, 'project.html', context)
    return render(request, 'autherror.html')
