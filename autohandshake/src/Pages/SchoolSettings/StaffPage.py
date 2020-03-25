from autohandshake.src.Pages import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL
from typing import List
from bs4 import BeautifulSoup


class StaffPage(Page):

    def __init__(self, browser: HandshakeBrowser):
        """
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        majors_base_url = f'{BASE_URL}/schools/{browser.school_id}/manage_users'
        url_query = '?page=1&per_page=5000&sort_direction=desc&sort_column=default'
        super().__init__(majors_base_url + url_query,
                         browser)

    @Page.require_user_type(UserType.STAFF)
    def get_staff_names(self) -> List[dict]:
        """
        Get a list of names of all the school's active career center staff accounts.

        :return: a list full staff names of the form ['Mary Jeffries', 'John Cabot']
        :rtype: list
        """
        name_cards = BeautifulSoup(self._browser.get_element_attribute_by_xpath(
            '//div[@data-hook="search-results"]', 'innerHTML'),
            'html.parser').find_all('h2')
        return [card.find('a').text for card in name_cards]

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
        self._browser.wait_until_element_exists_by_xpath("//div[@data-hook='search-results']")
