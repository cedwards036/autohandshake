import unittest
from autohandshake.src.Pages import InsightsPage
from autohandshake.tests import TestSession
from autohandshake.src.exceptions import InvalidURLError, NoSuchElementError


class TestInsightsPage(unittest.TestCase):

    def test_error_is_thrown_given_malformed_url(self):
        malformed_url = 'https://app.joinhandshake.com/anlytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls'
        malformed_query_param = 'fj4WQD2fhj$dsk2'
        with self.assertRaises(InvalidURLError):
            with TestSession() as browser:
                insights = InsightsPage(malformed_url, browser)
        with self.assertRaises(InvalidURLError):
            with TestSession() as browser:
                insights = InsightsPage(malformed_query_param, browser)

    def test_error_is_thrown_given_invalid_query_param(self):
        empty_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkfsgerh0QnUyV2JKTHhQMDZsdh4344yht1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls'
        with self.assertRaises(InvalidURLError):
            with TestSession() as browser:
                insights = InsightsPage(empty_query, browser)

        invalid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHdb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with self.assertRaises(InvalidURLError):
            with TestSession() as browser:
                insights = InsightsPage(invalid_query, browser)

        invalid_404_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuY3Rpb24vc3R1ZGVudHM_cWlkPXQ4NjBST1RqTFlYYVBUd3luaXVORG8mZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9cGlr'
        with self.assertRaises(InvalidURLError):
            with TestSession() as browser:
                insights = InsightsPage(invalid_404_query, browser)

    def test_error_is_thrown_when_selecting_download_file_type_outside_of_dialogue_box(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            with self.assertRaises(NoSuchElementError):
                insights.select_download_file_type('excel')

    def test_no_error_is_thrown_selecting_valid_download_file_type(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.open_download_dialogue()
            insights.select_download_file_type('txt')
            insights.select_download_file_type('csv')
            insights.select_download_file_type('json')
            insights.select_download_file_type('Tab-SeparaTED    ')
            insights.select_download_file_type('   HTML   ')
            insights.select_download_file_type('Markdown')
            insights.select_download_file_type('text')
            insights.select_download_file_type('Png')

    def test_set_limit_to_all_results(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.open_download_dialogue()
            insights.set_limit_to_all_results()
            self.assertTrue(browser.element_is_selected_by_xpath(
                "//input[@name='qr-export-modal-limit' and @value='all']"))
            insights.set_limit_to_all_results(True)
            self.assertTrue(browser.element_is_selected_by_xpath(
                "//input[@ng-model='queryDownloadController.runUnsorted']"))

    def test_set_custom_limit(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.open_download_dialogue()
            insights.set_custom_limit(357)
            self.assertTrue(browser.element_is_selected_by_xpath(
                "//input[@name='qr-export-modal-limit' and @value='custom']"))
            self.assertEqual(browser.get_element_attribute_by_xpath(
                "//input[@name='customExportLimit']", "value"), '357')

    def test_set_file_name(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.open_download_dialogue()
            insights.set_file_name('data_file.csv')
            self.assertEqual(browser.get_element_attribute_by_xpath(
                "//input[@name='customExportFilename']", "value"), 'data_file.csv')

    def test_set_file_name_throws_error_for_invalid_file_name(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.open_download_dialogue()
            with self.assertRaises(ValueError):
                insights.set_file_name('')
