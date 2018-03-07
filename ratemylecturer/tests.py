from django.test import TestCase
from django.urls import reverse

from ratemylecturer.views import index

# Create your tests here.

class IndexViewTests(TestCase):

    def test_home_contains_required_links(self):
        response = self.client.get((reverse("index"))) # returns the home page
        self.assertContains(response,"about".lower())
        self.assertContains(response,"Sign In".lower())
        self.assertContains(response,"Register".lower())



    def test_display_lecturer_Of_the_week_image(self):
        """
        ensures that index page display image for lecturer of the
        week.
        """
        response = self.client.get((reverse("index")))
        self.assertContains(response, 'profile_image')
