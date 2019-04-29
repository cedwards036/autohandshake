import unittest

from autohandshake import HandshakeBrowser, UserType
from autohandshake.src.exceptions import InvalidURLError, WrongPageForMethodError, \
    InsufficientPermissionsError
from autohandshake.src.constants import BASE_URL
from autohandshake.tests import TestSession


class TestHandshakeBrowserMainFunctionality(unittest.TestCase):

    def test_throws_error_if_given_invalid_url(self):
        completely_wrong_url = "https://www.google.com/"
        invalid_url = "https://jhu.joinhandhake.com/"
        not_a_url = "hello world"
        no_https = "jhu.joinhandshake.com"

        with self.assertRaises(InvalidURLError):
            browser = HandshakeBrowser()
            browser.get(completely_wrong_url)
            browser.quit()

        with self.assertRaises(InvalidURLError):
            browser = HandshakeBrowser()
            browser.get(invalid_url)
            browser.quit()

        with self.assertRaises(InvalidURLError):
            browser = HandshakeBrowser()
            browser.get(not_a_url)
            browser.quit()

        with self.assertRaises(InvalidURLError):
            browser = HandshakeBrowser()
            browser.get(no_https)
            browser.quit()

    def test_throws_error_for_insufficient_permissions(self):
        with self.assertRaises(InsufficientPermissionsError):
            with TestSession() as browser:
                browser.get(f'{BASE_URL}/schools/{int(browser.school_id) - 1}/edit')

    def test_throws_error_for_invalid_url_while_logged_in(self):
        with self.assertRaises(InvalidURLError):
            with TestSession() as browser:
                browser.get(f'{BASE_URL}/schools/abcdefg/edit')

    def test_element_exists_by_xpath(self):
        # tests valid as of 4/8/19
        browser = HandshakeBrowser()
        browser.get(BASE_URL)

        self.assertTrue(browser.element_exists_by_xpath('//div'))
        self.assertTrue(browser.element_exists_by_xpath("//a/span[@class='select2-chosen']"))

        self.assertFalse(browser.element_exists_by_xpath("//div[@class='this_isnt_a_real_class']"))

        browser.quit()


class TestHandshakeBrowserUserTypes(unittest.TestCase):
    """
    This test suite assumes the testing user has all three account types available to switch to.
    Additionally, each test assumes that the user is starting logged in as a career services
    user.
    """

    def test_sets_user_type_to_correct_type_upon_login(self):
        with TestSession() as browser:
            self.assertEqual(UserType.STAFF, browser.user_type)

    def test_switch_user_type_on_valid_page(self):
        with TestSession() as browser:
            self.assertEqual(UserType.STAFF, browser.user_type)
            browser.switch_users(UserType.EMPLOYER)
            self.assertEqual(UserType.EMPLOYER, browser.user_type)
            browser.switch_users(UserType.STUDENT)
            self.assertEqual(UserType.STUDENT, browser.user_type)
            browser.switch_users(UserType.STAFF)
            self.assertEqual(UserType.STAFF, browser.user_type)

    def test_browser_registers_correct_user_type_on_login(self):
        with TestSession() as browser:
            self.assertEqual(UserType.STAFF, browser.user_type)
            browser.switch_users(UserType.EMPLOYER)
        with TestSession() as browser:
            self.assertEqual(UserType.EMPLOYER, browser.user_type)
            browser.switch_users(UserType.STUDENT)
        with TestSession() as browser:
            self.assertEqual(UserType.STUDENT, browser.user_type)
            browser.switch_users(UserType.STAFF)
            self.assertEqual(UserType.STAFF, browser.user_type)
