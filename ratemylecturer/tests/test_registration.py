from django.urls import reverse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ratemylecturer import forms
from ratemylecturer.models import LecturerProfile
from ratemylecturer.tests.test_utils import BaseLiveServerTestCase, BaseRegistrationTestCase


class AccountRegistrationTest(BaseLiveServerTestCase):

    def test_student_can_register(self):
        # open the link we want to test.
        self.driver.get(self.live_server_url + '/ratemylecturer/register/')

        # find the form element.
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
        user_name = 'test_student'
        student_radio.click()
        username.send_keys(user_name)
        email.send_keys('test@gla.ac.uk')
        password.send_keys('WycleffJean')
        first_name.send_keys('Yusuf')
        surname.send_keys('Ogunjobi')
        uni.send_keys('University of Glasgow')
        course.send_keys('Electronic and Software Engineering')
        # picture.send_keys('C:\Users\pace\Pictures\Screenshots\1')
        bio.send_keys('Prospective student')
        # submit form
        submit.click()
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.title_contains('Register'))
        self.assertIn('Thank you for registering', self.driver.find_element_by_tag_name('body').text)
        # body_text = self.driver.find_element_by_tag_name('body').text
        # self.assertTrue('Thank you' in body_text)

    def test_lecturer_can_register(self):
        self.driver.get(self.live_server_url + '/ratemylecturer/register/')

        # find the form element.
        lecturer_radio = self.driver.find_element_by_id('lecturer_radio')
        username = self.driver.find_element_by_id('id_username')
        email = self.driver.find_element_by_id('id_email')
        password = self.driver.find_element_by_id('id_password')
        name = self.driver.find_element_by_id('lectuer_name')
        uni = self.driver.find_element_by_id('lecturer_uni')
        department = self.driver.find_element_by_id('lecturer_depart')
        picture = self.driver.find_element_by_id('id_picture')
        bio = self.driver.find_element_by_id('id_bio')
        submit = self.driver.find_element_by_name('register')

        # fill in the form
        user_name = 'test_student'
        lecturer_radio.click()
        username.send_keys(user_name)
        email.send_keys('test@gla.ac.uk')
        password.send_keys('WycleffJean')
        name.send_keys('Yusuf')
        uni.send_keys('University of Glasgow')
        department.send_keys('Electronic and Software Engineering')
        # picture.send_keys('C:\Users\pace\Pictures\Screenshots\1')
        bio.send_keys('Award winning lecturer')
        # submit form
        submit.click()
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.title_contains('Register'))
        self.assertIn('Thank you for registering', self.driver.find_element_by_tag_name('body').text)


class RegistrationModelTestCase(BaseRegistrationTestCase):
    """
    Tests for the model-oriented functionality of django-registration,
    including ``RegistrationProfile`` and its custom manager.

    """

    def test_lecturer_profile_created(self):
        """
        Test that a ``RegistrationProfile`` is created for a new user.

        """
        self.assertEqual(LecturerProfile.objects.count(), 1, 'Number of registered lecturers should be one ')


class RegistrationFormTest(BaseRegistrationTestCase):
    """
    Tests for the forms and custom validation logic included in
    forms.
    """

    def test_registration_form(self):
        """
        Test that ``RegistrationForm`` enforces username constraints
        and matching passwords.
        """
        invalid_data_dicts = [
            # Non-alphanumeric username.
            {
                'data':
                    {'username': 'foo/bar',
                     'email': 'foo@gla.ac.uk',
                     'password1': 'foo'},
                'error':
                    ('username', [u"Enter a valid value."])
            },
            # Already-existing username.
            {
                'data':
                    {'username': 'bob',
                     'email': 'bob@example.gla.ac.uk',
                     'password1': 'secret'},
                'error':
                    ('username', [u"This username is already taken. Please choose another."])
            },
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.UserForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]], invalid_dict['error'][1])
        form = forms.UserForm(data={'username': 'foo', 'email': 'foo@example.ac.uk', 'password1': 'foo'})
        self.failUnless(form.is_valid())

        def test_registration_form_unique_email(self):
            form = forms.UserForm(data={'username': 'foo', 'email': 'alice@example.ac.uk', 'password1': 'foo'})
            self.failIf(form.is_valid())
            self.assertEqual(form.errors['email'],
                             [u"This email address is already in use. Please supply a different email address."])

            form = forms.RegistrationFormUniqueEmail(
                data={'username': 'foo', 'email': 'foo@example.ac.uk', 'password1': 'foo'})
            self.failUnless(form.is_valid())


class RegistrationViewUnitTests(BaseRegistrationTestCase):
    """
    Tests for the views included in django-registration.

    """

    def test_registration_view(self):
        """
        Test that the registration view rejects invalid submissions,
        and creates a new user and redirects after a valid submission.

        """
        # Invalid data fails.
        response = self.client.post(reverse('register'), data={'username': 'alice',  # Will fail on username uniqueness.
                                                               'email': 'foo@example.ac.uk',
                                                               'password1': 'foo'})
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['user_form_student'])
        self.failUnless(response.context['user_form_student'].errors)

        response = self.client.post(reverse('register'),
                                    data={'username': 'foo',
                                          'email': 'foo@example.ac.uk',
                                          'password1': 'foo',
                                          })
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['Location'], 'http://testserver%s' % reverse('registration_complete'))
        self.assertEqual(LecturerProfile.objects.count(), 3)
