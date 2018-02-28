from django.shortcuts import render
from ratemylecturer.forms import UserForm,LecturerProfileForm, StudentProfileForm, ReviewForm


def index(request):
    return render(request,'ratemylecturer/index.html',{})

# view for registration
def register(request):
    registered = False; # flag to tell if registration is successful
    lecturer = False
    student = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if request.POST.get("student"):# student button clicked
            student = True
            student_profile_form = StudentProfileForm(data=request.POST)
            # if userForm and any of the two is valid
            if user_form.is_valid() and student_profile_form.is_valid():
                # save user form data
                user = user_form.save()
                user.set_password(user.password)
                user.save();
                # save student profile data
                # commit = false until ready to commit to avoid interity problem
                studentProfile = student_profile_form.save(commit=False)
                studentProfile.user = user
                if 'picture' in request.FILES:
                    studentProfile.picture = request.FILES['picture']
                studentProfile.save()
                registered = True
            else:  # invalid form, for whatever reason
                print(user_form.errors, student_profile_form.errors)
         # lecturer button clicked
        if request.POST.get("lecturer"):# lecturer button clicked
            lecturer = True
            lecturer_profile_form = LecturerProfileForm(data=request.POST)
            if user_form.is_valid() and student_profile_form.is_valid():
                # save user form data
                user = user_form.save()
                user.set_password(user.password)
                user.save();

                lecturerProfile = lecturer_profile_form.save(commit=False)
                lecturerProfile.user = user
                if 'picture' in request.FILES:
                    lecturerProfile.picture = request.FILES['picture']
                lecturerProfile.save()
                registered = True


            else:#invalid form, for whatever reason
                print(user_form.errors, lecturer_profile_form.errors)

    else:# not http POST
        user_form = UserForm()
        student_profile_form = StudentProfileForm()
        lecturer_profile_form  = LecturerProfileForm()
        context_dict = None
    if student:
        return render( request,'ratemylecturer/register.html',{'user_form':user_form,'student_profile_form':student_profile_form, 'registered': registered, 'student':
                            student})
    if lecturer:
        return render(request,'ratemylecturer/register.html',{'user_form':user_form,'lecturer_profile_form':lecturer_profile_form, 'registered': registered,
                            'lecturer':lecturer})








