# forms
from django import forms
from django.contrib.auth.models import User

from ratemylecturer.models import LecturerProfile, StudentProfile, Review

# User model's form
# (used to create new user with a username, email and password)
class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # Checks that the email is not already used and that it is a university email address
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        if email.endswith(".ac.uk") == False:
            raise forms.ValidationError("Must use university email address. i.e ends with 'ac.uk'")
        return email


# LecturerProfile model's form
# Completes the LecturerProfile model (1st part are the information from user model)
# with name, university, department, bio and profile picture
class LecturerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.pop("user")
        self.fields.pop("rating_avr")
        self.fields.pop("uni_slug")

    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'lecturer_name'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'id': 'lecturer_depart'}))
    university = forms.CharField(widget=forms.TextInput(attrs={'id': 'lecturer_uni'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = LecturerProfile
        exclude = ("picture_url",)


# StudentProfile model's form
# Completes the StudentProfile model (1st part are the information from user model)
# with first name, surname, university, course, bio and profile picture
class StudentProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.pop("user")

    first_name = forms.CharField(max_length=30, )
    surname = forms.CharField(max_length=30, )
    university = forms.CharField(max_length=30, required=False, )
    course = forms.CharField(max_length=30, required=False, )
    bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = StudentProfile
        exclude = ("picture_url",)


# Review model's form
# Allows to write new review with a title, module, body and rating as described below in the status_choices
class ReviewForm(forms.ModelForm):

    likes=forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    dislikes= forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    rating=forms.IntegerField()
    module=forms.CharField()
    # STATUS_CHOICES = (
    #     (1, 'Poor - 1 Star'),
    #     (2, 'Fair - 2 Stars'),
    #     (3, 'Average - 3 Stars'),
    #     (4, 'Good - 4 Stars'),
    #     (5, 'Excellent - 5 Stars'),
    # )
    # rating = forms.ChoiceField(choices=STATUS_CHOICES,
    #                            widget=forms.Select(attrs={'class': 'form-control input-lg'}))
    review_body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),required=False)

    class Meta:
        model = Review
        fields = ('module',  'likes', 'dislikes','rating', 'title', 'review_body')

# Edit profile picture form for students
class StudPictureForm(forms.ModelForm):
	edit_picture = forms.ImageField(required=False)
	class Meta:
		model=StudentProfile
		fields=("edit_picture",)

# Edit profile picture form for lecturers
class LecPictureForm(forms.ModelForm):
	edit_picture = forms.ImageField(required=False,)
	class Meta:
		model=LecturerProfile
		fields=("edit_picture",)