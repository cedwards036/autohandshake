from autohandshake.src.Pages.Page import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.exceptions import NoSuchElementError
from autohandshake.src.file_download_utils import confirm_file_downloaded
from autohandshake.src.constants import BASE_URL
from datetime import datetime


class EventsPage(Page):
    """
    The main Events page in Handshake.
    """

    def __init__(self, browser: HandshakeBrowser):
        """
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(f'{BASE_URL}/events', browser)

    @Page.require_user_type(UserType.STAFF)
    def load_saved_search(self, saved_search_name: str):
        """
        Given the case-sensitive name of a saved search, apply that search.
        """
        saved_search_btn_xpath = '//a[@id="open-saved-searches"]'
        saved_search_xpath = f'//div[./h3/span[text()="{saved_search_name}"]]'
        self._browser.click_element_by_xpath(saved_search_btn_xpath)
        self._browser.wait_until_element_is_clickable_by_xpath('//ul[@id="saved-searches"]')
        try:
            self._browser.click_element_by_xpath(saved_search_xpath)
        except NoSuchElementError:
            raise ValueError(f'There is no saved search with the name "{saved_search_name}"')
        self._wait_until_page_is_loaded()

    @Page.require_user_type(UserType.STAFF)
    def download_event_data(self, download_dir: str, wait_time=300) -> str:
        """
        Download a CSV of the event data matching the page's current filters.

        :param download_dir: the directory into which the file will download
        :type download_dir: str
        :param wait_time: the maximum time to wait for the download to appear
        :type wait_time: int
        :return: the file path of the downloaded file
        :rtype: str
        """
        download_btn_xpath = '//a[contains(@class, "download-results")]'
        download_link_xpath = '//a[contains(text(), "Your download is ready")]'
        self._browser.wait_then_click_element_by_xpath(download_btn_xpath)
        self._browser.wait_then_click_element_by_xpath(download_link_xpath)
        filename_pattern = self._get_filename_pattern()
        return confirm_file_downloaded(download_dir, filename_pattern, wait_time)

    @staticmethod
    def _get_filename_pattern() -> str:
        """
        Get a regex string describing the form of the downloaded file.
        """
        return f'event_download{datetime.now().strftime("%Y%m%d")}*.csv'

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
        self._browser.wait_until_element_exists_by_xpath('//tbody[@data-bind="foreach: events"]')
