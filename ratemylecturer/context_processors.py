import json
from django.contrib.auth.models import User
from .models import UserMethods,LecturerProfile

def glb_var(request):
    lecturer_list=[]
    lecturers=LecturerProfile.objects.all().values_list("name", 'university', "user_id")
    for name, uni, user, in lecturers:
        user=User.objects.get(pk=user)
        data = {"label": name + " - " + uni,"category":"Lecturers", "username": user.username}
        lecturer_list.append(data)
    js_data=json.dumps(lecturer_list)
    isStudent= UserMethods.is_student(request.user)
    return {"is_student": isStudent, 'lecturers':lecturer_list}