from selenium import webdriver
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models    import User

class BaseLiveServerTestCase(LiveServerTestCase):
    def setUp(self):
        super(BaseLiveServerTestCase,self).setUp()
        self.driver = webdriver.Chrome()
        #
        #
        # # Get the list of all users before the tests.
        # # Must evaluate the QuerySet or it will be lazily-evaluated later, which is wrong.
        # self.users_before = list(User.objects.values_list('id', flat=True).order_by('id'))
        # print(self.users_before)



    def TearDown(self):
        super(BaseLiveServerTestCase,self).tearDown()
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