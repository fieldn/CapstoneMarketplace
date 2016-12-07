"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render

from . import models

def getProjects(request):
	projects_list = models.Project.objects.all()
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
            form = forms.ProjectForm(request.POST)
            if form.is_valid():

                # make sure that the user is a teacher
                if not request.user.is_engineer:
                    return render(request, 'projectform.html', {'error' : 'Only engineers can create classes!'})

                # make sure the engineer belongs to a company
                engineer = models.Engineer.objects.get(user__exact=request.user)
                if len(request.user.company_set.all()) == 0:
                    return render(request, 'projectform.html', {'error' : 'Engineer must be associated with a company!'})

                # check that the project's name is unique
                name = form.cleaned_data['name']
                if models.Project.objects.get(name__exact=name).exists():
                    return render(request, 'projectform.html', {'error' : 'Error: That project name already exists!'})

                # create a new project
                new_project = models.Project(name=name,
                    description=cleaned_data['description'],
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

