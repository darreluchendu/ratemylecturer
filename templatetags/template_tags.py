from django import template
from ratemylecturer.forms import StudentProfileForm,LecturerProfileForm

register = template.Library()

#This is just to customize the page rendering
@register.filter
def get_label(field):
    return field.label