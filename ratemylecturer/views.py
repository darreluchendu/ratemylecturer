from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import LecturerProfile,StudentProfile
from ratemylecturer.forms import UserForm,LecturerProfileForm, StudentProfileForm, ReviewForm
from django.contrib.auth.models import User
import json


def index(request):
    user_id=request.user.id
    try:
        user = StudentProfile.objects.get(user_id=user_id)
        isStudent=True
    except StudentProfile.DoesNotExist:
        isStudent= False
    return render(request,'ratemylecturer/index.html',{"user_id":user_id, "isStudent": isStudent})

# view for registration
def register_student(request):
    registered = False; # flag to tell if registration is successful
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        student_profile_form = StudentProfileForm(data=request.POST)
        if user_form.is_valid() and student_profile_form.is_valid():
            # save user form data
            user = user_form.save()
            user.set_password(user.password)
            user.save();
            # save student profile data
            # commit = false until ready to commit to avoid interity problem
            student_profile = student_profile_form.save(commit=False)
            student_profile.user = user
            if 'picture' in request.FILES:
                student_profile.picture = request.FILES['picture']
            student_profile.save()
            registered = True
        else:  # invalid form, for whatever reason
            print(user_form.errors, student_profile_form.errors)
    else:  #not http POST
        user_form = UserForm()
        student_profile_form = StudentProfileForm()
    return render( request,'ratemylecturer/register_student.html',{'user_form':user_form,
                    'student_profile_form':student_profile_form, 'registered': registered})

def register_lecturer(request):
    registered = False; # flag to tell if registration is successful
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        lecturer_profile_form = LecturerProfileForm(data=request.POST)
        if user_form.is_valid() and lecturer_profile_form.is_valid():
            # save user form data
            user = user_form.save()
            user.set_password(user.password)
            user.save();
            lecturer_profile = lecturer_profile_form.save(commit=False)
            lecturer_profile.user = user
            if 'picture' in request.FILES:
                lecturer_profile.picture = request.FILES['picture']
            lecturer_profile.save()
            registered = True

        else:#invalid form, for whatever reason
            print(user_form.errors, lecturer_profile_form.errors)

    else:# not http POST
        user_form = UserForm()
        lecturer_profile_form  = LecturerProfileForm()
    return render( request,'ratemylecturer/register_lecturer.html',{'user_form':user_form,'registered': registered, 'lecturer_profile_form':
                            lecturer_profile_form})

# login page view
def user_login(request):
    login_error=False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # password authentication using django
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active: # account may have been disabled
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else: # account inactive
                return HttpResponse("Your account is disabled.")
        else: # invalid login details
            login_error = True
            return render(request, 'rango/login.html', {'error': login_error})
    else: # not a HTTP POST, hence blank dictionary object
        context_dict = {}
        return render(request,'ratemylecturer/login.html',context_dict)
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def is_student(user):
    try:
        user_profile = StudentProfile.objects.get(user=user)
        return True
    except StudentProfile.DoesNotExist:
        return False


@user_passes_test(is_student, login_url='/ratemylecturer/login/')
@login_required
def create_lecturer(request,user_id ):

    created=False
        # flag to tell if registration is successful
    if request.method == 'POST':

        lecturer_profile_form = LecturerProfileForm(data=request.POST)
        if lecturer_profile_form.is_valid():
            # save user form data
            lecturer_profile = lecturer_profile_form.save(commit=False)
            rand_password = User.objects.make_random_password()
            proxy_user_count=LecturerProfile.objects.all().count()+1
            user = User.objects.create(username="proxy_user"+proxy_user_count ,
                                       email="proxy_user"+proxy_user_count+'@gmail.com')
            user.set_password(rand_password)
            user.save()

            lecturer_profile.user = user

            if 'picture' in request.FILES:
                lecturer_profile.picture = request.FILES['picture']
            lecturer_profile.save()
            created = True

        else:  # invalid form, for whatever reason
            print(lecturer_profile_form.errors)

    else:# not http POST
        lecturer_profile_form  = LecturerProfileForm()
        name_list_raw = LecturerProfile.objects.all().values_list('name', 'university')
        name_list = []
        for name, uni in name_list_raw:
            data = {"name": name, "uni": uni,"value": name + " - " + uni}
            name_list.append(data)
        js_data = json.dumps(name_list)

    return render( request,'ratemylecturer/create_lecturer.html',{'created': created, 'lecturer_profile_form':
        lecturer_profile_form, 'user_id':user_id,"name_list":js_data})








