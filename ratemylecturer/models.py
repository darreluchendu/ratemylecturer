import os
import tempfile
import urllib
from urllib.request import urlretrieve, urlopen

from django.core import files
from django.core.files.base import ContentFile
from django_resized import ResizedImageField
from django.core.files.temp import NamedTemporaryFile
from PIL import Image, ImageFile

from django.contrib.auth.models import User
import requests
from django.core.files import File
from django.db import models
from io import StringIO, BytesIO


# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    university = models.CharField(max_length=30, blank=True)
    course = models.CharField(max_length=30, blank=True)
    picture =ResizedImageField(size=[500, 300],upload_to='profile_images', blank=True)
    picture_url = models.URLField(default='http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png')
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


    # def get_remote_image(self):
    #     if self.picture_url and not self.picture:
    #         result = urllib.request.urlretrieve(self.  picture_url)
    #         self.picture.save(
    #             os.path.basename(self.  picture_url),
    #             File(open(result[0]))
    #         ,save=False)
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

        # r = requests.get(url)
        #
        # with tempfile.NamedTemporaryFile(mode='wb') as img_temp:
        #     img_temp.write(r.content)
        #
        #
        # self.picture.save(url[url.rfind("/")+1:]+'.jpg', img_temp, save=False)

        # self.picture.save(url[url.rfind("/") + 1:], File(img_temp), save=True)
        # im = Image.open(url[url.rfind("/") + 1:])
        # rgb_im = im.convert('RGB')
        # self.picture.save(url[url.rfind("/") + 1:] + '.jpg', rgb_im, save=True)

    def save(self, *args, **kwargs):
        if not self.pk:
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
    picture = ResizedImageField(size=[500, 300],upload_to='profile_images', blank=True)
    picture_url = models.URLField(default='http://itccthailand.com/wp-content/uploads/2016/07/default-user-icon-profile.png',)


    def __str__(self):
        return self.user.username

    def updateRating(self):
        rating_list = []
        for r in Review.objects.filter(lecturer=self):
            rating_list.append(r.rating)
        self.rating_avr = (sum(rating_list)) / len(rating_list)
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
    #
    # def get_remote_image(self):
    #     if self.picture_url and not self.picture:
    #         result = urllib.request.urlretrieve(self.picture_url)
    #         self.picture.save(
    #             os.path.basename(self.picture_url),
    #             File(open(result[0]))
    #         )
    #         self.save(force_update=True)



    def save(self, *args, **kwargs):
        if not self.pk:
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
        if Review.objects.filter(lecturer=self).count() > 0:
            self.updateRating()

       # super(LecturerProfile, self).save(*args, **kwargs)


class Review(models.Model):
    lecturer = models.ForeignKey(LecturerProfile, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    module = models.CharField(max_length=30)
    rating = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    title = models.CharField(max_length=30)
    review_body = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if Review.objects.filter(lecturer=self.lecturer).count() > 0:
            self.lecturer.updateRating()
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
