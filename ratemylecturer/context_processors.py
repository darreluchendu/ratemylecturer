from .models import UserMethods


def glb_var(request):
    isStudent= UserMethods.is_student(request.user)
    return {"is_student": isStudent}