# from registration.backends.default.views import RegistrationView
# from .forms import LecturerProfileForm, StudentProfileForm
# from .models import LecturerProfile, StudentProfile
# #
#
#
#
# # custom view for user registration
#
# class MyRegistrationView(RegistrationView):
#     form_class = LecturerProfileForm
#
#     def register(self,request, form_class):
#
#         new_user = super(MyRegistrationView, self).register(form_class)
#         _name = form_class.cleaned_data['name']
#         _university = form_class.cleaned_data['university']
#         _department = form_class.cleaned_data['department']
#         _bio = form_class.cleaned_data['bio']
#         _picture = form_class.cleaned_data['picture']
#         lecturer_profile = LecturerProfile.objects.create(user=new_user, name=_name,
#                                                           university=_university, department=_department, bio=_bio,
#                                                           picture=_picture)
#         lecturer_profile.save()
#         return new_user
#
#     # redirect users to index page, if successful at logging in.
#     def get_success_url(self, user):
#         return '/ratemylecturer'