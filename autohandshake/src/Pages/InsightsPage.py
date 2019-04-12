from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL
from autohandshake.src.HandshakeBrowser import HandshakeBrowser
from autohandshake.src.exceptions import InvalidURLError
import re


class InsightsPage(Page):
    """The overview settings page listing all appointment types"""

    def __init__(self, url_string: str, browser: HandshakeBrowser):
        """
        Load the insights page specified by either the full URL or the query string

        :param url_string: either a full insights URL or just the alphanumeric
                           query string specifying the exact report
        :type url_string: str
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(url_string, browser)
        if self._browser.element_exists_by_xpath(
                "//span[text()='Select some dimensions or measures.' and @aria-hidden='false']"):
            raise InvalidURLError('Insights URL has no dimensions or measures selected')

    def open_download_dialogue(self):
        self._browser.click_element_by_xpath("//i[@class='lk-icon-gear']")
        self._browser.click_element_by_xpath("//a[@ng-click='openDownloadDialog()']")
        self._browser.wait_until_element_exists_by_xpath("//div[contains(@class, 'query-download-modal-limit')]")

    def validate_url(self, url):
        """
        Ensure that url string given is either a valid Insights URL or a valid
        Insights query string.

        :param url: the url to validate
        :type url: str
        """
        try:  # try full URL match
            re.match(fr'^{BASE_URL}/analytics/explore_embed\?insights_page=[a-zA-Z0-9_]+(==)?$', url) \
                .group(0)
        except AttributeError:
            try:  # try query parameter match
                re.match(r'^[a-zA-Z0-9_]+(==)?$', url) \
                    .group(0)
            except AttributeError:
                raise InvalidURLError()

    def wait_until_page_is_loaded(self):
        """Wait until the page has finished loading."""
        self._switch_to_looker_iframe()

    def _switch_to_looker_iframe(self):
        """Bring the Looker iframe into focus on the insights page"""
        exists_once_iframe_in_focus = "//i[@class='lk-icon-gear']"
        if not self._browser.element_exists_by_xpath(exists_once_iframe_in_focus):
            if self._browser.element_exists_by_xpath("//div[@style='display: none']"):
                raise InvalidURLError("Insights query string is malformed")

            iframe_xpath = "//iframe[@id='insights-iframe']"
            self._browser.wait_until_element_exists_by_xpath(iframe_xpath)
            self._browser.switch_to_frame_by_xpath(iframe_xpath)

            if self._browser.element_exists_by_xpath("//div[@class='error-http-status-code']"):
                raise InvalidURLError("Insights query string is malformed")

            self._browser.wait_until_element_exists_by_xpath(exists_once_iframe_in_focus)
