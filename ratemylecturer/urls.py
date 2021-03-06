from django.conf.urls import url

from ratemylecturer import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^universities/(?P<uni_slug>[\w\-]+)/$', views.uni_detail, name='universities'),
    url(r'^search$', views.search, name='search'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_lecturer/(?P<user_id>[\w\-]+)/$', views.create_lecturer, name='create_lecturer'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^register/lecturer_ajax_data/$', views.lecturer_ajax_data, name='lecturer_ajax_data'),
    url(r'^profile/(?P<username>[\w\-]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/(?P<username>[\w\-]+)/edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/edit_picture/$', views.editPicture, name='editPicture'),


]