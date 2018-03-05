import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','rate_my_lecturer_project.settings')

import django

django.setup()
from django.contrib.auth.models import User
from ratemylecturer.models import StudentProfile, LecturerProfile, Review

def populate():
    reviews=[
        {"module":"CS1P","rating":4,"likes":45,"dislikes":23,"body":"I loved him!!!","title":"I loved him!!!"},
        {"module":"HCI","rating":1,"likes":124,"dislikes":5,"body":"WORST MODULE EVER!","title":"WORST MODULE EVER!"},
        {"module":"ADS","rating":2,"likes":14,"dislikes":5,"body":"Poor","title":"Poor"}
    ]
    students=[
        {"username":"bob","password":12345678,"email":"ad@gmail.com","first":"Bob","sur":"Ryu","bio":"I like trains","reviews":[reviews[0]],"img":"profile_images/kid1.jpg"},
        {"username":"sam","password":12345678,"email":"sf2@gmail.com","first":"Sam","sur":"Nut","bio":"I see dead people","reviews":[reviews[1],reviews[2]],"img":"profile_images/kid2.jpg"}
    ]  
    lecturers=[
        {"username":"julia","password":12345678,"email":"asv@gmail.com","name":"Julia Ass","bio":"Easy-going Lecturer","uni":"University of North Korea","depart":"Computer Science","reviews":[reviews[0],reviews[2]],"img":"profile_images/adult2.jpg"},
        {"username":"john","password":12345678,"email":"vzs@gmail.com","name":"John Kami","bio":"The meme machine","uni":"University of your Mom","depart":"Your mom's department","reviews":[reviews[1]],"img":"profile_images/adult1.jpg"}
    ]
    for student in students:
        s=add_student(student["username"],student["password"],student["email"],student["first"],student["sur"],student["bio"],student["img"])
        for lecturer in lecturers:
            l= add_lecturer(lecturer["username"],lecturer["password"],lecturer["email"],lecturer["name"],lecturer["bio"],lecturer["uni"],lecturer["depart"],lecturer["img"])
            for review in reviews:
                if (review in student["reviews"] and review in lecturer["reviews"]):
                    add_review(l,s,review["module"],review["rating"],review["likes"],review["dislikes"],review["body"], review["title"])

    for s in StudentProfile.objects.all():
        print("Creating Student "+ s.first_name+" "+s.surname)
    for l in LecturerProfile.objects.all():
        print("Creating Lecturer "+ l.name)


def add_student(user, pas, email,first, sur,bio,img):
    user,created=User.objects.get_or_create(username=user, email=email)
    if created:
        user.set_password(pas) # This line will hash the password
    user.save()
    s=StudentProfile.objects.get_or_create(user=user)[0]
    s.surname=sur
    s.first_name=first
    s.bio=bio
    s.picture=img
    s.save()
    return s
def add_lecturer(user, pas, email,name,bio,uni,depart,img):
    user,created=User.objects.get_or_create(username=user, email=email)
    if created:
        user.set_password(pas) # This line will hash the password
    user.save()
    l=LecturerProfile.objects.get_or_create(user=user)[0]
    l.name=name

    l.bio=bio
    l.university=uni
    l.department=depart
    l.picture=img
    l.save()
    return l

def add_review(lecturer,student,module,rating,likes,dis,body,title):
    r=Review.objects.get_or_create(lecturer=lecturer, student=student, rating=rating)[0]
    r.module=module
    r.likes=likes
    r.dislikes=dis
    r.review_body=body
    r.title=title
    r.save()

if __name__ == '__main__':
    print("Starting Lecturer population script...")
    populate()