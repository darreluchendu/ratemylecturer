import os
import random
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE','rate_my_lecturer_project.settings')

import django

django.setup()
from django.contrib.auth.models import User
from ratemylecturer.models import StudentProfile, LecturerProfile, Review
from defusedxml.lxml import fromstring
# The requests library
import requests
def UniversityScraper():
    API_url = 'https://www.topuniversities.com/sites/default/files/qs-rankings-data/357051.txt?_=1521685252703'
    scraped_unis=[]
    uni_names=[]
    response=requests.get(API_url)
    count=1

    uni_list=response.json().get('data')
    for uni in uni_list:
        uni_dict={}

        if uni['cc']=='GB':
            uni_dict['url']='https://www.topuniversities.com'+uni['url']
            uni_dict['name']=uni['title']
            uni_dict['rank']=count
            scraped_unis.append(uni_dict)

            uni_names.append(uni['title'])
            count+=1

    with open('uni_ranking.json', 'w') as json_file:
        json.dump(scraped_unis, json_file, indent=4)
    return uni_names[:20]


names=[]
universities=[]
departments=[]
courses=[]
bios=[]
pics=[]
# good_titles="excellent, superb, outstanding, magnificent, of the highest quality, of the highest standard, exceptional, marvellous, wonderful, first-rate, first-class, superlative, splendid, admirable, worthy, sterling"
# titles_g=[]
# for elm in good_titles.split(','):
#     titles_g.append(elm.strip())
# bad_titles='substandard, poor, inferior, second-rate, second-class, unsatisfactory, inadequate, unacceptable, not up to scratch, not up to par, deficient, imperfect, defective, faulty, shoddy, amateurish, careless, negligent'
# titles_b=-[]
# for elm in bad_titles.split(','):
#     titles_b.append(elm.strip())
comments_b=['Impossible to understand! Even if you can decipher his words, he talks so fast its impossible to write notes. Uses NO slides either',
            'His expectations are undefined and his lectures are pointless. I definetly do not recommend this crazy man.',
            'He speaks too fast to write his notes and often gets mad if you ask him to repeat, but do because you will need this info for the exams.',
            'Not a good experience. Marks too hard. Insane notes didnt narrow down content on exams. My worst uni grade ever',
            'Develope hardcore note taking skills before entering the class. The class killed my interest for this subject',
            'He seems like a nice guy, but the info that was taught was not organized enough',
            'Hard accent to understand some of the time, and tooooo many notes']
comments_g=['Amazing. All you need to do is show up to class and listen to her. Her lectures are phenomenal and she is hilarious. '
            'She should seriously consider stand-up comedy.',
            'She is an easy grader. Easy A is guaranteed.',
            'Fun and easy professor. Easiest A ever!!!!!!',
            'Inspirational professor. Young and very smart, I would take Speech 101 with her again any day.',
            'The best of the best. A true professional and wonderful professor. She gets an A+ from me.',
            'Caring professor who will make sure you show up to class and learn. She helped me get rid of my fears of public speaking.',
            'A highly intelligent professor, always available to answer any and all of my questions that I email even if at 1 AM. She knows her stuff and loves what she does. I couldnt have asked for more']
modules=['ECON1001''ECON1002','MGT1003','MGT1004','ACCFIN1003','ACCFIN1004','ACCFIN1018','COMPSCI1002','COMPSCI1018',
         'COMPSCI1005','MATHS1001','MATHS1002','MATHS1004','CHEM1004','CHEM1002','CHEM1003','ENG1022','LAW1021','LAW1022',]
#getting data from files
with open('Lecturers.txt', encoding='utf-8') as names_file, open('courses.txt') as courses_file:
    for line in names_file:
        names.append(line.strip())
    for line in courses_file:
        courses.append((line.strip()))
with open('UniversityList.txt') as uniList, open('U_Departments.txt') as depart:
   # for line in uniList:
     #   universities.append(line.strip())
    for line in depart:
        departments.append(line.strip())
with open('bios.txt', encoding='utf-8') as bioList, open('pictures.txt', encoding='utf-8') as picList:
    for line in bioList:
        bios.append(line.strip())
    for line in picList:
        pics.append(line.strip())
for uni in UniversityScraper():
    universities.append(uni)

def populate():
    for name in names[:20]:
        s=add_student(name)
        print("Creating Student " + s.first_name + " " + s.surname,'-',num_users)
    #adding lecturers with good reviews
    start = 20
    end = 23
    for n in universities:
        for name in names[start:end]:
            l=add_lecturer(name,n)
            print("Creating Lecturer " + l.name,'-',num_users)
            for stud in StudentProfile.objects.all()[:5]:
                add_review(l,stud)
            rating_list = []
            for r in Review.objects.filter(lecturer=l):
                rating_list.append(r.rating)
            l.rating_avr = (sum(rating_list)) / len(rating_list)
            l.save()
        start+=3
        end+=3

            # for r in Review.objects.filter(lecturer=l):
            #     rating_list.append(r.rating)
            # l.rating_avr = (sum(rating_list)) / len(rating_list)
            # l.save()
        # adding lecturers with bad reviews
        # for i in range(1):
        #     l = add_lecturer(n)
        #     print("Creating Lecturer " + l.name, '-', num_users)
        #     for stud in StudentProfile.objects.all()[5:10]:
        #         add_review(l, stud, False)
        #     rating_list=[]
        #     for r in  Review.objects.filter(lecturer=l):
        #         rating_list.append(r.rating)
        #     l.rating_avr=(sum(rating_list))/len(rating_list)
        #     l.save()
# creating test accounts username  can be either 'test_student or 'test_Lecturer'; password is below
    test_s=add_student('Test Student')
    test_s.user.set_password('testpassword')
    test_s.user.save()
    for lec in LecturerProfile.objects.all()[5:10]:
        add_review(lec, test_s)

    test_l = add_lecturer('Test Lecturer',random.choice(universities))
    test_l.user.set_password('testpassword')
    test_l.user.save()
    for stud in StudentProfile.objects.all()[5:10]:
        add_review(test_l, stud)
    rating_list = []
    for r in Review.objects.filter(lecturer=test_l):
        rating_list.append(r.rating)
    test_l.rating_avr = (sum(rating_list)) / len(rating_list)
    test_l.save()
num_users=0
def add_student(name):
    rand_password = User.objects.make_random_password()
    global num_users
    num_users+=1
    proxy_user_count =num_users

    proxy_user_count = str(proxy_user_count)
    user = User.objects.get_or_create(username=(name.split()[0] + '_'+name.split()[1]).lower(),
                               email="proxy_user" + proxy_user_count + '@gmail.com')[0]
    user.set_password(rand_password)
    user.save()
    s=StudentProfile.objects.get_or_create(user=user)[0]

    s.surname=name.split()[1]
    s.first_name=name.split()[0]
    s.bio=random.choice(bios)
    s.course=random.choice(courses)
    s.university=random.choice(universities)
    s.picture=random.choice(pics)
    s.save()
    return s

def add_lecturer(name,university):

    rand_password = User.objects.make_random_password()
    global num_users
    num_users += 1
    proxy_user_count =num_users
    proxy_user_count = str(proxy_user_count)
    user = User.objects.get_or_create(username=(name.split()[0] + '_'+name.split()[1]).lower(),
                               email="proxy_user" + proxy_user_count + '@gmail.com')[0]
    user.set_password(rand_password)
    user.save()
    l = LecturerProfile.objects.get_or_create(user=user)[0]
    l.name = name
    l.bio = random.choice(bios)
    l.university = university
    l.picture=random.choice(pics)
    l.rating_avr=0
    l.save()
    return l

def add_review(lecturer,student):
    r=Review.objects.get_or_create(lecturer=lecturer, student=student)[0]
    r.module=random.choice(modules)

    r.likes=random.randrange(1,15)
    r.dislikes=random.randrange(1,10)
    good = random.choice([True, False])
    if good==True:
        r.review_body=random.choice(comments_g)
        r.rating = random.randint(4, 5)
    else:
        r.review_body = random.choice(comments_b)
        r.rating = random.randint(1, 3)
    if r.rating==1:
        r.title='Terrible'
    elif r.rating==2:
        r.title='Mediorce'
    elif r.rating==3:
        r.title='Average'
    elif r.rating == 4:
        r.title = 'Good'
    elif r.rating == 5:
        r.title = 'Excellent'
    r.save()

if __name__ == '__main__':
    print("Starting Rate My Lecturer population script...")
    populate()