from autohandshake.src.Pages import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser
from autohandshake.src.constants import BASE_URL
from bs4 import BeautifulSoup
from enum import Enum
from typing import List
from datetime import datetime
import math
import time
import re


class RequestStatus(Enum):
    """The possible access request statuses"""
    WAITING = 'Waiting'
    SUCCESSFUL = 'Successful'
    REJECTED = 'Rejected'
    FAILED = 'Failed'
    ALL = 'All'


class AccessRequestPage(Page):
    """The page on which users view and respond to Handshake access requests."""

    def __init__(self, browser: HandshakeBrowser):
        """
        Load the Handshake account access request page

        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(f'{BASE_URL}/email_actions', browser)

    def get_request_data(self, status: RequestStatus = RequestStatus.ALL) -> List[dict]:
        """
        Scrape access request data from the access request page for the specified request status.

        Data will be returned as a list of dicts of the form:

        {
            'user': [the requesting user's name],
            'user_id': [the requesting user's Handshake ID],
            'email': [the requesting user's email address],
            'request_date': [the date on which the request was submitted],
            'request': [the type of the request, either 'Student Access',
                        'Student Reactivation', or 'Mentor Access'],
            'status': [the request status, one of 'waiting', 'successful',
                       'rejected', or 'failed']
        }

        IMPORTANT: due to unknown limitations of Handshake's server, the request
        page appears to only be capable of loading up to around 1750 rows before
        crashing the website. To guard against this, this method will only pull
        the first 69 pages of results. If you have more than 1725 requests in any
        status, you will be unable to pull the entire dataset for that status.
        The method will only return the first 1725 rows.

        :param status: the status type of requests to pull. By default, pull data for all requests
        :type status: RequestStatus
        :return: a list of request data dicts
        :rtype: list
        """
        SEE_MORE_BTN_XPATH = "//a[text()='See More']"

        # filter page to only include requests of the given status
        self._browser.click_element_by_xpath(self._status_btn_xpath(status))
        self._browser.wait_until_element_is_clickable_by_xpath(
            "//*[@class='table manage-table']/tbody/tr[1]/td[1]")

        # load all requests of the given status onto the page
        total_requests = sum(map(int, self._browser.get_elements_attribute_by_xpath(
            "//div[@class='panel panel-default']//a/span[@class='badge' and text()!='0']", "text")))

        pages_to_load = int(math.floor(total_requests / 25))
        # account for apparent load limit on Handshake's servers
        if pages_to_load > 69:
            pages_to_load = 69
        for i in range(pages_to_load):  # click "See More" btn until all rows loaded
            print(i)
            self._browser.wait_until_element_exists_by_xpath(SEE_MORE_BTN_XPATH)
            self._browser.click_element_by_xpath(SEE_MORE_BTN_XPATH)

        time.sleep(2)  # wait for final set of names to finish loading before scraping

        # scrape request data from page
        request_data = []
        student_rows = BeautifulSoup(
            self._browser.get_element_attribute_by_xpath("//tbody", "innerHTML"),
            'html.parser').find_all('tr')
        for row in student_rows:
            user = row.find('td', {'class': 'requester_name'}).find('a').text
            user_id_link = row.find('td', {'class': 'requester_name'}).find('a')['href']
            user_id = re.findall(r'([0-9]+)', user_id_link)[0]
            date_str = row.find('td', {'class': 'request_date'}).find('a').text
            date_str = re.sub(r'(\d)(st|nd|rd|th)', r'\1', date_str)
            data_row = {
                'user': user,
                'user_id': user_id,
                'email': row.find('td', {'class': 'requester_email'}).find('a').text,
                'request_date': datetime.strptime(date_str, '%B %d %Y').date(),
                'request': row.find('td', {'class': 'request'}).find('a').text,
                'status': row.find('td', {'class': 'status'}).find('span').text
            }
            request_data.append(data_row)
        return request_data

    def validate_url(self, url):
        """
        Ensure that the given URL is a valid URL.

        Since the URL is not entered by the user, it is always valid.

        :param url: the url to validate
        :type url: str
        """
        return

    def wait_until_page_is_loaded(self):
        """Wait until the page has finished loading."""
        for status in RequestStatus:
            self._browser.wait_until_element_is_clickable_by_xpath(
                self._status_btn_xpath(status))

    @staticmethod
    def _status_btn_xpath(status: RequestStatus):
        """Get the xpath for the button to load request data for the given status"""
        return f'//div[@id="notifications-affix"]//a[./span[text()="{status.value}"]]'
