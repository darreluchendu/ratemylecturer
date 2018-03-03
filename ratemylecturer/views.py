from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from ratemylecturer.forms import UserForm, LecturerProfileForm, StudentProfileForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    return render(request, 'ratemylecturer/index.html', {})


def about(request):
    return render(request, 'ratemylecturer/about.html', {})


def register(request):
    registered = False  # flag to tell if registration is successful
    checked_user_type = ""

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        student_profile_form = StudentProfileForm(data=request.POST)
        lecturer_profile_form = LecturerProfileForm(data=request.POST)
        if user_form.is_valid():
            # save user form data
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            if lecturer_profile_form.is_valid():
                lecturer_profile = lecturer_profile_form.save(commit=False)
                lecturer_profile.user = user
                if 'picture' in request.FILES:
                    lecturer_profile.picture = request.FILES['picture']
                lecturer_profile.save()
            if student_profile_form.is_valid:
                student_profile = student_profile_form.save(commit=False)
                student_profile.user = user
                if 'picture' in request.FILES:
                    student_profile.picture = request.FILES['picture']
                student_profile.save()
            registered = True
        else:  # invalid form, for whatever reason
            print(user_form.errors, lecturer_profile_form.errors)
    else:  # not http POST
        user_form = UserForm()
        lecturer_profile_form = LecturerProfileForm()
        student_profile_form = StudentProfileForm()
    return render(request, 'ratemylecturer/../templates/registration/register.html',
                  {'user_form': user_form, 'registered': registered, 'lecturer_profile_form': lecturer_profile_form,
                   'student_profile_form': student_profile_form, 'user_type': checked_user_type})

@login_required()
def profile(request):
    return render(request, 'ratemylecturer/profile.html', {})


def review(request):
    return render(request, 'ratemylecturer/review.html')


@login_required()
def add_review(request):
    return render(request, 'ratemylecturer/add_review.html')

@login_required()
def add_lecturer(request):
    return render(request,'ratemylecturer/add_lecturer.html')

