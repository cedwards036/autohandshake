from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from enum import Enum
import re
import os

from autohandshake.src.exceptions import (
    InvalidURLError, NoSuchElementError, WrongPageForMethodError,
    InsufficientPermissionsError, InvalidUserTypeError
)
from autohandshake.src.constants import MAX_WAIT_TIME
from autohandshake.src.constants import BASE_URL


class UserType(Enum):
    """
    The possible user types in Handshake

            * Employer - a Handshake employer account
            * Staff - a career services staff/admin account
            * Student - a student or alumni account
    """

    EMPLOYER = 'Employers'
    STAFF = 'Career Services'
    STUDENT = 'Students'


class HandshakeBrowser:
    """
    An automated browser for navigating Handshake.

    Since a logged-in instance of this class is returned by HandshakeSession's
    __enter__ method, it does not usually need to be manually instantiated. Additionally,
    for most use cases, the user only needs to pass a HandshakeBrowser object to
    a Page object, then let the Page's methods do the heavy-lifting.

    For example, you almost never need to write:
    ::
        browser = HandshakeBrowser()

    The vast majority of use cases look something like:
    ::
        with HandshakeSession(school_url, email) as browser:
            some_page = SomePage(browser)
            some_page.do_something()

    If you need to specify a custom max_wait_time, that can be done through the
    HandshakeSession object:
    ::
        # this
        with HandshakeSession(school_url, email, max_wait_time = 60) as browser:
            some_page = SomePage(browser)

        # not this
        browser = HandshakeBrowser(max_wait_time = 60)

    """

    def __init__(self, max_wait_time: int = MAX_WAIT_TIME):
        """
        :param max_wait_time: the maximum time (in seconds) to wait for an element
                              to load before throwing a timeout error
        :type max_wait_time: int
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')

        dirname = os.path.dirname(__file__)
        driver_path = os.path.join(dirname, '../chromedriver.exe')

        self._browser = webdriver.Chrome(executable_path=driver_path,
                                         options=options)
        self.max_wait_time = max_wait_time
        self._user_type = None

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
            WebDriverWait(self._browser, self.max_wait_time).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            raise TimeoutError(f"Element with xpath {xpath} did not appear in time")

    def wait_until_element_does_not_exist_by_xpath(self, xpath: str):
        """
        Wait until an element with the given xpath exists on the page.

        :param xpath: the xpath of the element to wait for
        :type xpath: str
        """
        try:
            WebDriverWait(self._browser, self.max_wait_time).until(
                EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            raise TimeoutError(f"Element with xpath {xpath} did not disappear in tme")

    def wait_until_element_is_clickable_by_xpath(self, xpath: str):
        """
        Wait until an element with the given xpath is clickable.

        :param xpath: the xpath of the element to wait for
        :type xpath: str
        """
        try:
            WebDriverWait(self._browser, self.max_wait_time).until(
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

    def wait_then_click_element_by_xpath(self, xpath):
        """
        Click an element on the page given its xpath after waiting to make sure
        it exists

        :param xpath: the xpath of the element to click
        :type xpath: str
        """
        self.wait_until_element_exists_by_xpath(xpath)
        self.click_element_by_xpath(xpath)

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

    def execute_script_on_element_by_xpath(self, script: str, xpath: str = None):
        """
        Execute the given javascript expression. If xpath of element is provided,
        the element becomes available to use in the script, and can be accessed
        using arguments[0].

        :param script: the javascript to be executed
        :type script: str
        :param xpath: the xpath of the optional element to be passed to the script
        :type xpath: str
        """
        if not xpath:
            self._browser.execute_script(script)
        else:
            try:
                self._browser.execute_script(script, self._browser.find_element_by_xpath(xpath))
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

    def update_constants(self):
        """
        Update any Handshake environment constants such as School ID or User ID.

        This should be done every time the browser switches user types and upon
        initial login.
        """
        if self._user_type == UserType.EMPLOYER:
            self.employer_id = self._get_meta_constant('logged_in_user_institution_id')
        else:
            self.school_id = self._get_meta_constant('logged_in_user_institution_id')
        self.user_id = self._get_meta_constant('logged_in_user_id')
        self._user_type = UserType(self._get_meta_constant('current_user_type'))

    def _get_meta_constant(self, name: str) -> str:
        """
        Get the content of a meta tag with the given name.

        The method is used to pull data like the current school id, user id,
        or employer id from Handshake's <meta> tags. All tags are of the form:
        <meta content="foo" name="bar">. Given "bar," this method returns "foo".

        :param name: the name of the meta tag to query
        :type name: str
        :return: the content of the meta tag
        :rtype: str
        """
        return self.get_element_attribute_by_xpath(f'//meta[@name="{name}"]',
                                                   'content')

    def switch_to_new_tab(self):
        """Wait for the new tab to finish loaded, then switch to it."""
        WebDriverWait(self._browser, self.max_wait_time).until(
            EC.number_of_windows_to_be(2))
        self._browser.switch_to.window(self._browser.window_handles[-1])

    def return_to_main_tab(self):
        """With a second tab open, close the current tab and return to the main tab."""
        self._browser.execute_script('window.close();')
        self._browser.switch_to.window(self._browser.window_handles[0])

    def maximize_window(self):
        """Maximize the browser window."""
        self._browser.maximize_window()

    @property
    def user_type(self) -> UserType:
        """
        Get the user type of the account currently logged into Handshake.

        :return: the browser's currently-logged-in user type
        :rtype: UserType
        """
        return self._user_type

    def switch_users(self, user_type: UserType):
        """
        Switch to the system view specified by the given user type.

        This method automates the built-in "Switch Users" function in Handshake.

        :param user_type: the user type to which to switch
        :type user_type: UserType
        """
        if self._user_type == user_type:
            return  # do nothing if the browser already has the desired user type
        self.get(f'{BASE_URL}/user_switcher/options')
        try:
            self.click_element_by_xpath(f'//a[div[h4[contains(text(), "{user_type.value}")]]]')
        except NoSuchElementError:
            raise InvalidUserTypeError("User does not have a linked account of the given type")
        self.update_constants()

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
            raise InvalidURLError(self._browser.current_url)

    def _validate_permissions(self):
        """Determine whether or not the logged in user has permission to view the current page"""
        if self.element_exists_by_xpath("//div[contains(text(), 'You do not "
                                        "have permission to do that.')]"):
            raise InsufficientPermissionsError
