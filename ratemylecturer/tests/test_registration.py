from django.urls import reverse
from ratemylecturer.tests.test_utils import BaseLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




class AccountRegistrationTestCase(BaseLiveServerTestCase):

    def test_student_registration(self):
        # open the lick we want to test.
        self.driver.get('http://127.0.0.1:8000/ratemylecturer/register/')

        #find the form element.
        student_radio = self.driver.find_element_by_id('student_radio')
        username = self.driver.find_element_by_id('id_username')
        email = self.driver.find_element_by_id('id_email')
        password = self.driver.find_element_by_id('id_password')
        first_name = self.driver.find_element_by_id('id_first_name')
        surname = self.driver.find_element_by_id('id_surname')
        uni = self.driver.find_element_by_id('id_university')
        course = self.driver.find_element_by_id('id_course')
        picture = self.driver.find_element_by_id('id_picture')
        bio = self.driver.find_element_by_id('id_bio')
        submit = self.driver.find_element_by_name('register')

        # fill in the form
        user_name = 'test_user8'
        student_radio.click()
        username.send_keys(user_name)
        email.send_keys('test8@gmail.com')
        password.send_keys('WycleffJean')
        first_name.send_keys('Yusuf')
        surname.send_keys('Ogunjobi')
        uni.send_keys('University of Glasgow')
        course.send_keys('Electronic and Software Engineering')
        #picture.send_keys('C:\Users\pace\Pictures\Screenshots\1')
        bio.send_keys('Prospective student')
        # submit form
        submit.click()
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.title_contains('Register'))
        body_text = self.driver.find_element_by_tag_name('body').text
        self.assertTrue('Thank you' in body_text)

    def test_lecturer_registration(self):
        self.driver.get()

    def test_registration_via_facebook(self):
        self.driver.get('')

    def test_registration_via_google(self):
        self.driver.get('')