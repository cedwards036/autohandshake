import unittest
from autohandshake import CareerInterestsPage, ViewAsStudent
from autohandshake.tests import TestSession
from autohandshake.src.constants import BASE_URL
from autohandshake.src.exceptions import InsufficientPermissionsError

TEST_STUDENT_ID = 20474668


class TestCareerInterestsPage(unittest.TestCase):

    def test_page_loads_correctly(self):
        with TestSession() as browser:
            try:
                page = CareerInterestsPage(TEST_STUDENT_ID, browser)
                self.fail("Did not throw permissions error when logged in as staff")
            except InsufficientPermissionsError:
                pass  # it should throw an error if not logged in as a student
            with ViewAsStudent(TEST_STUDENT_ID, browser):
                page = CareerInterestsPage(TEST_STUDENT_ID, browser)

    def test_selects_clusters_and_saves_correctly(self):
        with TestSession() as browser:
            with ViewAsStudent(TEST_STUDENT_ID, browser):
                page = CareerInterestsPage(TEST_STUDENT_ID, browser)
                finance_selected = False
                health_selected = False
                if page.cluster_is_selected_by_id(200):
                    finance_selected = True
                    page.deselect_cluster_by_id(200)
                if page.cluster_is_selected_by_id(201):
                    health_selected = True
                    page.deselect_cluster_by_name("Homewood: Health Sciences")

                self.assertFalse(page.cluster_is_selected_by_id(200))
                self.assertFalse(page.cluster_is_selected_by_id(201))

                page.select_cluster_by_id(200)  # Homewood: Finance
                page.select_cluster_by_name('Homewood: Health Sciences')  # id: 201

                self.assertTrue(page.cluster_is_selected_by_id(201))
                self.assertTrue(page.cluster_is_selected_by_name('Homewood: Finance'))

                # make sure "select" only clicks when the cluster isn't already selected
                page.select_cluster_by_id(200)
                self.assertTrue(page.cluster_is_selected_by_name('Homewood: Finance'))

                page.save_interests()

                # navigate away and back again to make sure it saved
                browser.get(BASE_URL)

                page = CareerInterestsPage(TEST_STUDENT_ID, browser)
                self.assertTrue(page.cluster_is_selected_by_id(200))
                self.assertTrue(page.cluster_is_selected_by_name('Homewood: Health Sciences'))

                # clean up the career interests so they are the way we found them
                if not finance_selected:
                    page.deselect_cluster_by_id(200)
                if not health_selected:
                    page.deselect_cluster_by_id(201)

                page.save_interests()
