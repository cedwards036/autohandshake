from autohandshake.src.Pages.Page import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL
import time
import os
import glob
from datetime import datetime
from typing import List


class SurveyPage(Page):
    """
    A survey page in Handshake.
    """

    def __init__(self, survey_id: int, browser: HandshakeBrowser):
        """
        :param survey_id: the id of the survey to load
        :type survey_id: int
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        self._id = survey_id
        super().__init__(f'{BASE_URL}/surveys/{survey_id}', browser)

    @Page.require_user_type(UserType.STAFF)
    def download_responses(self, download_dir: str) -> str:
        """
        Download a CSV of the survey responses.

        :param download_dir: the directory into which the survey responses will download
        :type download_dir: str
        :return: the file path of the downloaded file
        :rtype: str
        """
        download_btn_xpath = '//a[text()="Download Results (CSV)"]'
        download_link_xpath = '//a[contains(text(), "Your download is ready")]'
        self._browser.wait_then_click_element_by_xpath(download_btn_xpath)
        self._browser.wait_then_click_element_by_xpath(download_link_xpath)
        return self._confirm_file_downloaded(download_dir)

    def _confirm_file_downloaded(self, dir, wait_time=300) -> str:
        """
        Confirm that the response data file downloaded successfully.

        Throw an error if the file still does not exist when the given wait time
        is up

        :param dir: the expected download directory for the file
        :type dir: str
        :param wait_time: the maximum time to wait for the file to download
        :type wait_time: integer
        :return: the file path of the newly downloaded file
        :rtype: str
        """
        file_name_start = self._get_file_name_start()
        baseline_matches = self._get_filename_matches(file_name_start, dir)
        start_time = time.time()
        time_to_stop = start_time + wait_time
        while time.time() <= time_to_stop:
            time.sleep(0.5)
            updated_matches = self._get_filename_matches(file_name_start, dir)
            if len(updated_matches) == len(baseline_matches) + 1:
                return max(updated_matches, key=os.path.getctime)

        raise RuntimeError('File did not download in time')

    @staticmethod
    def _get_filename_matches(file_name_start: str, dir: str) -> List[str]:
        """

        :param file_name_start: the beginning of the file name string to search for
        :type file_name_start: str
        :param dir: the directory in which to search
        :type dir: str
        :return: a list of matching files
        :rtype: list
        """
        return glob.glob(os.path.join(dir, f'{file_name_start}*.csv'))

    @staticmethod
    def _get_file_name_start() -> str:
        """
        Get the predictable part of the downloaded file name.

        :return: the known part of the response file name.
        :rtype: str
        """
        return 'survey_response_download' + datetime.now().strftime('%Y%m%d')

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
        self._browser.wait_until_element_exists_by_xpath('//div[@class="entity-sidebar tile white"]')
