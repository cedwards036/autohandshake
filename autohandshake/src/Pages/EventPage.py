from typing import List

from bs4 import BeautifulSoup

from autohandshake.src.Pages.Page import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL


class EventPage(Page):
    """
    A specific Event page in Handshake.
    """

    def __init__(self, event_id: int, browser: HandshakeBrowser):
        """
        :param event_id: the id of the event page to visit
        :type event_id: int
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(f'{BASE_URL}/events/{event_id}', browser)

    @Page.require_user_type(UserType.STAFF)
    def get_invited_schools(self) -> List[str]:
        """
        Get a list of the names of schools invited to the event
        """
        school_elements = BeautifulSoup(self._browser.get_element_attribute_by_xpath(
            '//div[h4[text()="Invited Schools"]]', 'innerHTML'),
            'html.parser').find_all('img')
        return [school.get('title') for school in school_elements]

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
        self._browser.wait_until_element_exists_by_xpath('//div[@class="row attendees-lists"]')
