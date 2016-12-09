"""GroupsApp URL

Created by Naman Patwari on 10/10/2016.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^group/all$', views.getGroups, name='Groups'),
    url(r'^group/form$', views.getGroupForm, name='GroupForm'),
    url(r'^group/formupdate$', views.getGroupFormUpdate, name='GroupFormUpdate'),
    url(r'^group/formsuccess$', views.getGroupFormSuccess, name='GroupFormSuccess'),
    url(r'^group/update$', views.updateGroupForm, name='UpdateGroupForm'),
    url(r'^group/join$', views.joinGroup, name='GJoin'),
    url(r'^group/unjoin$', views.unjoinGroup, name='GUnjoin'),
    url(r'^group$', views.getGroup, name='getGroup'),
    url(r'^group/getComments$', views.getComments, name='getComments'),
    url(r'^group/gAddComment$', views.gAddComment, name='gAddComment'),
    url(r'^group/gDeleteComment$', views.gDeleteComment, name='gDeleteComment'),
    url(r'^group/accept$', views.acceptProject, name='AcceptProject'),
    url(r'^group/remove$', views.removeGroup, name='RemoveGroup'),
    url(r'^group/feature/done$', views.featureDone, name='FeatureDone'),
]
