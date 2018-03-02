from django.conf.urls import url
from ratemylecturer import views

urlpatterns = [

url(r'^$', views.index, name='index'),
url(r'^login$', views.user_login, name='login'),
url(r'^about$', views.about, name='about'),
url(r'^register$', views.register, name='register'),
url(r'^profile$', views.profile, name='profile'),
url(r'^review$', views.review, name = 'review'),
url(r'^add_review$', views.add_review, name = 'add_review')






]