import unittest

from autohandshake.src.HandshakeSession import HandshakeSession


class TestHandshakeSession(unittest.TestCase):

    def test_throws_error_if_given_invalid_url(self):
        completely_wrong_url = "https://www.google.com/"
        invalid_url = "https://jhu.joinhandhake.com/"
        not_a_url = "hello world"
        no_https = "jhu.joinhandshake.com"
        misspelled_school_url = "https://jhuu.joinhandshake.com/login"

        with self.assertRaises(ValueError):
            HandshakeSession(login_url=completely_wrong_url)

        with self.assertRaises(ValueError):
            HandshakeSession(login_url=invalid_url)

        with self.assertRaises(ValueError):
            HandshakeSession(login_url=not_a_url)

        with self.assertRaises(ValueError):
            with HandshakeSession(login_url=misspelled_school_url):
                pass

        with self.assertRaises(ValueError):
            with HandshakeSession(login_url=no_https):
                pass

    def test_does_not_throw_error_given_valid_url(self):
        standard_url = "https://jhu.joinhandshake.com"
        login_url = "https://jhu.joinhandshake.com/login"

        try:
            with HandshakeSession(login_url=standard_url):
                pass
        except ValueError:
            self.fail("Unexpected ValueError given a valid normal URL")

        try:
            with HandshakeSession(login_url=login_url):
                pass
        except ValueError:
            self.fail("Unexpected ValueError given a valid login-style URL")
