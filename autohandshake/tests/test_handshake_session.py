import unittest

from autohandshake.src.HandshakeSession import HandshakeSession
from autohandshake.src.Pages.Page import Page
from autohandshake.src.exceptions import InvalidURLError


class TestHandshakeSession(unittest.TestCase):

    valid_url = "https://jhu.joinhandshake.com"

    def test_throws_error_if_given_invalid_url(self):
        completely_wrong_url = "https://www.google.com/"
        invalid_url = "https://jhu.joinhandhake.com/"
        not_a_url = "hello world"
        no_https = "jhu.joinhandshake.com"
        misspelled_school_url = "https://jhuu.joinhandshake.com/login"
        login_style_url = "https://jhu.joinhandshake.com/login"

        with self.assertRaises(InvalidURLError):
            HandshakeSession(home_url=completely_wrong_url)

        with self.assertRaises(InvalidURLError):
            HandshakeSession(home_url=invalid_url)

        with self.assertRaises(InvalidURLError):
            HandshakeSession(home_url=not_a_url)

        with self.assertRaises(InvalidURLError):
            with HandshakeSession(home_url=misspelled_school_url):
                pass

        with self.assertRaises(InvalidURLError):
            with HandshakeSession(home_url=no_https):
                pass

        with self.assertRaises(InvalidURLError):
            with HandshakeSession(home_url=login_style_url):
                pass

    def test_does_not_throw_error_given_valid_url(self):
        standard_url = "https://jhu.joinhandshake.com"

        slash_url = "https://jhu.joinhandshake.com/"

        try:
            with HandshakeSession(home_url=standard_url):
                pass
        except ValueError:
            self.fail("Unexpected ValueError given a valid normal URL")

        try:
            with HandshakeSession(home_url=slash_url):
                pass
        except ValueError:
            self.fail("Unexpected ValueError given a valid login-style URL")

    def test_load_throws_error_given_invalid_page(self):

        with self.assertRaises(ValueError):
            with HandshakeSession(home_url=self.valid_url) as hs:
                hs.load(32153)

        with self.assertRaises(ValueError):
            with HandshakeSession(home_url=self.valid_url) as hs:
                hs.load("not a page")

    def test_load_does_not_throw_error_given_valid_page(self):

        class ValidPage(Page):

            def __init__(self):
                super().__init__("a url")

            def page_is_loaded(self, browser):
                pass

        try:
            with HandshakeSession(home_url=self.valid_url) as hs:
                hs.load(ValidPage())
        except:
            self.fail("Unexpected Error given a valid page")