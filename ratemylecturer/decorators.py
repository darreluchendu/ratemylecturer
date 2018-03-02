from django.db import models
from django.contrib.auth.models import User

def user_is_student(function):
    def wrap(request, *args, **kwargs):
        user =User.objects.get(pk=user.id)
        if entry.created_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap