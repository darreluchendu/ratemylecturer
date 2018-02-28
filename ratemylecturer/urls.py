from django.conf.urls import url
from ratemylecturer import views

urlpatterns = [

url(r'^$', views.index, name='index'),
url(r'^register_student$', views.register_student, name='register_student'),
url(r'^register_lecturer$', views.register_lecturer, name='register_lecturer'),
url(r'^login$', views.user_login, name='login'),




]