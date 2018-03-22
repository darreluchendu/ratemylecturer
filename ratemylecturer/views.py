import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from ratemylecturer.forms import LecturerProfileForm, StudentProfileForm, ReviewForm, UserForm
from ratemylecturer.models import Review, StudentProfile, LecturerProfile, UserMethods


def index(request):
    reviews_list = Review.objects.order_by('-date')[:3]
    context_dict = {'reviews': reviews_list}
    return render(request, 'ratemylecturer/index.html', context_dict)


def about(request):
    return render(request, 'ratemylecturer/about.html', {})


@csrf_exempt
def lecturer_ajax_data(request):
    post_data = json.loads(request.body.decode('utf-8'))
    proxy_user = post_data["user"]

    request.session["user_id"]=proxy_user
    request.session["is_ajax"] =True

    return HttpResponse("")


def user_login(request):
    invalid_login = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled")
        else:  # invalid login details
            invalid_login = True
            return render(request, 'ratemylecturer/login.html', {'invalid_login': invalid_login})
    else:
        return render(request, 'ratemylecturer/login.html', {'invalid_login': invalid_login})


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
                if 'picture' in request.FILES:
                    student_profile.picture = request.FILES['picture']
                else:
                    student_profile.picture = 'http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png'
                user.save()
                student_profile.user = user
                student_profile.save()

            if lecturer_profile_form.is_valid():
                lecturer_profile = lecturer_profile_form.save(commit=False)
                if request.session.get("is_ajax"):
                    # save user form data
                    # adding real user to an already created lecturer
                    proxy_user_id = request.session.get("user_id")
                    proxy_user = User.objects.get(pk=proxy_user_id)
                    proxy_user.username = user.username
                    proxy_user.email = user.email
                    proxy_user.set_password(user.password)
                    proxy_user.save()

                    lecturer_profile.user = proxy_user
                    LecturerProfile.objects.filter(user=proxy_user).delete()

                else:
                    user.save()
                    lecturer_profile.user = user
                if 'picture' in request.FILES:
                    lecturer_profile.picture = request.FILES['picture']
                else:
                    lecturer_profile.picture = 'http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png'
                lecturer_profile.save()
            registered = True
        else:  # invalid form, for whatever reason
            print(user_form.errors, student_profile_form.errors, lecturer_profile_form.errors)

    else:  # not http POST
        user_form = UserForm()
        lecturer_profile_form = LecturerProfileForm()
        student_profile_form = StudentProfileForm()
    name_list_raw = []
    request.session["is_ajax"] = False
    name_list = []
    for user in User.objects.filter(email__startswith="proxy_user"):

        name_list_raw = LecturerProfile.objects.filter(user=user).values_list("name", 'university', "user_id",
                                                                              "department")
        for name, uni, user, depart in name_list_raw:
            data = {"name": name, "uni": uni, "value": name + " - " + uni, "user": user, "depart": depart}
            name_list.append(data)
    js_data = json.dumps(name_list)

    return render(request, 'ratemylecturer/register.html',
                  {"user_form": user_form, 'registered': registered, 'lecturer_profile_form': lecturer_profile_form,
                   'student_profile_form': student_profile_form, "name_list": js_data})


@user_passes_test(UserMethods.is_student)
@login_required
def create_lecturer(request, user_id):
    created = False
    # flag to tell if registration is successful
    if request.method == 'POST':

        lecturer_profile_form = LecturerProfileForm(data=request.POST)
        if lecturer_profile_form.is_valid():
            # save user form data
            lecturer_profile = lecturer_profile_form.save(commit=False)
            rand_password = User.objects.make_random_password()
            proxy_user_count = LecturerProfile.objects.all().count() + 1
            proxy_user_count = str(proxy_user_count)
            user = User.objects.create(username="proxy_user" + proxy_user_count,
                                       email="proxy_user" + proxy_user_count + '@gmail.com')
            user.set_password(rand_password)
            user.save()
            lecturer_profile.user = user
            if 'picture' in request.FILES:
                lecturer_profile.picture = request.FILES['picture']
            else:
                lecturer_profile.picture = 'http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png'
            lecturer_profile.save()
            created = True
        else:  # invalid form, for whatever reason
            print(lecturer_profile_form.errors)
    else:  # not http POST
        lecturer_profile_form = LecturerProfileForm()
    return render(request, 'ratemylecturer/create_lecturer.html',
                  {'created': created, 'lecturer_profile_form': lecturer_profile_form, "user_id": user_id, })


# Profile
def profile(request, username):
    profile_user = User.objects.get(username=username)
    context_dict = {}
    if UserMethods.is_student(profile_user):
        student_profile = StudentProfile.objects.get(user=profile_user)
        student_reviews = Review.objects.filter(student=student_profile)
        context_dict['profile'] = student_profile
        context_dict['reviews'] = student_reviews
        context_dict["student_profile"] = True
    else:
        lecturer_profile = LecturerProfile.objects.get(user=profile_user)
        lecturer_reviews = Review.objects.filter(lecturer=lecturer_profile)
        context_dict['profile'] = lecturer_profile
        context_dict['reviews'] = lecturer_reviews
        # Yusuf - average rating
        # rating_sum =

        context_dict["student_profile"] = False
    context_dict["profile_user"] = username

    return render(request, 'ratemylecturer/profile.html', context_dict)


def review(request):
    context_dict = {}
    return render(request, 'ratemylecturer/review.html')


@user_passes_test(UserMethods.is_student)
@login_required()
def add_review(request, username):
    added = False
    lecturer = User.objects.get(username=username)
    lecturer_id = lecturer.id
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.lecturer = lecturer_id
            review.student = request.user.id
            review.save()
            added = True
        else:  # invalid form, for whatever reason
            print(review_form.errors)
    else:  # not http POST
        review_form = ReviewForm()

    return render(request, 'ratemylecturer/add_review.html', {})


# creates student profile for user who logs in using google or facebook
def save_profile(backend, user, response, details, **kwargs):
    num_users = str(User.objects.all().count() + 1)
    fname = details.get('first_name').lower()
    sname=details.get('last_name').lower()
    fname.replace(" ","_")
    sname.replace(" ","_")
    username=fname+sname
    if User.objects.filter(username=username).exists():
        user.username = details.get('first_name').lower() + '_' + details.get('last_name').lower() + num_users
    else:
        user.username = details.get('first_name').lower() + '_' + details.get('last_name').lower()
    if backend.name == 'facebook':
        profile = StudentProfile.objects.get_or_create(user_id=user.id)[0]
        profile.first_name = details.get('first_name')
        profile.surname = details.get('last_name')

        profile.picture = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        profile.save()

    elif backend.name == 'google-oauth2':
        profile = StudentProfile.objects.get_or_create(user_id=user.id)[0]

        profile.first_name = details.get('first_name').capitalize()
        profile.surname = details.get('last_name').capitalize()
        if response['image'].get('isDefault') == False:
            profile.picture = response['image'].get('url')
        else:
            profile.picture = 'http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png'
        profile.save()


def check_email_exists(request, details, *args, **kwargs):
    email = details.get('email', '')
    # check if given email is in use
    count = User.objects.filter(email=email).count()
    if count > 0:
        user = User.objects.get(email=email)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect(reverse('index'))


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
