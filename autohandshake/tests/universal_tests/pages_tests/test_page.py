import unittest

from autohandshake.src.Pages import Page
from autohandshake import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL
from autohandshake.tests import TestSession
from autohandshake.src.exceptions import InvalidUserTypeError


class TestPage(unittest.TestCase):

    def test_throws_error_when_required_methods_not_implemented(self):
        with self.assertRaises(TypeError):
            class SomePage(Page):
                pass

            some_page = SomePage(BASE_URL, HandshakeBrowser())

    def test_throws_error_when_method_called_with_incorrect_user_type(self):

        class TestPage(Page):

            def __init__(self, browser):
                super().__init__(BASE_URL, browser)

            @Page.require_user_type(UserType.STAFF)
            def staff_method(self):
                pass

            @Page.require_user_type(UserType.STUDENT)
            def student_method(self):
                pass

            @Page.require_user_type(UserType.EMPLOYER)
            def employer_method(self):
                pass

            def _validate_url(self, url):
                pass

            def _wait_until_page_is_loaded(self):
                pass

        with TestSession() as browser:
            self.assertEqual(UserType.STAFF, browser.user_type)
            test_page = TestPage(browser)
            with self.assertRaises(InvalidUserTypeError):
                test_page.student_method()
            with self.assertRaises(InvalidUserTypeError):
                test_page.employer_method()

            browser.switch_users(UserType.STUDENT)
            self.assertEqual(UserType.STUDENT, browser.user_type)

            with self.assertRaises(InvalidUserTypeError):
                test_page.employer_method()
            with self.assertRaises(InvalidUserTypeError):
                test_page.staff_method()
            try:
                test_page.student_method()
            except InvalidUserTypeError:
                browser.switch_users(UserType.STAFF)
                self.fail("Using an approved method still threw an error.")
            browser.switch_users(UserType.STAFF)
