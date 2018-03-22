from django.contrib.auth.models import User
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver

from ratemylecturer.models import StudentProfile, LecturerProfile


class BaseLiveServerTestCase(LiveServerTestCase):

    def setUp(self):
        super(BaseLiveServerTestCase, self).setUp()
        self.driver = webdriver.Chrome()
        #
        #
        # # Get the list of all users before the tests.
        # # Must evaluate the QuerySet or it will be lazily-evaluated later, which is wrong.
        # self.users_before = list(User.objects.values_list('id', flat=True).order_by('id'))
        # print(self.users_before)

    def TearDown(self):
        super(BaseLiveServerTestCase, self).tearDown()
        self.driver.quit()

        # # Get the list of all users after the tests.
        # users_after = list(User.objects.values_list('id', flat=True).order_by('id'))
        #
        # # Calculate the set difference.
        # users_to_remove = sorted(list(set(users_after) - set(self.users_before)))
        # print(users_to_remove)
        #
        # # Delete that difference from the database.
        # User.objects.filter(id__in=users_to_remove).delete()


class BaseRegistrationTestCase(TestCase):

    # Base class for the test cases; this sets up two users

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
