from abc import ABC, abstractmethod
from autohandshake.src.HandshakeBrowser import HandshakeBrowser

class Page(ABC):
    """
    A single web page on the Handshake site
    """

    def __init__(self, url: str, browser: HandshakeBrowser):
        """
        Create a page object for the given URL

        :param url: the url of the page to initialize
        :type url: str
        :param browser: a HandshakeBrowser that is logged in to Handshake
        :type browser: HandshakeBrowser
        """
        self._url = url
        self._browser = browser
        self._browser.get(url)
        self.wait_until_page_is_loaded()

    @abstractmethod
    def wait_until_page_is_loaded(self):
        """Determine whether or not the page has fully loaded.

        For pages without complex javascript involved in the load, simply
        returning True is sufficient.
        """
        raise NotImplementedError


    @abstractmethod
    def validate_current_page(self):
        """Ensure that the browser is on the correct page before calling a method.

        To be used to make sure methods on this page are not called while the
        browser is on a different page
        """
        raise NotImplementedError


    @property
    def url(self):
        """Get the page's url"""
        return self._url