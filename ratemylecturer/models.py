from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class StudentProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    first_name= models.CharField(max_length=30)
    surname= models.CharField(max_length=30)
    university = models.CharField(max_length=30, blank=True)
    course = models.CharField(max_length=30, blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio=models.CharField( max_length=200, blank=True)

    def __str__(self):
        return self.user.username

class LecturerProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=30)

    university=models.CharField(max_length=30)
    department=models.CharField(max_length=30)
    bio = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Review(models.Model):

    lecturer=models.ForeignKey(LecturerProfile, on_delete=models.CASCADE)
    student=models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    module= models.CharField(max_length=30)
    rating=models.IntegerField()
    date= models.DateField(auto_now_add=True)
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    title=models.CharField(max_length=30)
    review_body=models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title
# for defining custom user methods
class UserMethods(User):
    def is_student(self):
        if self.is_authenticated:
            try:
                user_profile = StudentProfile.objects.get(user=self)
                return True
            except StudentProfile.DoesNotExist:
                return False
        else:
            return False
    class Meta:
        proxy=True
