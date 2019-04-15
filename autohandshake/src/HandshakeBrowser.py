from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, \
    NoSuchElementException, TimeoutException
import re
import os

from autohandshake.src.exceptions import InvalidURLError, NoSuchElementError, \
    WrongPageForMethodError, InsufficientPermissionsError
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
        self._validate_url_str(url)
        self._browser.get(url)
        self._validate_page_exists()
        self._validate_permissions()

    def quit(self):
        """Close the browser"""
        self._browser.quit()

    def element_exists_by_xpath(self, xpath: str) -> bool:
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
        try:
            WebDriverWait(self._browser, MAX_WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            raise TimeoutError(f"Element with xpath {xpath} did not appear")

    def wait_until_element_is_clickable_by_xpath(self, xpath: str):
        """
        Wait until an element with the given xpath is clickable.

        :param xpath: the xpath of the element to wait for
        :type xpath: str
        """
        try:
            WebDriverWait(self._browser, MAX_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            raise TimeoutError(f"Element with xpath {xpath} did not become clickable")

    def send_text_to_element_by_xpath(self, xpath: str, text: str, clear: bool = True):
        """
        Send a string to an input field identified by the given xpath

        :param text: the text to send
        :type text: str
        :param xpath: the xpath of the input field to which to send the text
        :type xpath: str
        :param clear: whether or not to clear the field before sending text. If
                      False, text will be appended to any text already present.
        :type clear: bool
        """
        try:
            element = self._browser.find_element_by_xpath(xpath)
            if clear:
                element.clear()
            element.send_keys(text)
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

    def get_element_attribute_by_xpath(self, xpath: str, attribute: str) -> str:
        """
        Get the value of the given attribute from the element with the given xpath

        :param xpath: the xpath of the element of interest
        :type xpath: str
        :param attribute: the name of the attribute of interest, e.g. 'value'
        :type attribute: str
        :return: the value of the attribute on the element of interest
        :rtype: str
        """
        try:
            if attribute.lower() == 'text':
                return self._browser.find_element_by_xpath(xpath).text
            return self._browser.find_element_by_xpath(xpath).get_attribute(attribute)
        except NoSuchElementException:
            raise NoSuchElementError(f'No element found for xpath: "{xpath}"')

    def get_elements_attribute_by_xpath(self, xpath: str, attribute: str) -> list:
        """
        Get the value of a given attribute for all elements with the given xpath

        :param xpath: the xpath of the elements of interest
        :type xpath: str
        :param attribute: the name of the attribute of interest, e.g. 'value'
        :type attribute: str
        :return: a list of values of the given attribute for each matching element
        :rtype: list
        """
        try:
            elements = self._browser.find_elements_by_xpath(xpath)
            if attribute.lower() == 'text':
                return [element.text for element in elements]
            return [element.get_attribute(attribute) for element in elements]
        except NoSuchElementException:
            raise NoSuchElementError(f'No elements found for xpath: "{xpath}"')

    def element_is_selected_by_xpath(self, xpath: str) -> bool:
        """Get whether or not the element specified by the given xpath is selected

        :param xpath: the xpath of the elements of interest
        :type xpath: str
        :return: True if the element is selected, False otherwise
        :rtype: bool
        """
        try:
            return self._browser.find_element_by_xpath(xpath).is_selected()
        except:
            raise NoSuchElementError(f'No elements found for xpath: "{xpath}"')

    def switch_to_frame_by_xpath(self, xpath):
        try:
            frame = self._browser.find_element_by_xpath(xpath)
            self._browser.switch_to.frame(frame)
        except NoSuchElementException:
            raise NoSuchElementError(f'No elements found for xpath: "{xpath}"')

    def record_school_id(self):
        """Record the school's Handshake ID from a link in the main sidebar"""
        try:
            full_href = self._browser.find_element_by_css_selector(
                "a[href*='/schools/'").get_attribute('href')
            final_slash_position = full_href.rfind(r'/')
            school_id = full_href[final_slash_position + 1:]
            self.school_id = school_id
        except NoSuchElementException:
            raise WrongPageForMethodError('The main sidebar must be visible in '
                                          'order to get the school id')

    def switch_to_new_tab(self):
        """Wait for the new tab to finish loaded, then switch to it."""
        WebDriverWait(self._browser, MAX_WAIT_TIME).until(
            EC.number_of_windows_to_be(2))
        self._browser.switch_to.window(self._browser.window_handles[-1])

    def return_to_main_tab(self):
        """With a second tab open, close the current tab and return to the main tab."""
        self._browser.execute_script('window.close();')
        self._browser.switch_to.window(self._browser.window_handles[0])

    @property
    def current_url(self):
        """Get the url of the browser's current page"""
        return self._browser.current_url

    @staticmethod
    def _validate_url_str(url: str):
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

    def _validate_page_exists(self):
        """Determine whether the current page exists or gave a 404 error."""
        if self.element_exists_by_xpath("//p[contains(text(), 'You may want "
                                        "to head back to the homepage.')]"):
            raise InvalidURLError

    def _validate_permissions(self):
        """Determine whether or not the logged in user has permission to view the current page"""
        if self.element_exists_by_xpath("//div[contains(text(), 'You do not "
                                        "have permission to do that.')]"):
            raise InsufficientPermissionsError
