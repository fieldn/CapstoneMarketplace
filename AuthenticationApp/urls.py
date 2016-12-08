"""AuthenticationApp URL Configuration

Created by Naman Patwari on 10/4/2016.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.auth_login, name='Login'),
    url(r'^logout$', views.auth_logout, name='Logout'),
    url(r'^register$', views.auth_register, name='Register'),
    url(r'^update$', views.update_profile, name='UpdateProfile'),    
    url(r'^user$', views.view_profile, name='ViewProfile'),    
    url(r'^register_student$', views.register_student, name='AuthStudent'),
    url(r'^register_teacher$', views.register_teacher, name='AuthTeacher'),
    url(r'^register_engineer$', views.register_engineer, name='AuthEngineer'),

]
