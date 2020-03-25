import unittest
from autohandshake.src.Pages import StaffPage
from autohandshake.tests import TestSession


class TestStaffPage(unittest.TestCase):

    def test(self):
        with TestSession() as browser:
            staff_page = StaffPage(browser)
            names = staff_page.get_staff_names()
            self.assertEqual('Abby Jackson', names[0])
            self.assertEqual('Alayna Hayes', names[3])
