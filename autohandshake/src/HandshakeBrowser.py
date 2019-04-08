from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, \
                                       NoSuchElementException
import re

from autohandshake.src.exceptions import InvalidURLError

class HandshakeBrowser:
    """An automated browser for navigating Handshake"""

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')

        self._browser = webdriver.Chrome(executable_path='../chromedriver.exe',
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