


from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_resized import ResizedImageField

from PIL import Image

from django.contrib.auth.models import User
import requests

from django.db import models
from io import BytesIO


# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    university = models.CharField(max_length=30, blank=True)
    course = models.CharField(max_length=30, blank=True)
    picture =ResizedImageField(size=[600, 500],upload_to='profile_images', blank=True)
    picture_url = models.URLField()
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username



    def save_image_from_url(self, url):
        if url and not self.picture:
            image_request_result = requests.get(url)
            image = Image.open(BytesIO(image_request_result.content))
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            # width, height = image.size
            # max_size = [200, 200]
            # if width > 200 or height > 200:
            #     image.thumbnail(max_size)
            file_name = url[url.rfind("/") + 1:]
            image_io = BytesIO()
            image.save(image_io, format='JPEG')
            self.picture.save(file_name, ContentFile(image_io.getvalue()) ,save=False)


    def save(self, *args, **kwargs):
        if not self.picture:
            self.save_image_from_url(self.picture_url)
        for field in ['course', 'university']:
            new_val = []
            val = getattr(self, field, False)
            if val:
                val_list = val.split(' ')
                if len(val_list) > 1:
                    for word in val_list:
                        if len(word) > 3 or val_list.index(word) == 0 or val_list.index(word) == len(val_list) - 1:
                            new_val.append(word.capitalize())
                        else:
                            new_val.append(word)
                    setattr(self, field, ' '.join(new_val))
                else:
                    setattr(self, field, val.capitalize())

        for field_name in ['first_name', 'surname']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())

        super(StudentProfile, self).save(*args, **kwargs)


class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    rating_avr = models.FloatField(default=0)
    university = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    bio = models.CharField(max_length=200, blank=True)
    picture = ResizedImageField(size=[600, 500],upload_to='profile_images', blank=True)
    picture_url = models.URLField()


    def __str__(self):
        return self.user.username


    def save_image_from_url(self, url):
        if url and not self.picture:
            image_request_result = requests.get(url)
            image = Image.open(BytesIO(image_request_result.content))
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            # width, height = image.size
            # max_size = [200, 200]
            # if width > 200 or height > 200:
            #     image.thumbnail(max_size)
            file_name = url[url.rfind("/") + 1:]
            image_io = BytesIO()
            image.save(image_io, format='JPEG')
            self.picture.save(file_name, ContentFile(image_io.getvalue()),save=False)



    def save(self, *args, **kwargs):
        if not self.picture:
            self.save_image_from_url(self.picture_url)
        for field in ['department', 'university']:
            new_val = []
            val = getattr(self, field, False)
            if val:
                val_list = val.split(' ')
                if len(val_list) > 1:
                    for word in val_list:
                        if len(word) > 3 or val_list.index(word) == 0 or val_list.index(word) == len(val_list) - 1:
                            new_val.append(word.capitalize())
                        else:
                            new_val.append(word)
                    setattr(self, field, ' '.join(new_val))
                else:
                    setattr(self, field, val.capitalize())
        name = getattr(self, 'name', False)
        setattr(self, 'name', name.title())


        super(LecturerProfile, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-rating_avr']


class Review(models.Model):
    lecturer = models.ForeignKey(LecturerProfile, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    module = models.CharField(max_length=30)
    rating = models.IntegerField(default=0, )
    date = models.DateField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    title = models.CharField(max_length=30)
    review_body = models.CharField(max_length=200, blank=True)
    # class Meta:
    #     ordering = ['-date']
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)

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
    def is_owner(self,username):
        if self.is_authenticated:
            if self.username==username:
                return True
            else:
                return False
        else:
         return False
    class Meta:
        proxy = True
