import unittest
from autohandshake.src.Pages import InsightsPage
from autohandshake.tests import TestSession
from autohandshake.src.exceptions import InvalidURLError


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
