import unittest
from autohandshake.src.Pages import LoginPage
from autohandshake.tests import email, password, homepage
from autohandshake import HandshakeBrowser
from autohandshake.src import InvalidURLError, InvalidEmailError, \
                              InvalidPasswordError

class TestLoginPage(unittest.TestCase):

    def test_throws_error_if_given_invalid_url(self):
        misspelled_school_url = "https://jhuu.joinhandshake.com/login"
        invalid_url = f"{homepage}/events"

        with self.assertRaises(InvalidURLError):
            login_page = LoginPage(misspelled_school_url, HandshakeBrowser())
        with self.assertRaises(InvalidURLError):
            login_page = LoginPage(invalid_url, HandshakeBrowser())

    def test_doesnt_throw_error_if_given_valid_url(self):
        valid_url = homepage
        valid_url_with_login = f"{homepage}/login"

        try:
            login_page = LoginPage(valid_url, HandshakeBrowser())
        except:
            self.fail()

        try:
            login_page = LoginPage(valid_url_with_login, HandshakeBrowser())
        except:
            self.fail()

    def test_login_works_with_valid_credentials(self):
        browser = HandshakeBrowser()
        login_page = LoginPage(homepage, browser)
        login_page.login(email, password)
        browser.quit()

    def test_login_throws_exception_for_invalid_email(self):
        fake_email = "f@ke_email@jhu.edu"
        fake_pw = ""

        browser = HandshakeBrowser()
        login_page = LoginPage(homepage, browser)
        with self.assertRaises(InvalidEmailError):
            login_page.login(fake_email, fake_pw)
            browser.quit()

    def test_login_throws_exception_for_invalid_password(self):
        fake_pw = "not a password"

        browser = HandshakeBrowser()
        login_page = LoginPage(homepage, browser)
        with self.assertRaises(InvalidPasswordError):
            login_page.login(email, fake_pw)
            browser.quit()
