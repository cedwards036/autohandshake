import unittest

from autohandshake import HandshakeSession
from autohandshake.tests import email, password, homepage


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
