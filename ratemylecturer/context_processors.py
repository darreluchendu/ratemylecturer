import json
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from .models import UserMethods,LecturerProfile

def glb_var(request):
    lecturer_list=[]
    lecturers=LecturerProfile.objects.all().values_list("name", 'university', "user_id")
    isStudent = UserMethods.is_student(request.user)
    # universities = set()
    # for lecturer in LecturerProfile.objects.all():
    #     universities.add(lecturer.university)
    # uni_avg_rating = []
    # for university in universities:
    #     lecturer_s = LecturerProfile.objects.filter(university=university)
    #     rating_avg_sum = 0.0
    #     for lec in lecturer_s:
    #         rating_avg_sum += lec.rating_avr
    #     num_lecturer = lecturer_s.count()
    #     uni_avg_rating[university] rating_avg_sum / num_lecturer, 'slug': slugify(university)})
    for name, uni, user in lecturers:
        user=User.objects.get(pk=user)
        data = {"label": name + " - " + uni,"category":"Lecturers", "username": user.username,}
        lecturer_list.append(data)
    for  uni,slug, in LecturerProfile.objects.all().values_list('university', "uni_slug"):
        data = {"label": uni ,"category":"University", 'slug':slug}
        if data not in lecturer_list:
            lecturer_list.append(data)

    return {"is_student": isStudent, 'lecturers':lecturer_list}