"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render

from . import models
from . import forms

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
            }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
            }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'], 
                    photo=request.FILES['photo'],  
                    description=form.cleaned_data['description'],
                    website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                    }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
    # check that the user is authenticated
    if not request.user.is_authenticated():
        return render(request, 'autherror.html')
    
    in_name = request.GET.get('name', 'None')
    in_university = models.University.objects.get(name__exact=in_name)

    # Check that the user is a student or a teacher
    if not request.user.is_student and not request.user.is_teacher:
        # TODO show error message saying you must be a student or teacher
        context = {
            'university' : in_university,
            'userIsMember': False,
            'error' : 'You must be a student or teacher!',
            }
        return render(request, 'university.html', context)

    # Check that the user is not already in another university
    if len(request.user.university_set.all()) > 0:
        # TODO show error message when trying to another university
        context = {
            'university' : in_university,
            'userIsMember': False,
            'error' : 'You can only attend one university at at time!',
            }
        return render(request, 'university.html', context)

    in_university.members.add(request.user)
    in_university.save();
    request.user.university_set.add(in_university)
    request.user.save()
    context = {
        'university' : in_university,
        'userIsMember': True,
        }
    return render(request, 'university.html', context)

def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
            }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')

def getCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_member = in_course.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse' : is_member,
            }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def courseForm(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        context = {
            'university': in_university,
            }
        return render(request, 'courseform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addCourse(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.CourseForm(request.POST)
            if form.is_valid():
                in_university_name = request.GET.get('name', 'None')
                in_university = models.University.objects.get(name__exact=in_university_name)

                # make sure that the user is a teacher
                if not request.user.is_teacher:
                    return render(request, 'courseform.html', {'error' : 'Only teachers can create classes!'})

                # make sure the teach is at the university
                if not request.user in in_university.members.all():
                    return render(request, 'courseform.html', {'error' : 'Only teachers at the university can create classes!'})

                if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
                    return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
                new_course = models.Course(tag=form.cleaned_data['tag'],
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    university=in_university)
                new_course.save()
                in_university.course_set.add(new_course)
                is_member = in_university.members.filter(email__exact=request.user.email)
                context = {
                    'university' : in_university,
                    'userIsMember': is_member,
                    }
                return render(request, 'university.html', context)
            else:
                return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
        else:
            form = forms.CourseForm()
            return render(request, 'courseform.html')
        # render error page if user is not logged in
    return render(request, 'autherror.html')

def removeCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)

        # make sure that the user is a teacher
        if not request.user.is_teacher:
            return render(request, 'courseform.html', {'error' : 'Only teachers can remove classes!'})

        # make sure the teach is at the university
        if not request.user in in_university.members.all():
            return render(request, 'courseform.html', {'error' : 'Only teachers at the university can remove classes!'})

        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.delete()
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember' : is_member,
            }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.add(request.user)
        in_course.save();
        request.user.course_set.add(in_course)
        request.user.save()
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': True,
            }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def unjoinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.remove(request.user)
        in_course.save();
        request.user.course_set.remove(in_course)
        request.user.save()
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': False,
            }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def manageCourse(request):
    if request.user.is_authenticated():

        # make sure that the user is a teacher
        if not request.user.is_teacher:
            return render(request, 'manage.html', {'error' : 'Only teachers can remove classes!'})

        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        
        # handle form submission
        if request.method == 'POST':
            form = forms.AddStudentForm(request.POST)

            # ensure form is valid
            if not form.is_valid():
                return render(request, 'manage.html', {'error' : 'Undefined Error!'})

            # try and add all of the students to the class
            students = form.cleaned_data['students']
            for student in students.split(','):
                user = models.MyUser.objects.get(email__exact=student.strip())

                # check that the user is a student
                if not user.is_student:
                    continue

                in_course.members.add(user)
                in_course.save();
                user.course_set.add(in_course)
                user.save()

        else:
            form = forms.AddStudentForm()

        context = {
            'university' : in_university,
            'course' : in_course,
            }
        return render(request, 'manage.html', context)
    return render(request, 'autherror.html')


def removeStudent(request):
    if request.user.is_authenticated():

        # make sure that the user is a teacher
        if not request.user.is_teacher:
            return render(request, 'manage.html', {'error' : 'Only teachers can remove classes!'})

        in_email = request.GET.get('email', 'None')
        in_user = models.MyUser.objects.get(email__exact=in_email)
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.remove(in_user)
        in_course.save();
        in_user.course_set.remove(in_course)
        in_user.save()
        context = {
            'university' : in_university,
            'course' : in_course,
        }
        return render(request, 'manage.html', context)
    return render(request, 'autherror.html')
