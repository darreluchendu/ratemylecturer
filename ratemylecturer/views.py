import json
import operator

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from ratemylecturer.forms import LecturerProfileForm, StudentProfileForm, ReviewForm, UserForm, StudPictureForm,LecPictureForm


from ratemylecturer.models import Review, StudentProfile, LecturerProfile, UserMethods


def index(request):
    new_reviews=[]
    new_names=[]
    reviews_list = reversed(Review.objects.all())


    for i in reviews_list:
        if i.lecturer not in new_names:
            new_reviews.append(i)
            new_names.append(i.lecturer)
            if len(new_reviews)==3:
                break
    print(new_names)
    # calculating uni average rating
    universities = set()
    lecturers = LecturerProfile.objects.all()
    for lecturer in lecturers:
        universities.add(lecturer.university)
    # get all reviews attributed to lecturers in a university
    uni_avg_rating = {}
    for university in universities:
        lecturer_s = LecturerProfile.objects.filter(university=university)
        rating_avg_sum = 0.0
        for lec in lecturer_s:
            rating_avg_sum += lec.rating_avr
        num_lecturer = lecturer_s.count()
        uni_avg_rating[university] = rating_avg_sum / num_lecturer
    top_uni = sorted(uni_avg_rating.items(), key=operator.itemgetter(1))
    top_uni.reverse()

    top_lect = LecturerProfile.objects.order_by('-rating_avr')[:5]
    # uni_ratings = Review.objects.filter(lecturer__university=university)
    context_dict = {'reviews': new_reviews[:3], 'user': request.user, 'top_lecturer': top_lect, 'nbar': "home",
                    'top_uni': top_uni[:5]}
    return render(request, 'ratemylecturer/index.html', context_dict)


def about(request):
    return render(request, 'ratemylecturer/about.html', {'nbar': 'about'})


@csrf_exempt
def lecturer_ajax_data(request):
    post_data = json.loads(request.body.decode('utf-8'))
    proxy_user = post_data["user"]

    request.session["user_id"] = proxy_user
    request.session["is_ajax"] = True

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
            return render(request, 'ratemylecturer/login.html', {'invalid_login': invalid_login, 'nbar': "login"})
    else:
        return render(request, 'ratemylecturer/login.html', {'invalid_login': invalid_login, 'nbar': "login"})


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
                    student_profile.picture_url = 'http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png'
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
                    lecturer_profile.picture_url = 'http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png'
                lecturer_profile.save()
            registered = True
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect("/ratemylecturer/")
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
                   'student_profile_form': student_profile_form, "name_list": js_data, 'nbar': "register"})


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
            num_users = str(User.objects.all().count() + 1)
            name = lecturer_profile.first_name.lower()
            name.replace(" ", "_")
            if User.objects.filter(username=name).exists():
                username = name + num_users
            else:
                username = name
            user = User.objects.create(username=username,email="proxy_user" +num_users + '@gmail.com')
            user.set_password(rand_password)
            user.save()
            lecturer_profile.user = user
            if 'picture' in request.FILES:
                lecturer_profile.picture = request.FILES['picture']
            else:
                lecturer_profile.picture_url = 'http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png'
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
    def percent(rating_count, total_rating):
        if total_rating:
            x= int(rating_count*100/total_rating)
            return str(x)+"%"
        else:
            return 'No rating here'

    profile_user = User.objects.get(username=username)

    owner=UserMethods.is_owner(request.user,username)
    context_dict = {'owner':owner}

    if owner:
        if UserMethods.is_student(request.user):
            pic_form=StudPictureForm(instance=StudentProfile.objects.get(user=profile_user))
        else:
            pic_form = LecPictureForm(instance=LecturerProfile.objects.get(user=request.user))
        context_dict['pic_form']=pic_form

    if UserMethods.is_student(profile_user):
        student_profile = StudentProfile.objects.get(user=profile_user)
        student_reviews = Review.objects.filter(student=student_profile).order_by('-date')
        context_dict['profile'] = student_profile
        context_dict['reviews'] = student_reviews
        context_dict["student_profile"] = True

    else:
        lecturer_profile = LecturerProfile.objects.get(user=profile_user)
        lecturer_reviews = Review.objects.filter(lecturer=lecturer_profile).order_by('-date')
        context_dict['profile'] = lecturer_profile
        context_dict['reviews'] = lecturer_reviews
        context_dict['one_star_rating_count'] = lecturer_reviews.filter(rating=1).count()
        context_dict['two_star_rating_count'] = lecturer_reviews.filter(rating=2).count()
        context_dict['three_star_rating_count'] = lecturer_reviews.filter(rating=3).count()
        context_dict['four_star_rating_count'] = lecturer_reviews.filter(rating=4).count()
        context_dict['five_star_rating_count'] = lecturer_reviews.filter(rating=5).count()

        context_dict['total_star_rating'] = lecturer_reviews.count()

        if context_dict['total_star_rating']!=0:
            context_dict['percentages'] = [
                    percent(context_dict['five_star_rating_count'], context_dict['total_star_rating']),
                    percent(context_dict['four_star_rating_count'], context_dict['total_star_rating']),
                    percent(context_dict['three_star_rating_count'], context_dict['total_star_rating']),
                    percent(context_dict['two_star_rating_count'], context_dict['total_star_rating']),
                    percent(context_dict['one_star_rating_count'], context_dict['total_star_rating'])
                    ]
        else:
            context_dict['percentages']=["0%","0%","0%","0%","0%"]

        context_dict["student_profile"] = False
    context_dict["profile_user"] = username
    context_dict['nbar'] = 'profile'
    return render(request, 'ratemylecturer/profile.html', context_dict)


@user_passes_test(UserMethods.is_student)
@login_required()
def add_review(request, username):
    profile_user=User.objects.get(username=username)
    added = False
    student = StudentProfile.objects.get(user=request.user)
    lecturer = LecturerProfile.objects.get(user=profile_user)

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.lecturer = lecturer
            review.student = student
            if Review.objects.filter(lecturer=lecturer,student=student).exists():
                Review.objects.get(lecturer=lecturer, student=student).delete()
            review.save()
            added = True

            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
        else:  # invalid form, for whatever reason
            print(review_form.errors)
    else:  # not http POST
        review_form = ReviewForm()
    review_form.fields['rating'].widget = forms.HiddenInput()
    return render(request, 'ratemylecturer/add_review.html', {'review_form': review_form,
                                                              'username': username,'lecturer':lecturer, 'nbar': 'profile'})


# creates student profile for user who logs in using google or facebook
def save_profile(backend, user, response, details, **kwargs):
    num_users = str(User.objects.all().count() + 1)
    fname = details.get('first_name').lower()
    sname = details.get('last_name').lower()
    fname.replace(" ", "_")
    sname.replace(" ", "_")
    username = fname +'_'+ sname
    if User.objects.filter(username=username).exists():
        user.username = username + num_users
    else:
        user.username = username
    if backend.name == 'facebook':
        profile = StudentProfile.objects.get_or_create(user_id=user.id)[0]
        profile.first_name = details.get('first_name')
        profile.surname = details.get('last_name')

        profile.picture_url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        profile.save()

    elif backend.name == 'google-oauth2':
        profile = StudentProfile.objects.get_or_create(user_id=user.id)[0]
        profile.picture_url ='http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png'
        profile.first_name = details.get('first_name').capitalize()
        profile.surname = details.get('last_name').capitalize()
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


@login_required
def edit_profile(request, username):

    profile_user = User.objects.get(username=request.user)

    if request.method == 'POST':
        if UserMethods.is_student(profile_user):
           profile_form = StudentProfileForm(request.POST,instance=StudentProfile.objects.get(user=request.user))
        else:
            profile_form = LecturerProfileForm(request.POST, instance=LecturerProfile.objects.get(user=request.user))
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)

            profile.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'username': request.user.username}))
    else:

        if UserMethods.is_student(profile_user):
            stud_dict = model_to_dict(StudentProfile.objects.filter(user=request.user)[0])
            profile_form = StudentProfileForm(initial=stud_dict,instance=StudentProfile())

        else:
            lec_dict = model_to_dict(LecturerProfile.objects.filter(user=request.user)[0])
            profile_form = LecturerProfileForm(initial=lec_dict,instance=LecturerProfile())
        profile_form.fields['picture'].widget = forms.HiddenInput()
    return render(request, 'ratemylecturer/edit_profile.html', {'profile_form': profile_form,'nbar': 'profile'})
@login_required
def editPicture(request,username):

    if UserMethods.is_student(request.user):
        prof_obj=StudentProfile.objects.get(user=request.user)
        pic_form=StudPictureForm(request.POST,instance=prof_obj)
    else:
        prof_obj = LecturerProfile.objects.get(user=request.user)
        pic_form = LecPictureForm(request.POST,instance=prof_obj)

    pic=pic_form.save(commit=False)
    print (request.FILES)

    if 'edit_picture' in request.FILES:
        pic.picture = request.FILES['edit_picture']
    pic.save()
    return HttpResponseRedirect(reverse('profile', kwargs={'username': request.user.username}))

@receiver(post_save, sender=LecturerProfile)
def updateRating(sender, instance,**kwargs):
    rating_list = []
    for r in Review.objects.filter(lecturer=instance):
        rating_list.append(r.rating)
    instance.rating_avr = (sum(rating_list)) / len(rating_list)
    instance.save()

@receiver(post_save, sender=Review)
def updateRating(sender, instance,**kwargs):
    lecturer=instance.lecturer
    rating_list = []
    for r in Review.objects.filter(lecturer=lecturer):
        rating_list.append(r.rating)
    lecturer.rating_avr = sum(rating_list)/ len(rating_list)
    lecturer.save()



