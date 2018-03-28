from django.contrib.auth.models import User
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver

from ratemylecturer.models import StudentProfile, LecturerProfile


class BaseLiveServerTestCase(LiveServerTestCase):

    def setUp(self):
        super(BaseLiveServerTestCase, self).setUp()
        self.driver = webdriver.Chrome()
        self.user = User.objects.create_user(username='alice', password='secret', email='alice@example.ac.uk')
        self.student_user = StudentProfile.objects.create(user=self.user, first_name='Alice', surname='Mark',
                                                          university='University of Glasgow',
                                                          course='Computer Science', bio='super student')
        self.user.save()
        self.student_user.save()

        self.user = User.objects.create_user(username='bob', password='swordfish', email='bob@example.ac.uk')

        self.lecturer_user = LecturerProfile.objects.create(user=self.user, university='Oxford University',
                                                            name='Einstein')
        self.user.save()
        self.lecturer_user.save()

    def TearDown(self):
        super(BaseLiveServerTestCase, self).tearDown()
        self.driver.quit()


class BaseRegistrationTestCase(TestCase):

    # Base class for the test cases; this sets up two users

    @classmethod
    def setUpTestData(cls):
        super(BaseRegistrationTestCase, cls).setUp()
        cls.user = User.objects.create_user(username='alice', password='secret', email='alice@example.ac.uk')
        cls.student_user = StudentProfile.objects.create(user=cls.user, first_name='Alice', surname='Mark',
                                                         university='University of Glasgow',
                                                         course='Computer Science', bio='super student')
        cls.user.save()
        cls.student_user.save()

        cls.user = User.objects.create_user(username='bob', password='swordfish', email='bob@example.ac.uk')

        cls.lecturer_user = LecturerProfile.objects.create(user=cls.user, university='Oxford University',
                                                           name='Einstein')
        cls.user.save()
        cls.lecturer_user.save()

    def setUp(self):
        super(BaseRegistrationTestCase, self).setUp()
        self.user = User.objects.create_user(username='alice', password='secret', email='alice@example.ac.uk')
        self.student_user = StudentProfile.objects.create(user=self.user, first_name='Alice', surname='Mark',
                                                          university='University of Glasgow',
                                                          course='Computer Science', bio='super student')
        self.user.save()
        self.student_user.save()

        self.user = User.objects.create_user(username='bob', password='swordfish', email='bob@example.ac.uk')

        self.lecturer_user = LecturerProfile.objects.create(user=self.user, university='Oxford University',
                                                            name='Einstein')
        self.user.save()
        self.lecturer_user.save()
