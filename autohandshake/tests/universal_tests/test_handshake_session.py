import unittest

from autohandshake import HandshakeSession
from autohandshake.tests import email, password, homepage, school_id
from autohandshake.src.exceptions import InvalidPasswordError


class TestHandshakeSession(unittest.TestCase):

    def test_does_not_throw_error_given_valid_url(self):
        standard_url = homepage

        login_style_url = f"{homepage}/login"

        try:
            with HandshakeSession(login_url=standard_url, email=email, password=password):
                pass
        except ValueError:
            self.fail("Unexpected ValueError given a valid normal URL")

        try:
            with HandshakeSession(login_url=login_style_url, email=email, password=password):
                pass
        except ValueError:
            self.fail("Unexpected ValueError given a valid login-style URL")

    def test_sets_browser_school_id(self):
        try:
            with HandshakeSession(homepage, email, password) as browser:
                self.assertEqual(browser.school_id, school_id)
        except AttributeError:
            self.fail("School ID has not been set")

    def test_works_with_keyring_password(self):
        """This test requires a valid keyring password to be set up on the testing computer"""
        try:
            with HandshakeSession(homepage, email):
                pass
        except InvalidPasswordError:
            self.fail("Password did not work or was not found")

    def test_throws_error_if_keyring_cannot_find_password(self):
        """This test requires the testing computer to NOT have the specified service/user combination set"""
        with self.assertRaises(InvalidPasswordError):
            with HandshakeSession('https://abc.joinhandshake.com', 'notuser@abc.edu'):
                pass

    def test_custom_chromedriver_path(self):
        try:
            with HandshakeSession(homepage, email, chromedriver_path='./chromedriver.exe') as browser:
                pass
        except Exception as e:
            self.fail(e)
