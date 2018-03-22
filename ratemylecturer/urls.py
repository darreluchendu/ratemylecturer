from django.conf.urls import url
from ratemylecturer import views

urlpatterns = [

url(r'^$', views.index, name='index'),
url(r'^about/$', views.about, name='about'),
url(r'^add_lecturer/(?P<user_id>[\w\-]+)/$', views.create_lecturer, name='create_lecturer'),
url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
url(r'^register/lecturer_ajax_data/$', views.lecturer_ajax_data, name='lecturer_ajax_data'),
url(r'^profile/(?P<username>[\w\-]+)/add_review/$', views.add_review, name = 'add_review'),
url(r'^review/$', views.review, name = 'review'),
url(r'^register/$',views.register,name='register'),
url(r'^login/$', views.user_login, name='login'),
url(r'^logout/$', views.user_logout, name='logout'),
url(r'^edit_profile/(?P<username>[\w\-]+)/$', views.edit_profile, name='edit_profile'),

]