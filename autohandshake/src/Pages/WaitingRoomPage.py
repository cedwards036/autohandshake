from autohandshake.src.Pages.Page import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL
from autohandshake.src.exceptions import NoSuchElementError
from typing import List
from bs4 import BeautifulSoup
from dateutil import parser


class WaitingRoomPage(Page):
    """
    The Handshake appointment waiting room page.

    All office location filters are automatically cleared upon loading the page.
    """

    def __init__(self, browser: HandshakeBrowser):
        """
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(f'{BASE_URL}/checkins/waiting_room', browser)
        self._clear_office_locations_filter()

    @Page.require_user_type(UserType.STAFF)
    def get_checkin_data(self) -> List[dict]:
        """
        Get student checkin data from the waiting room.

        Data is returned in the format:
        ::

            [
                {
                    'being_created': True,
                    'student_id': 2284230,
                    'student_name': 'John Ferguson',
                    'datetime': datetime.datetime(2018, 10, 31, 14, 33),
                    'office_location': 'Rogers Hall Room 302'
                },
                {
                    'being_created': False,
                    'student_id': 6574835,
                    'student_name': 'Alyssa Fernandez',
                    'datetime': datetime.datetime(2018, 11, 3, 9, 50),
                    'office_location': None
                }
            ]

        :return: a list of student checkin data dicts
        """
        check_ins = BeautifulSoup(self._browser.get_element_attribute_by_xpath(
            '//div[@data-bind="foreach: drop_ins"]', 'innerHTML'),
            'html.parser').find_all('div', recursive=False)
        return self._parse_checkins(check_ins)

    def _parse_checkins(self, checkins: List[BeautifulSoup]) -> List[dict]:
        result = []
        for checkin in checkins:
            result.append(self._parse_checkin(checkin))
        return result

    @staticmethod
    def _parse_checkin(checkin: BeautifulSoup) -> dict:
        result = {
            'being_created': checkin.find('a', {'class': 'btn'}).text == 'Being Created',
            'student_id': int(checkin.h3.a['href'][7:]),
            'student_name': checkin.h3.a.text,
            'datetime': parser.parse(checkin.h4.text[12:]),
            'office_location': checkin.select('h4:nth-of-type(2)')[0].text[17:]
        }
        if result['office_location'] == 'null':
            result['office_location'] = None
        return result

    @Page.require_user_type(UserType.STAFF)
    def _clear_office_locations_filter(self):
        """
        Clear any office location default search filters.
        """
        office_location_dropdown_xpath = '//li[@data-hook="office_locations-dropdown"]//a'
        all_options_btn_xpath = '//li[@data-hook="office_locations-dropdown"]//div[text()="All Options"]'
        modal_xpath = '//div[@id="filter-modal"]'
        done_btn_xpath = '//button[text()="Done"]'

        self._browser.click_element_by_xpath(office_location_dropdown_xpath)
        self._browser.click_element_by_xpath(all_options_btn_xpath)
        self._browser.wait_until_element_is_clickable_by_xpath(modal_xpath)
        self._uncheck_all_office_locations()
        self._browser.click_element_by_xpath(done_btn_xpath)
        self._browser.wait_until_element_does_not_exist_by_xpath(modal_xpath)

    def _uncheck_all_office_locations(self):
        i = 1
        while True:
            try:
                checkbox_xpath = f'//div[@class="not-selected"]/div[{i}]/input'
                office_location_xpath = f'//div[@class="not-selected"]/div[{i}]'
                if self._browser.element_is_selected_by_xpath(checkbox_xpath):
                    office_location = self._browser.get_element_attribute_by_xpath(
                        office_location_xpath, 'text')
                    self._browser.click_element_by_xpath(office_location_xpath)
                    self._wait_until_filter_is_removed(office_location)
                i += 1
            except NoSuchElementError:
                break

    def _wait_until_filter_is_removed(self, office_location):
        office_location_filter_card_xpath = self._get_filter_card_xpath(office_location)
        self._browser.wait_until_element_does_not_exist_by_xpath(office_location_filter_card_xpath)

    def _get_filter_card_xpath(self, office_location):
        return f'//div[@class="selected_filters"]//a[text()="{office_location}"]'

    def _validate_url(self, url):
        """
        Ensure that the given URL is a valid URL.

        Since the URL is not entered by the user, it is always valid.

        :param url: the url to validate
        :type url: str
        """
        return

    def _wait_until_page_is_loaded(self):
        """Wait until the page has finished loading."""
        self._browser.wait_until_element_exists_by_xpath('//div[@class="panel-title center"]/h4')
