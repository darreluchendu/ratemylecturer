# forms
from django import forms
from django.contrib.auth.models import User
from ratemylecturer.models import LecturerProfile, StudentProfile, Review


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')



    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email

# LecturerProfile model's form

class LecturerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.pop("user")
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'lecturer_name'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'id': 'lecturer_depart'}))
    university = forms.CharField(widget=forms.TextInput(attrs={'id': 'lecturer_uni'}))
    bio = forms.CharField(widget=forms.Textarea(), required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model=LecturerProfile
        exclude=("",)
# StudentProfile model's form
class StudentProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.pop("user")
    first_name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    university = forms.CharField(max_length=30,required=False)
    course = forms.CharField(max_length=30,required=False)
    bio = forms.CharField(widget=forms.Textarea(), required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model=StudentProfile
        exclude=("",)

# Review model's form
class ReviewForm(forms.ModelForm):
    likes=forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    dislikes= forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Review
        fields = ('module', 'rating', 'likes', 'dislikes', 'title', 'review_body')
