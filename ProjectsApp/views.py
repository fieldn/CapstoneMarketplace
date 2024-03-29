"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render, redirect

from . import models
from .forms import ProjectForm, UpdateProjectForm, FeatureForm
from AuthenticationApp.models import Engineer
from .models import Project, Feature
from django.contrib.auth.decorators import login_required

from datetime import datetime

def getProjects(request):
    projects_list = Project.objects.all()
    return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
    in_name = request.GET.get('name', 'None')

    # check if the user has bookmarked the project
    in_project = models.Project.objects.get(name__exact=in_name)
    try:
        if models.Bookmark.objects.filter(project=in_project,).filter(user=request.user):
            bookmarked = True
        else:
            bookmarked = False
    except:
        bookmarked = False

    features = in_project.feature_set.all()

    context = {
        'project': in_project,
        'bookmarked': bookmarked,
        'features': features,
    }
    if request.user.is_engineer:
        try:
            context['can_delete'] = in_project.company == request.user.company_set.all()[0]
        except:
            context['can_delete'] = False
    else:
        context['can_delete'] = False

    return render(request, 'project.html', context)

def removeProject(request):
    if request.user.is_authenticated():
        proj_name = request.GET.get('name', 'None')
        models.Project.objects.get(name__exact=proj_name).delete()

        return render(request, 'projects.html')
    return render(request, 'autherror.html')

@login_required
def updateProject(request):
    proj = models.Project.objects.filter(name=request.GET.get('name', 'None')).first()
    form = UpdateProjectForm(request.POST or None, instance=proj)

    print form.is_valid()

    if form.is_valid():
        form.save()

    context = {
        'form': form,
        'success': 'Updated successfully',
    }

    return render(request, 'projectupdate.html', context)

def getProjectForm(request):
    if request.user.is_authenticated():
        form = ProjectForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'projectform.html', context)
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
                    description= form.cleaned_data['description'], created_at = datetime.now(), updated_at = datetime.now(),
                    company = request.user.company_set.all()[0],
                    yrs_of_exp = form.cleaned_data['combined_years_of_experience'],
                    c_lang = ('C' in ','.join(form.cleaned_data['languages'])),
                    java_lang = ('Java' in ','.join(form.cleaned_data['languages'])),
                    python_lang = ('Python' in ','.join(form.cleaned_data['languages'])),
                    no_lang = ('None' in ','.join(form.cleaned_data['languages'])),
                    front_end_spec = ('Front_end' in ','.join(form.cleaned_data['specialty'])),
                    back_end_spec = ('Back_end' in ','.join(form.cleaned_data['specialty'])),
                    full_stack_spec = ('Full_stack' in ','.join(form.cleaned_data['specialty'])),
                    mobile_spec = ('Mobile' in ','.join(form.cleaned_data['specialty'])),
                    no_spec = ('None' in ','.join(form.cleaned_data['specialty'])),
                    )
                new_project.save()
                return render(request, 'projects.html')
            else:
                return render(request, 'projectform.html', {'error' : 'Form was invalid. All fields need to be filled out'})
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

        context = {
            'project': in_project, 
            'bookmarked' : True,
            }

        return render(request, 'project.html', context)
    return render(request, 'autherror.html')

def removeBookmark(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_project = models.Project.objects.get(name__exact=in_name)

        bookmark = models.Bookmark.objects.filter(project=in_project)
        bookmark.delete()

        context = {
            'project': in_project, 
            'bookmarked' : False,
            }

        return render(request, 'project.html', context)
    return render(request, 'autherror.html')

def getFeatureForm(request):
    if request.user.is_authenticated():
        in_project_name = request.GET.get('name', 'None')
        in_project = models.Project.objects.filter(name=in_project_name).first()
        form = None
        context = {}
        if request.POST:
            feat = Feature()
            form = FeatureForm(request.POST, instance=feat)
            if form.is_valid():
                form.save()
                setattr(feat, 'project', in_project)
                feat.save()
                context['success'] = 'Feature ' + feat.name + ' Sucessfully Added!'
        form = FeatureForm(None)
        context['form'] = form
        return render(request, 'projectupdate.html', context)
    return render(request, 'autherror.html')
