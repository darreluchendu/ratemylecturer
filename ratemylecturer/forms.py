# forms
from django import forms
from django.contrib.auth.models import User
from ratemylecturer.models import LecturerProfile, StudentProfile, Review

# base user form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields = ('username', 'email', 'password')

# LecturerProfile model's form
class LecturerProfileForm(forms.ModelForm):
    class Meta:
        model=LecturerProfile
        fields = ('name','university', 'department', 'bio', 'picture')

# StudentProfile model's form
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model=StudentProfile
        fields = ('first_name','surname','university', 'course', 'bio', 'picture')

# Review model's form
class ReviewForm(forms.ModelForm):
    likes=forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    dislikes= forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model=Review
        fields = ('module','rating', 'likes', 'dislikes', 'title', 'review_body')


