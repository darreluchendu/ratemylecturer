from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ratemylecturer.tests.test_utils import BaseLiveServerTestCase


class LoginTests(BaseLiveServerTestCase):

    def test_can_login_via_facebook(self):
        self.driver.get("https://www.facebook.com/")
        facebookUsername = "pokbxblnjj_1522226896@tfbnw.net"
        facebookPassword = "testpassword"

        self.driver.get('http://127.0.0.1:8000/' + 'ratemylecturer/login/')
        facebook_button = self.driver.find_element_by_link_text('Login with Facebook')
        facebook_button.click()
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.title_contains('Facebook'))

        emailFieldID = "email"
        passFieldID = "pass"
        loginButtonID = "loginbutton"

        emailFieldElement = wait.until(lambda driver: driver.find_element_by_id(emailFieldID))
        passFieldElement = wait.until(lambda driver: driver.find_element_by_id(passFieldID))
        loginButtonElement = wait.until(
            lambda driver: self.driver.find_element_by_id(loginButtonID))

        emailFieldElement.clear()
        emailFieldElement.send_keys(facebookUsername)
        passFieldElement.clear()
        passFieldElement.send_keys(facebookPassword)
        loginButtonElement.click()
        wait.until(EC.title_contains('Facebook'))
        self.assertIn('susan', self.driver.find_element_by_tag_name('body').text)

    def test_login_via_google(self):
        self.driver.get('http://127.0.0.1:8000/' + 'ratemylecturer/login/')
        # find google button
        google_button = self.driver.find_element_by_link_text('Login with Google')
        google_button.click()
        wait = WebDriverWait(self.driver, 10)
