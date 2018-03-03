from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import LecturerProfile,StudentProfile,Review,UserMethods
from ratemylecturer.forms import UserForm,LecturerProfileForm, StudentProfileForm, ReviewForm
from django.contrib.auth.models import User
import json
import requests
def index(request):
    return render(request,'ratemylecturer/index.html',{})

@csrf_exempt
def lecturer_ajax_data(request):

    post_data = json.loads(request.body.decode('utf-8'))
    proxy_user = post_data["user"]
    request.session["user_id"]=proxy_user
    request.session["is_ajax"] =True
    return HttpResponse("")

def register(request):
    registered = False  # flag to tell if registration is successful
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        student_profile_form = StudentProfileForm(data=request.POST)
        lecturer_profile_form = LecturerProfileForm(data=request.POST)
        if user_form.is_valid():
            # save user form data
            user = user_form.save(commit=False)
            user.set_password(user.password)

            if student_profile_form.is_valid():
                student_profile = student_profile_form.save(commit=False)
                user.save()
                student_profile.user = user
                if 'picture' in request.FILES:
                    student_profile.picture = request.FILES['picture']
                student_profile.save()

            if lecturer_profile_form.is_valid():
                lecturer_profile = lecturer_profile_form.save(commit=False)

                if request.session.get("is_ajax"):
                  # save user form data
                  # adding real user to an already created lecturer
                    proxy_user_id = request.session.get("user_id")
                    proxy_user=User.objects.get(pk=proxy_user_id)
                    proxy_user.username = user.username
                    proxy_user.email = user.email
                    proxy_user.set_password(user.password)
                    proxy_user.save()

                    LecturerProfile.objects.filter(user=proxy_user).delete()
                    lecturer_profile.user = proxy_user
                else:
                    user.save()
                    lecturer_profile.user = user
                    if 'picture' in request.FILES:
                        lecturer_profile.picture = request.FILES['picture']
                lecturer_profile.save()
            registered=True

        else:  # invalid form, for whatever reason
            print(user_form.errors,student_profile_form.errors, lecturer_profile_form.errors)

    else:  # not http POST
        user_form = UserForm()
        lecturer_profile_form = LecturerProfileForm()
        student_profile_form = StudentProfileForm()
        request.session["is_ajax"] = False
    name_list_raw = LecturerProfile.objects.all().values_list('name', 'university', "user_id","department")
    name_list = []
    for name, uni, user,depart in name_list_raw:
        data = {"name": name, "uni": uni, "value": name + " - " + uni, "user": user ,"depart":depart}
        name_list.append(data)
    js_data = json.dumps(name_list)

    return render(request, 'ratemylecturer/register.html',
                  {'user_form':user_form, 'registered':registered, 'lecturer_profile_form':lecturer_profile_form,
                   'student_profile_form':student_profile_form, "name_list":js_data})

# login page view
def user_login(request):
    login_error=False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # password authentication using django
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:  # account may have been disabled
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:  # account inactive
                return HttpResponse("Your account is disabled.")

        else: # invalid login details
            login_error = True
            return render(request, 'ratemylecturer//login.html', {'error': login_error})
    else: # not a HTTP POST, hence blank dictionary object
        context_dict = {}
        return render(request,'ratemylecturer/login.html',context_dict)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@user_passes_test(UserMethods.is_student, login_url='/ratemylecturer/login/')
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
            proxy_user_count=str(proxy_user_count)
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
    return render( request,'ratemylecturer/create_lecturer.html',{'created': created, 'lecturer_profile_form':
        lecturer_profile_form, 'user_id':user_id})


def about(request):
    return render(request, 'ratemylecturer/about.html', {})

def profile(request):
    return render(request, 'ratemylecturer/profile.html', {})
