import unittest
from autohandshake.src.Pages import LoginPage
from autohandshake import HandshakeBrowser
from autohandshake.src import InvalidURLError, InvalidEmailError, \
                              InvalidPasswordError

class TestLoginPage(unittest.TestCase):

    def test_throws_error_if_given_invalid_url(self):
        misspelled_school_url = "https://jhuu.joinhandshake.com/login"
        invalid_url = "https://jhu.joinhandhake.com/events"

        with self.assertRaises(InvalidURLError):
            login_page = LoginPage(misspelled_school_url, HandshakeBrowser())
        with self.assertRaises(InvalidURLError):
            login_page = LoginPage(invalid_url, HandshakeBrowser())

    def test_doesnt_throw_error_if_given_valid_url(self):
        valid_url = "https://jhu.joinhandshake.com"
        valid_url_with_login = "https://jhu.joinhandshake.com/login"

        try:
            login_page = LoginPage(valid_url, HandshakeBrowser())
        except:
            self.fail()

        try:
            login_page = LoginPage(valid_url_with_login, HandshakeBrowser())
        except:
            self.fail()

    # def test_login_works_with_valid_credentials(self):
    #     valid_url = "https://jhu.joinhandshake.com"
    #
    #     # only fill in temporarily for testing. Never commit the file with
    #     # valid email and password listed here
    #     email = ""
    #     password = ""
    #
    #     browser = HandshakeBrowser()
    #     login_page = LoginPage(valid_url, browser)
    #     login_page.login(email, password)
    #     browser.quit()

    def test_login_throws_exception_for_invalid_email(self):
        valid_url = "https://jhu.joinhandshake.com"
        email = "f@ke_email@jhu.edu"
        password = ""

        browser = HandshakeBrowser()
        login_page = LoginPage(valid_url, browser)
        with self.assertRaises(InvalidEmailError):
            login_page.login(email, password)
            browser.quit()

    def test_login_throws_exception_for_invalid_password(self):
        valid_url = "https://jhu.joinhandshake.com"
        email = "cedwar42@jhu.edu"
        password = "not a password"

        browser = HandshakeBrowser()
        login_page = LoginPage(valid_url, browser)
        with self.assertRaises(InvalidPasswordError):
            login_page.login(email, password)
            browser.quit()
