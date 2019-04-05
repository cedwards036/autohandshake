from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
import re


class HandshakeSession:
    """
    A Handshake browsing session.
    """

    def __init__(self, login_url: str):
        """
        Initialize Handshake session.

        :param login_url: a valid Handshake login url of the form
                          "https://[school].joinhandshake.com"
        :type login_url: str
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')

        if not self._login_url_str_is_valid(login_url):
            raise ValueError('Login URL must be of the form "https://[school].joinhandshake.com"')

        self.login_url = login_url
        self.browser = webdriver.Chrome(executable_path='../chromedriver.exe',
                                        options=options)

    def __enter__(self):
        self.browser.get(self.login_url)
        if self._school_is_invalid():
            raise ValueError('Invalid school in login URL')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    @staticmethod
    def _login_url_str_is_valid(login_url: str):
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
            return True
        except AttributeError:
            return False

    def _school_is_invalid(self):
        """
        Determine whether or not the current Handshake URL' school is invalid.

        If the page asks the user to select a school before signing in, that
        means the URL had an invalid school to begin with.

        :return: True if the school is invalid, false otherwise
        :rtype: bool
        """
        try:
            self.browser.find_element_by_xpath('//span[text()=\'Please select '
                                               'your school to sign in.\']')
            return True
        except NoSuchElementException:
            return False
