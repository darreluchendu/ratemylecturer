from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ratemylecturer.tests.test_utils import BaseLiveServerTestCase


class LoginTests(BaseLiveServerTestCase):

    def test_can_login_via_facebook(self):
        self.driver.get("https://www.facebook.com/")
        facebookUsername = "ratemylecturerteam@gmail.com"
        facebookPassword = "ogun1033"

        self.driver.get(self.live_server_url + '/ratemylecturer/login/')
        facebook_button = self.driver.find_element_by_link_text('Login with Facebook')
        facebook_button.click()
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.title_contains('Facebook'))

        emailFieldID = "email"
        passFieldID = "pass"
        loginButtonXpath = "//input[@value='Log In']"
        facebookLogo = "/html/body/div/div[1]/div/div/div/div[1]/div/h1/a"

        emailFieldElement = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID))
        passFieldElement = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID))
        loginButtonElement = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_xpath(loginButtonXpath))

        emailFieldElement.clear()
        emailFieldElement.send_keys(facebookUsername)
        passFieldElement.clear()
        passFieldElement.send_keys(facebookPassword)
        loginButtonElement.click()
        WebDriverWait(self.driver, 20).until(lambda driver: self.driver.find_element_by_xpath(facebookLogo))

    def test_login_via_google(self):
        self.driver.get(self.live_server_url + '/ratemylecturer/login/')
        # find google button
        google_button = self.driver.find_element_by_link_text('Login with Google')
        google_button.click()
        wait = WebDriverWait(self.driver, 10)
