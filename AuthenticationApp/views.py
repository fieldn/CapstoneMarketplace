"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterTeacherForm, RegisterStudentForm, RegisterEngineerForm, UpdateForm, UpdateStudentForm, UpdateTeacherForm, UpdateEngineerForm
from .models import MyUser, Student, Teacher, Engineer

# Auth Views

def auth_login(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if next_url is None:
        next_url = "/"
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            messages.success(request, 'Success! Welcome, ' + (user.first_name or ""))
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            messages.warning(request, 'Invalid username or password.')

    context = {
            "form": form,
            "page_name" : "Login",
            "button_value" : "Login",
            "links" : ["register"],
            }
    return render(request, 'auth_form.html', context)

def auth_logout(request):
    logout(request)
    messages.success(request, 'Success, you are now logged out')
    return render(request, 'index.html')

#simply asks if the user is a student, teacher, or engineer
def auth_register(request): 
    if request.user.is_authenticated(): 
        return HttpResponseRedirect("/")
    return render(request, 'register.html')

#Register teacher
def register_teacher(request):
    form = RegisterTeacherForm(request.POST or None)
    if form.is_valid():
        new_user = MyUser.objects.create_user(
            email=form.cleaned_data['email'], 
            password=form.cleaned_data["password2"], 
            first_name=form.cleaned_data['firstname'], 
            last_name=form.cleaned_data['lastname'],
            is_teacher=True,
        )
        new_user.save()
        new_teacher = Teacher(user = new_user,
            title = form.cleaned_data['teacherTitle'],
            phone = form.cleaned_data['teacherPhone'],
            office = form.cleaned_data['teacherOffice'],
            photo = request.FILES['teacherPhoto'],  
            about = form.cleaned_data['teacherAbout'],
            )
        new_teacher.save()

        login(request, new_user)
        messages.success(request, 'Success! Your account was created.')
        return render(request, 'index.html')

    context = {
        "form": form,
        "page_name" : "Register Teacher",
        "button_value" : "Register",
        "links" : ["login"],
        }
    return render(request, 'auth_form.html', context)

#Register student
def register_student(request):
    form = RegisterStudentForm(request.POST or None)
    if form.is_valid():
        new_user = MyUser.objects.create_user(
            email=form.cleaned_data['email'], 
            password=form.cleaned_data["password2"], 
            first_name=form.cleaned_data['firstname'], 
            last_name=form.cleaned_data['lastname'],
            is_student=True,
        )
        new_user.save()
        new_student = Student(user = new_user,
            phone = form.cleaned_data['studentPhone'],
            about = form.cleaned_data['studentAbout'],
            photo = request.FILES['studentPhoto'],  
            c_lang = form.cleaned_data['c_lang'],
            java_lang = form.cleaned_data['java_lang'],
            python_lang = form.cleaned_data['python_lang'],
            no_lang = form.cleaned_data['no_lang'],
            mobile_spec = form.cleaned_data['mobile_spec'],
            front_end_spec = form.cleaned_data['front_end_spec'],
            back_end_spec = form.cleaned_data['back_end_spec'],
            full_stack_spec = form.cleaned_data['full_stack_spec'],
            no_spec = form.cleaned_data['no_spec'],
            yrs_of_exp = form.cleaned_data['yrs_of_exp'],
            )
        new_student.save()
        
        login(request, new_user)
        messages.success(request, 'Success! Your account was created.')
        return render(request, 'index.html')

    context = {
        "form": form,
        "page_name" : "Register Student",
        "button_value" : "Register",
        "links" : ["login"],
        }
    return render(request, 'auth_form.html', context)

#Register engineer
def register_engineer(request):
    form = RegisterEngineerForm(request.POST or None)
    if form.is_valid():
        new_user = MyUser.objects.create_user(
            email=form.cleaned_data['email'], 
            password=form.cleaned_data["password2"], 
            first_name=form.cleaned_data['firstname'], 
            last_name=form.cleaned_data['lastname'],
            is_engineer=True,
        )
        new_user.save()
        new_engineer = Engineer(user = new_user,
            title = form.cleaned_data['engineerTitle'],
            phone = form.cleaned_data['engineerPhone'],
            almaMater = form.cleaned_data['engineerAlmaMater'],
            photo = request.FILES['engineerPhoto'],  
            about = form.cleaned_data['engineerAbout'],
            )
        new_engineer.save()

        login(request, new_user)
        messages.success(request, 'Success! Your account was created.')
        return render(request, 'index.html')

    context = {
        "form": form,
        "page_name" : "Register Engineer",
        "button_value" : "Register",
        "links" : ["login"],
        }
    return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
    # for the general data that all users share
    form = UpdateForm(request.POST or None, instance=request.user)

    # for the specific data that only belongs to a student/teacher/engineer
    form2 = None
    if request.user.is_student == True:
        form2 = UpdateStudentForm(request.POST or None, instance=Student.objects.get(user_id=request.user.id))
    elif request.user.is_teacher == True:
        form2 = UpdateTeacherForm(request.POST or None, instance=Teacher.objects.get(user_id=request.user.id))
    elif request.user.is_engineer == True:
        form2 = UpdateEngineerForm(request.POST or None, instance=Engineer.objects.get(user_id=request.user.id))

    if form.is_valid():
        form.save()
    if form2.is_valid():
        form2.save()
    if form.is_valid() and form2.is_valid():
        messages.success(request, 'Success: your information was saved.')

    context = {
        "form": form,
        "form2": form2,
        "page_name" : "Update",
        "button_value" : "Update",
        "links" : ["logout"],
        }
    return render(request, 'auth_form.html', context)

def view_profile(request):
    # find the user
    in_name = request.GET.get('user')
    in_user = MyUser.objects.get(email__exact=in_name)
    
    current_user = request.user

    # find the information specific to the user's role
    student = None
    engineer = None
    teacher = None
    if in_user.is_student:
        student = Student.objects.get(user=in_user)
    if in_user.is_teacher:
        teacher = Teacher.objects.get(user=in_user)
    if in_user.is_engineer:
        engineer = Engineer.objects.get(user=in_user)

    context = {'current_user' : current_user,
            'user': in_user, 
            'student' : student,
            'teacher' : teacher,
            'engineer' : engineer,
        }
    return render(request, 'profile.html', context)
