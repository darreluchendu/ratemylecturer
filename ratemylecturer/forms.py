# forms
from django import forms
from django.contrib.auth.models import User
from ratemylecturer.models import LecturerProfile, StudentProfile, Review
from registration.forms import RegistrationForm, RegistrationFormUniqueEmail


# base user form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


# LecturerProfile model's form
# class LecturerProfileForm(forms.ModelForm):
#  class Meta:
#       model=LecturerProfile
#        fields = ('first_name','surname','university', 'department', 'bio', 'picture')
#
# LecturerProfile model's form
class LecturerProfileForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    university = forms.CharField(max_length=30)
    department = forms.CharField(max_length=30)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    picture = forms.ImageField(required=False)


# StudentProfile model's form
class StudentProfileForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    university = forms.CharField(max_length=30)
    course = forms.CharField(max_length=30)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    picture = forms.ImageField(required=False)


# Review model's form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('module', 'rating', 'likes', 'dislikes', 'title', 'review_body')
