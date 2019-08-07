import unittest

from autohandshake import UserType, ViewAsStudent
from autohandshake.tests import TestSession
from autohandshake.src.constants import BASE_URL

TEST_USER_ID = 8534543  # my old fake student account


class TestViewAsStudent(unittest.TestCase):

    def test_view_as_student_changes_user_type_correctly(self):
        with TestSession() as browser:
            self.assertEqual(UserType.STAFF, browser.user_type)
            with ViewAsStudent(TEST_USER_ID, browser):
                self.assertEqual(UserType.STUDENT, browser.user_type)
                self.assertEqual(f'{BASE_URL}/users/{TEST_USER_ID}', browser.current_url)
            self.assertEqual(UserType.STAFF, browser.user_type)
