from django.contrib import admin

from ratemylecturer.models import StudentProfile, LecturerProfile, Review


# Register your models here
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
class StudentAdmin(admin.ModelAdmin):
    inlines =[ReviewInline]
    list_display = ("user","first_name","surname",)
    
admin.site.register(StudentProfile,StudentAdmin)

class LecturerAdmin(admin.ModelAdmin):
    list_display = ("user","first_name","surname","university","department")
    inlines =[ReviewInline]
admin.site.register(LecturerProfile,LecturerAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title","student","lecturer","module","date","rating","likes","dislikes")

admin.site.register(Review,ReviewAdmin)