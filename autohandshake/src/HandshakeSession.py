from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, \
                                       NoSuchElementException
import re
from typing import Type

from autohandshake.src.Pages.Page import Page
from autohandshake.src.exceptions import InvalidURLError


class HandshakeSession:
    """
    A Handshake browsing session.

    To be used as a context manager. Example:

    with HandshakeSession("https://jhu.joinhandshake.edu", username, password) as hs:
        [do something]

    """

    def __init__(self, login_url: str):
        """
        Initialize Handshake session.

        :param login_url: a valid Handshake homepage url of the form
                          "https://[school].joinhandshake.com"
        :type login_url: str
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')

        if self._login_url_str_is_invalid(login_url):
            raise InvalidURLError('Login URL must be of the form '
                             '"https://[school].joinhandshake.com"')

        self._browser = webdriver.Chrome(executable_path='../chromedriver.exe',
                                         options=options)
        self._login_url = login_url

    def __enter__(self)->'HandshakeSession':
        """Open a web browser and log into Handshake, beginning the session"""
        self._browser.get(self._login_url)
        if self._school_is_invalid():
            raise InvalidURLError('Invalid school in login URL')
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the web browser"""
        self.close()


    def close(self):
        """Close the Handshake Session"""
        self._browser.quit()


    @staticmethod
    def _login_url_str_is_invalid(login_url: str)->bool:
        """
        Determine whether or not a given Handshake login URL is valid

        :param login_url: the login url to test
        :type login_url: str
        :return: True is the url is valid, false otherwise
        :rtype: bool
        """
        try:
            re.match(r'^https://[a-zA-Z]+\.joinhandshake\.com', login_url) \
                .group(0)
            return False
        except AttributeError:
            return True


    def _school_is_invalid(self)->bool:
        """
        Determine whether or not the current Handshake URL' school is invalid.

        If the page asks the user to select a school before signing in, that
        means the URL had an invalid school to begin with.

        :return: True if the school is invalid, false otherwise
        :rtype: bool
        """
        try:
            self._browser.find_element_by_xpath('//span[text()=\'Please select '
                                               'your school to sign in.\']')
            return True
        except NoSuchElementException:
            return False
