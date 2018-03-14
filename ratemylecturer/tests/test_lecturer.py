from ratemylecturer.tests.test_utils import BaseLiveServerTestCase


class LecturerTest(BaseLiveServerTestCase):

    def test_lecturer_can_link_to_existing_profile(self):
        self.driver.get('')

    def test_existing_lecturer_can_not_be_added(self):
        self.driver.get('')
