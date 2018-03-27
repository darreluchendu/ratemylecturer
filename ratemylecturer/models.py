from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    university = models.CharField(max_length=30, blank=True)
    course = models.CharField(max_length=30, blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
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
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

    def updateRating(self):
        rating_list = []
        for r in Review.objects.filter(lecturer=self):
            rating_list.append(r.rating)
        self.rating_avr = (sum(rating_list)) / len(rating_list)

    def save(self, *args, **kwargs):
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

        super(LecturerProfile, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-rating_avr']


class Review(models.Model):
    lecturer = models.ForeignKey(LecturerProfile, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    module = models.CharField(max_length=30)
    rating = models.IntegerField(default=0, )
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

    class Meta:
        proxy = True
