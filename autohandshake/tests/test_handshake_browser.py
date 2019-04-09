import unittest

from autohandshake import HandshakeBrowser
from autohandshake.src.exceptions import InvalidURLError
from autohandshake.src.constants import BASE_URL

class TestHandshakeBrowser(unittest.TestCase):

    def test_throws_error_if_given_invalid_url(self):
        completely_wrong_url = "https://www.google.com/"
        invalid_url = "https://jhu.joinhandhake.com/"
        not_a_url = "hello world"
        no_https = "jhu.joinhandshake.com"


        with self.assertRaises(InvalidURLError):
            browser = HandshakeBrowser()
            browser.get(completely_wrong_url)
            browser.quit()

        with self.assertRaises(InvalidURLError):
            browser = HandshakeBrowser()
            browser.get(invalid_url)
            browser.quit()

        with self.assertRaises(InvalidURLError):
            browser = HandshakeBrowser()
            browser.get(not_a_url)
            browser.quit()

        with self.assertRaises(InvalidURLError):
            browser = HandshakeBrowser()
            browser.get(no_https)
            browser.quit()

    def test_element_exists_by_xpath(self):
        # tests valid as of 4/8/19
        browser = HandshakeBrowser()
        browser.get(BASE_URL)

        self.assertTrue(browser.element_exists_by_xpath('//div'))
        self.assertTrue(browser.element_exists_by_xpath("//div/input[@class='login-main__email-input']"))

        self.assertFalse(browser.element_exists_by_xpath("//div[@class='this_isnt_a_real_class']"))

        browser.quit()
