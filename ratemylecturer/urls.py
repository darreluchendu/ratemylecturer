from django.conf.urls import url
from ratemylecturer import views

urlpatterns = [

url(r'^$', views.index, name='index'),
url(r'^login/$', views.user_login, name='login'),
url(r'^about/$', views.about, name='about'),
url(r'^register/$', views.register, name='register'),
url(r'^addlecturer/(?P<user_id>[\w\-]+)/$', views.create_lecturer, name='create_lecturer'),
url(r'^profile/(?P<user_id>[\w\-]+)/$', views.profile, name='profile'),
url(r'^logout/$', views.user_logout, name='logout'),
url(r'^register/lecturer_ajax_data/$', views.lecturer_ajax_data, name='lecturer_ajax_data'),

]