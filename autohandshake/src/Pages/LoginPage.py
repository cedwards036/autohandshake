from autohandshake.src.Pages.Page import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser
from autohandshake.src.exceptions import InvalidURLError, NoSuchElementError, \
                                         InvalidEmailError, InvalidPasswordError
import re

class LoginPage(Page):
    """
    The old Handshake login page
    """

    def __init__(self, url: str, browser: HandshakeBrowser):
        """
        Create a login page object for the given login page URL

        :param url: the url of the school's Handshake login page
        :type url: str
        :param browser: a HandshakeBrowser that has not logged in yet
        :type browser: HandshakeBrowser
        """
        super().__init__(url, browser)
        self.validate_url_school()

    def wait_until_page_is_loaded(self):
        """Wait until the page has finished loading.

        Return immediately since there are no complex load conditions
        """
        return

    def validate_url(self, url):
        """
        Ensure that the given URL is a valid login URL

        :param url: the url to validate
        :type url: str
        """
        try:
            re.match(r'^https://[a-zA-Z]+\.joinhandshake\.com(/login)?$', url)\
                .group(0)
        except AttributeError:
            raise InvalidURLError()


    def validate_url_school(self):
        """Ensure that the current URL leads to a valid school's login page"""
        if self._browser.element_exists_by_xpath('//span[text()=\'Please '
                                                 'select your school to '
                                                 'sign in.\']'):
            raise InvalidURLError("The school specified in the URL is not valid")


    def login(self, email, password):
        """
        Log into Handshake using the given credentials

        :param email: the username with which to log in
        :type email: str
        :param password: the password with which to log in
        :type password: str
        """
        self._enter_email_address(email)
        self._enter_password(password)
        self._browser.wait_until_element_exists_by_xpath("//span[text()='Student Activity Snapshot']")

    def _enter_email_address(self, email):
        """Enter email address into input field"""
        EMAIL_INPUT_XPATH = "//input[@name='identifier']"

        try: # if you get the old login page
            EMAIL_LINK_XPATH = "//div[@class='sign-with-email-address']//a"
            self._browser.click_element_by_xpath(EMAIL_LINK_XPATH)
            self._browser.send_text_to_element_by_xpath(email, EMAIL_INPUT_XPATH)
            EMAIL_BTN_XPATH = "//div[@class='login-main__email-box']/button"
            self._browser.click_element_by_xpath(EMAIL_BTN_XPATH)
            if self._browser.element_exists_by_xpath("//div[text()='Please enter a valid email address']"):
                raise InvalidEmailError(f"No account found for email {email}")

        except NoSuchElementError: # if you get the new login page
            EMAIL_LINK_XPATH = "//div[@class='sign-in-with-email-address']//a"
            self._browser.click_element_by_xpath(EMAIL_LINK_XPATH)
            self._browser.send_text_to_element_by_xpath(email, EMAIL_INPUT_XPATH)
            EMAIL_BTN_XPATH = "//div[@class='actions']/button"
            self._browser.click_element_by_xpath(EMAIL_BTN_XPATH)
            if 'known_error_message_present=true' in self._browser.current_url:
                raise InvalidEmailError(f"No account found for email {email}")

    def _enter_password(self, password):
        """Enter password into input field after having successfully entered email"""
        try: # if you get the old login page
            self._browser.click_element_by_xpath("//a[@class='no-underline']")
            self._browser.send_text_to_element_by_xpath(password, "//input[@name='password']")
            self._browser.click_element_by_xpath("//input[@name='commit']")
            if self._browser.element_exists_by_xpath("//div[contains(text(), "
                                                     "'You entered an invalid password.')]"):
                raise InvalidPasswordError("Invalid password")
        except NoSuchElementError: # if you get the new login page
            self._browser.click_element_by_xpath("//a[@class='alternate-login-link']")
            self._browser.send_text_to_element_by_xpath(password, "//input[@name='password']")
            self._browser.click_element_by_xpath("//button")
            if self._browser.element_exists_by_xpath("//div[contains(text(), "
                                                     "'You entered an invalid password.')]"):
                raise InvalidPasswordError("Invalid password")