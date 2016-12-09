"""ProjectsApp URL Configuration

Created by Harris Christiansen on 10/02/16.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^project/form$', views.getProjectForm, name='ProjectForm'),
    url(r'^project/add$', views.addProject, name='ProjectAdd'),
    url(r'^project/update$', views.updateProject, name='ProjectUpdate'),
    url(r'^project/remove$', views.removeProject, name='ProjectRemove'),
    url(r'^project/feature/form$', views.getFeatureForm, name='FeatureForm'),
    url(r'^bookmark/all$', views.getBookmarks, name='Bookmarks'),
    url(r'^bookmark/add$', views.addBookmark, name='BookmarkAdd'),
    url(r'^bookmark/remove$', views.removeBookmark, name='BookmarkRemove'),
]
