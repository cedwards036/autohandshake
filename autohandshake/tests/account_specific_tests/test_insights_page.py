import unittest
from autohandshake.src.Pages import InsightsPage, FileType
from autohandshake.tests import TestSession, download_dir
from autohandshake.src.exceptions import InvalidURLError, NoSuchElementError
import os
import json
from datetime import date, datetime


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

    def test_get_data(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX3NlcnZpY2Vfc3RhZmZzP3FpZD1oUGFSSldmQWpyQjFqcDYyd3FCaWh2JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            expected = [{'career_service_staffs.first_name': 'David',
                         'career_service_staffs.last_name': ' Le'},
                        {'career_service_staffs.first_name': 'Ella',
                         'career_service_staffs.last_name': 'Stern'},
                        {'career_service_staffs.first_name': 'Joy',
                         'career_service_staffs.last_name': 'Saunders'},
                        {'career_service_staffs.first_name': 'Ted',
                         'career_service_staffs.last_name': 'Shaprow'},
                        {'career_service_staffs.first_name': 'Troy',
                         'career_service_staffs.last_name': 'Parker: Technology & Innovation'}]
            actual = insights.get_data()
            actual.sort(key=lambda x: x['career_service_staffs.first_name'])
            self.assertEqual(expected, actual)

    def test_get_data_with_custom_limit(self):
        query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX3NlcnZpY2Vfc3RhZmZzP3FpZD1oUGFSSldmQWpyQjFqcDYyd3FCaWh2JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
        with TestSession() as browser:
            insights = InsightsPage(query, browser)
            expected = [{'career_service_staffs.first_name': 'David',
                         'career_service_staffs.last_name': ' Le'},
                        {'career_service_staffs.first_name': 'Ella',
                         'career_service_staffs.last_name': 'Stern'},
                        {'career_service_staffs.first_name': 'Joy',
                         'career_service_staffs.last_name': 'Saunders'}]
            actual = insights.get_data(limit=3)
            actual.sort(key=lambda x: x['career_service_staffs.first_name'])
            self.assertEqual(expected, actual)

    def test_download_file_works_with_valid_download_dir(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPWtmaHNhdzRvODh0QnFPY1FxQ1NCNzYmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        file_name = 'test_file_834898330.xlsx'
        expected_filepath = os.path.join(download_dir, file_name)
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            downloaded_filepath = insights.download_file(download_dir, file_name, FileType.EXCEL)
            self.assertEqual(expected_filepath, downloaded_filepath)
            self.assertTrue(os.path.exists(expected_filepath))
            os.remove(expected_filepath)

    def test_download_file_with_custom_limit(self):
        query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX3NlcnZpY2Vfc3RhZmZzP3FpZD1oUGFSSldmQWpyQjFqcDYyd3FCaWh2JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
        file_name = 'test_file_2589230.json'
        expected_filepath = os.path.join(download_dir, file_name)
        with TestSession() as browser:
            insights = InsightsPage(query, browser)
            downloaded_filepath = insights.download_file(download_dir, file_name, FileType.JSON, limit=3)
        expected = [{'career_service_staffs.first_name': 'David',
                     'career_service_staffs.last_name': ' Le'},
                    {'career_service_staffs.first_name': 'Ella',
                     'career_service_staffs.last_name': 'Stern'},
                    {'career_service_staffs.first_name': 'Joy',
                     'career_service_staffs.last_name': 'Saunders'}]
        self.assertTrue(os.path.exists(expected_filepath))
        with open(downloaded_filepath) as file:
            actual = json.load(file)
            actual.sort(key=lambda x: x['career_service_staffs.first_name'])
        self.assertEqual(expected, actual)
        os.remove(downloaded_filepath)

    def test_set_date_range_filter(self):
        def test_date_field(insights: InsightsPage, field: dict, new_start: date, new_end: date):
            """Helper function to test a given date field"""
            self.assertEqual(field['old_start_date'],
                             insights._browser.get_element_attribute_by_xpath(field['start_xpath'], 'value'))
            self.assertEqual(field['old_end_date'],
                             insights._browser.get_element_attribute_by_xpath(field['end_xpath'], 'value'))
            insights.set_date_range_filter(field['category'], field['title'], new_start, new_end)
            self.assertEqual(new_start.strftime('%Y-%m-%d'),
                             insights._browser.get_element_attribute_by_xpath(field['start_xpath'], 'value'))
            self.assertEqual(new_end.strftime('%Y-%m-%d'),
                             insights._browser.get_element_attribute_by_xpath(field['end_xpath'], 'value'))

        jobs_insights = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vam9icz9xaWQ9UVJ3OVZRR2xORHVnYnVQZWJtYVI3diZlbWJlZF9kb21haW49aHR0cHM6JTJGJTJGYXBwLmpvaW5oYW5kc2hha2UuY29tJnRvZ2dsZT1maWw='
        field1 = {'category': 'Postings', 'title': 'Created At Date',
                  'old_start_date': '2007-05-09', 'old_end_date': '2014-05-07',
                  'start_xpath': '//*[@id="lk-embed-container"]/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[2]/td[3]/lk-filter/table/tbody/tr/td[2]/span[2]/span[1]/input',
                  'end_xpath': '//*[@id="lk-embed-container"]/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[2]/td[3]/lk-filter/table/tbody/tr/td[2]/span[3]/span/input'}

        field2 = {'category': 'Postings', 'title': 'Expiration Date Date',
                  'old_start_date': '2016-03-28', 'old_end_date': '2017-08-28',
                  'start_xpath': '//*[@id="lk-embed-container"]/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[3]/td[3]/lk-filter/table/tbody/tr/td[2]/span[2]/span[1]/input',
                  'end_xpath': '//*[@id="lk-embed-container"]/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[3]/td[3]/lk-filter/table/tbody/tr/td[2]/span[3]/span/input'}

        field3 = {'category': 'Jobs', 'title': 'Start Date Date',
                  'old_start_date': '2019-04-02', 'old_end_date': '2019-04-16',
                  'start_xpath': '//*[@id="lk-embed-container"]/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[1]/td[3]/lk-filter/table/tbody/tr/td[2]/span[2]/span[1]/input',
                  'end_xpath': '//*[@id="lk-embed-container"]/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[1]/td[3]/lk-filter/table/tbody/tr/td[2]/span[3]/span/input'}
        with TestSession() as browser:
            insights = InsightsPage(jobs_insights, browser)
            test_date_field(insights, field1, datetime.strptime('10/31/2017', '%m/%d/%Y').date(),
                            datetime.strptime('12/03/2017', '%m/%d/%Y').date())
            test_date_field(insights, field2, datetime.strptime('12/02/2008', '%m/%d/%Y').date(),
                            datetime.strptime('05/04/2019', '%m/%d/%Y').date())
            test_date_field(insights, field3, datetime.strptime('01/02/2013', '%m/%d/%Y').date(),
                            datetime.strptime('02/03/2014', '%m/%d/%Y').date())


class TestInsightsPageDownloadModal(unittest.TestCase):

    def test_error_is_thrown_when_selecting_download_file_type_outside_of_dialogue_box(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            with self.assertRaises(NoSuchElementError):
                insights.modal.set_download_file_type('excel')

    def test_no_error_is_thrown_selecting_valid_download_file_type(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            insights.modal.set_download_file_type(FileType.TXT)
            self.assertEqual(FileType.TXT, insights.modal.get_download_file_type())
            insights.modal.set_download_file_type(FileType.CSV)
            self.assertEqual(FileType.CSV, insights.modal.get_download_file_type())
            insights.modal.set_download_file_type(FileType.JSON)
            self.assertEqual(FileType.JSON, insights.modal.get_download_file_type())
            insights.modal.set_download_file_type(FileType.HTML)
            self.assertEqual(FileType.HTML, insights.modal.get_download_file_type())
            insights.modal.set_download_file_type(FileType.MARKDOWN)
            self.assertEqual(FileType.MARKDOWN, insights.modal.get_download_file_type())
            insights.modal.set_download_file_type(FileType.PNG)
            self.assertEqual(FileType.PNG, insights.modal.get_download_file_type())

    def test_set_limit_to_all_results(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            insights.modal.set_limit_to_all_results()
            self.assertTrue(browser.element_is_selected_by_xpath(
                "//input[@name='qr-export-modal-limit' and @value='all']"))
            insights.modal.set_limit_to_all_results(True)
            self.assertTrue(browser.element_is_selected_by_xpath(
                "//input[@ng-model='queryDownloadController.runUnsorted']"))

    def test_set_custom_limit(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession(60) as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            insights.modal.set_custom_limit(357)
            self.assertTrue(browser.element_is_selected_by_xpath(
                "//input[@name='qr-export-modal-limit' and @value='custom']"))
            self.assertEqual(browser.get_element_attribute_by_xpath(
                "//input[@name='customExportLimit']", "value"), '357')

    def test_set_file_name(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            insights.modal.set_file_name('data_file.csv')
            self.assertEqual(browser.get_element_attribute_by_xpath(
                "//input[@name='customExportFilename']", "value"), 'data_file.csv')

            insights.modal.set_file_name('wrong_extension.json')
            self.assertEqual(browser.get_element_attribute_by_xpath(
                "//input[@name='customExportFilename']", "value"), 'wrong_extension.json.csv')

    def test_set_file_name_throws_error_for_invalid_file_name(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPXRoRnM0QnUyV2JKTHhQMDZ1dUpBT0QmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            with self.assertRaises(ValueError):
                insights.modal.set_file_name('')

    def test_download_file_works_with_valid_download_dir(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPWtmaHNhdzRvODh0QnFPY1FxQ1NCNzYmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        file_name = 'test_file_123456789.csv'
        file_path = download_dir + file_name
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            insights.modal.set_file_name(file_name)
            self.assertEqual(file_path, insights.modal.click_download_button(download_dir))
            self.assertTrue(os.path.exists(file_path))
            os.remove(file_path)

    def test_download_file_throws_error_with_invalid_download_dir(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPWtmaHNhdzRvODh0QnFPY1FxQ1NCNzYmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9ZmlsLHBpaw=='
        file_name = 'test_file_123456789.csv'
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            insights.modal.set_file_name(file_name)
            with self.assertRaises(RuntimeError):
                insights.modal.click_download_button('a/fake/download/dir/', 10)

    def test_open_in_browser_with_valid_file_type(self):
        expected = [
            {
                'career_service_staffs.first_name': "David",
                'career_service_staffs.last_name': " Le"
            },
            {
                'career_service_staffs.first_name': "Ella",
                'career_service_staffs.last_name': "Stern"
            },
            {
                'career_service_staffs.first_name': "Joy",
                'career_service_staffs.last_name': "Saunders"
            },
            {
                'career_service_staffs.first_name': "Ted",
                'career_service_staffs.last_name': "Shaprow"
            },
            {
                'career_service_staffs.first_name': "Troy",
                'career_service_staffs.last_name': "Parker"
            }
        ]
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX3NlcnZpY2Vfc3RhZmZzP3FpZD1oUGFSSldmQWpyQjFqcDYyd3FCaWh2JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            insights.modal.set_download_file_type(FileType.JSON)
            json_data = insights.modal.click_open_in_browser()
            self.assertEqual(expected.sort(key=lambda x: x['career_service_staffs.first_name']),
                             json_data.sort(key=lambda x: x['career_service_staffs.first_name']))

    def test_open_in_browser_throws_error_if_not_json(self):
        valid_query = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX3NlcnZpY2Vfc3RhZmZzP3FpZD1oUGFSSldmQWpyQjFqcDYyd3FCaWh2JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
        with TestSession() as browser:
            insights = InsightsPage(valid_query, browser)
            insights.modal.open()
            insights.modal.set_download_file_type(FileType.EXCEL)
            with self.assertRaises(RuntimeError):
                insights.modal.click_open_in_browser()
