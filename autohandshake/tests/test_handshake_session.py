import unittest

from autohandshake import HandshakeSession


class TestHandshakeSession(unittest.TestCase):
    """
    These tests only work with the author's school and login info. I have not
    figured out a way to generalize tests for this class.
    """

    def test_does_not_throw_error_given_valid_url(self):
        standard_url = "https://jhu.joinhandshake.com"

        login_style_url = "https://jhu.joinhandshake.com/login"

        try:
            with HandshakeSession(login_url=standard_url, email="", password=""):
                pass
        except ValueError:
            self.fail("Unexpected ValueError given a valid normal URL")

        try:
            with HandshakeSession(login_url=login_style_url, email="", password=""):
                pass
        except ValueError:
            self.fail("Unexpected ValueError given a valid login-style URL")


    # def test_session_logs_in_successfully_given_valid_credentials(self):
    #     """This test is for temporary spot-checking only. Never commit the file
    #     with saved valid login info listed here.
    #     """
    #     valid_url = "https://jhu.joinhandshake.com"
    #     valid_email = ""
    #     valid_password = ""
    #
    #     with HandshakeSession(valid_url, valid_email, valid_password) as browser:
    #         pass