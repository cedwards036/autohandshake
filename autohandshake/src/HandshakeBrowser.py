from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, \
                                       NoSuchElementException
import re
import os

from autohandshake.src.exceptions import InvalidURLError, NoSuchElementError, WrongPageForMethodError
from autohandshake.src.constants import MAX_WAIT_TIME

class HandshakeBrowser:
    """An automated browser for navigating Handshake"""

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')

        dirname = os.path.dirname(__file__)
        driver_path = os.path.join(dirname, '../chromedriver.exe')

        self._browser = webdriver.Chrome(executable_path=driver_path,
                                         options=options)


    def get(self, url: str):
        """Go to the web page specified by the given Handshake url.

        :param url: the url to visit. Must be of the form
                    "https://[...].joinhandshake.com[/...]"
        :type url: str
        """
        self._validate_url(url)
        self._browser.get(url)


    def quit(self):
        """Close the browser"""
        self._browser.quit()


    def element_exists_by_xpath(self, xpath: str)->bool:
        """
        Determine whether or not an element with the given xpath exists in the page.

        :param xpath: the xpath of the element to search for
        :type xpath: str
        :return: True if the element exists, false otherwise
        :rtype: bool
        """
        try:
            self._browser.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False


    def wait_until_element_exists_by_xpath(self, xpath: str):
        """
        Wait until an element with the given xpath exists on the page.

        :param xpath: the xpath of the element to wait for
        :type xpath: str
        """
        WebDriverWait(self._browser, MAX_WAIT_TIME).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))


    def send_text_to_element_by_xpath(self, text: str, xpath: str):
        """
        Send a string to an input field identified by the given xpath

        :param text: the text to send
        :type text: str
        :param xpath: the xpath of the input field to which to send the text
        :type xpath: str
        """
        try:
            self._browser.find_element_by_xpath(xpath).send_keys(text)
        except NoSuchElementException:
            raise NoSuchElementError(f'No element found for xpath: "{xpath}"')


    def click_element_by_xpath(self, xpath):
        """
        Click an element on the page given its xpath

        :param xpath: the xpath of the element to click
        :type xpath: str
        """
        try:
            self._browser.find_element_by_xpath(xpath).click()
        except NoSuchElementException:
            raise NoSuchElementError(f'No element found for xpath: "{xpath}"')


    def record_school_id(self):
        """Record the school's Handshake ID from a link in the main sidebar"""
        try:
            full_href = self._browser.find_element_by_css_selector("a[href*='/schools/'").get_attribute('href')
            final_slash_position = full_href.rfind(r'/')
            school_id = full_href[final_slash_position + 1:]
            self.school_id = school_id
        except NoSuchElementException:
            raise WrongPageForMethodError('The main sidebar must be visible in '
                                          'order to get the school id')


    @property
    def current_url(self):
        """Get the url of the browser's current page"""
        return self._browser.current_url

    @staticmethod
    def _validate_url(url: str):
        """
        Determine whether or not a given Handshake URL is valid

        :param login_url: the login url to test
        :type login_url: str
        """
        try:
            re.match(r'^https://[a-zA-Z]+\.joinhandshake\.com', url) \
                .group(0)
        except AttributeError:
            raise InvalidURLError('URL must be of the form '
                             '"https://app.joinhandshake.com[/...]" or '
                             '"https://[school name].joinhandshake.com[/...]"')