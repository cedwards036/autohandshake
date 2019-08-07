import unittest
from autohandshake import CareerInterestsPage, UserType
from autohandshake.tests import TestSession


class TestCareerInterestsPage(unittest.TestCase):
    TEST_STUDENT_ID = 8534543

    def test_something(self):
        with TestSession() as browser:
            browser.switch_users(UserType.STUDENT)
            page = CareerInterestsPage(self.TEST_STUDENT_ID, browser)
            self.fail("Must implement view-as-student first")
