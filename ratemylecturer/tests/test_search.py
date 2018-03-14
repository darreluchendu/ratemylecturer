from ratemylecturer.tests.test_utils import BaseLiveServerTestCase


class SearchTest(BaseLiveServerTestCase):

    def test_search_a_given_lecturer(self):
        self.driver.get()