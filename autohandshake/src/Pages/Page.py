from abc import ABC, abstractmethod
from selenium.webdriver.chrome.webdriver import WebDriver

class Page(ABC):
    """
    A single web page on the Handshake site
    """

    def __init__(self, url: str):
        """
        Create a page object for the given URL

        :param url: the url of the page to initialize
        :type url: str
        """
        self._url = url

    @abstractmethod
    def page_is_loaded(self, browser: WebDriver)->bool:
        """Determine whether or not the page has fully loaded.

        For pages without complex javascript involved in the load, simply
        returning True is sufficient.
        """
        raise NotImplementedError

    @property
    def url(self):
        """Get the page's url"""
        return self._url