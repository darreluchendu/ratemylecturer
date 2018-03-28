from ratemylecturer.tests.test_utils import BaseLiveServerTestCase


class StudentTest(BaseLiveServerTestCase):

    def test_student_can_add_lecturer(self):
        self.driver.get('')
