from django.conf.urls import url
from ratemylecturer import views

urlpatterns = [

url(r'^$', views.index, name='index'),
<<<<<<< HEAD
url(r'^register_student/$', views.register_student, name='register_student'),
url(r'^register_lecturer/$', views.register_lecturer, name='register_lecturer'),
url(r'^create_lecturer/(?P<user_id>[\w\-]+)/$', views.create_lecturer, name='create_lecturer'),
url(r'^login/$', views.user_login, name='login'),
url(r'^logout/$', views.user_logout, name='logout'),
=======
url(r'^login$', views.user_login, name='login'),
url(r'^about$', views.about, name='about'),
url(r'^register$', views.register, name='register'),
url(r'^profile$', views.profile, name='profile'),

>>>>>>> e2316caab2b38cf06218242c1440e61c7e45dda8




]