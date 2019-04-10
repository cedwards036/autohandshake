from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL
from autohandshake.src.HandshakeBrowser import HandshakeBrowser
from autohandshake.src.Pages.SchoolSettings.AppointmentTypePage import AppointmentTypePage
import re


class AppointmentTypesListPage(Page):
    """The overview settings page listing all appointment types"""

    def __init__(self, browser: HandshakeBrowser):
        """
        Load the appointment types list view from the school settings

        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(f'{BASE_URL}/schools/{browser.school_id}/appointment_types',
                         browser)

    def get_type_ids(self) -> list:
        """Get a list of appointment type IDs for your school"""
        type_links = self._browser.get_elements_attribute_by_xpath(
            "//div[@class='top-right-btn']/a[@class='btn btn-default']", "href")
        return [self._extract_type_id_from_url(link) for link in type_links]

    def get_type_settings(self, how_many: int = None) -> list:
        """
        Get a list of settings objects for all appointment type settings

        :param how_many: if specified, the number of settings objects to collect.
                         If None (the default), collect all settings. This
                         argument is mainly for testing purposes, as downloading
                         the full list of settings is prohibitively slow for
                         testing.
        :type how_many: int
        :return: a list of type settings objects for all appointment types
        :rtype: list
        """
        settings_list = []
        type_ids = self.get_type_ids()
        if not how_many:
            how_many = len(type_ids)
        for i in range(0, how_many):
            id = type_ids[i]
            type_page = AppointmentTypePage(id, self._browser)
            settings_list.append(type_page.get_settings())
        return settings_list

    def _extract_type_id_from_url(self, url):
        """Given an appointment type settings url, extract the type id"""
        return int(re.search("/appointment_types/([0-9]+)/edit", url).group(1))

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
        self._browser.wait_until_element_exists_by_xpath("//*[@class='top-right-btn']")
