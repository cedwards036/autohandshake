from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL


class CareerInterestsPage(Page):
    """A settings page for a single student's career interests.

    Only accessible while logged in as a student.
    """

    def __init__(self, student_id: int, browser: HandshakeBrowser):
        """
        :param student_id: the id of the student whose career interests page you are to visit
        :type student_id: int
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        self._id = student_id
        super().__init__(f'{BASE_URL}/users/{student_id}/career_interests', browser)
        browser.execute_script_on_element_by_xpath('window.scroll(0, 1000)')

    def cluster_is_selected_by_id(self, cluster_id: int) -> bool:
        """
        Check whether or not a specific cluster is selected, given the cluster ID.

        :param cluster_id: the id of the cluster to check
        :type cluster_id: int
        :return: True if the cluster is selected, false otherwise
        """
        cluster_xpath = f'//{self._get_cluster_xpath_by_id(cluster_id)}'
        return self._browser.element_is_selected_by_xpath(cluster_xpath)

    def cluster_is_selected_by_name(self, cluster_name: str) -> bool:
        """
        Check whether or not a specific cluster is selected, given the cluster name.

        :param cluster_name: the name of the cluster to check (case-sensitive)
        :type cluster_name: str
        :return: True if the cluster is selected, false otherwise
        """
        cluster_xpath = f'//{self._get_cluster_xpath_by_name(cluster_name)}'
        return self._browser.element_is_selected_by_xpath(cluster_xpath)

    def select_cluster_by_id(self, cluster_id: int):
        """
        Select a career cluster given its id.

        :param cluster_id: the id of the cluster to select
        :type cluster_id: int
        """
        cluster_xpath = f'//label[{self._get_cluster_xpath_by_id(cluster_id)}]'
        if not self.cluster_is_selected_by_id(cluster_id):
            self._browser.click_element_by_xpath(cluster_xpath)

    def select_cluster_by_name(self, cluster_name: str):
        """
        Select a career cluster given its name.

        :param cluster_name: the name of the cluster to select (case-sensitive)
        :type cluster_name: str
        """
        cluster_xpath = f'//label[{self._get_cluster_xpath_by_name(cluster_name)}]'
        if not self.cluster_is_selected_by_name(cluster_name):
            self._browser.click_element_by_xpath(cluster_xpath)

    def deselect_cluster_by_id(self, cluster_id: int):
        """
        Deselect a career cluster given its ID.

        :param cluster_id: the id of the cluster to deselect
        :type cluster_id: int
        """
        cluster_xpath = f'//label[{self._get_cluster_xpath_by_id(cluster_id)}]'
        if self.cluster_is_selected_by_id(cluster_id):
            self._browser.click_element_by_xpath(cluster_xpath)

    def deselect_cluster_by_name(self, cluster_name: str):
        """
        Deselect a career cluster given its name.

        :param cluster_name: the name of the cluster to deselect (case-sensitive)
        :type cluster_name: str
        """
        cluster_xpath = f'//label[{self._get_cluster_xpath_by_name(cluster_name)}]'
        if self.cluster_is_selected_by_name(cluster_name):
            self._browser.click_element_by_xpath(cluster_xpath)

    def save_interests(self):
        """
        Save any changes made to the student's career interests.
        """
        self._browser.click_element_by_xpath('//button[text()="Save My Career Interests"]')
        confirmation_msg_xpath = '//div[contains(text(), "Thanks for updating your Career Interests")]'
        self._browser.wait_until_element_exists_by_xpath(confirmation_msg_xpath)

    def _get_cluster_xpath_by_id(self, cluster_id: int) -> str:
        """
        Generate the xpath of a cluster's checkbox given its id.

        :param cluster_id: the id of the cluster to find
        :type cluster_id: int
        :return: the xpath of the cluster's check-box
        """
        return f'input[@value="{cluster_id}"]'

    def _get_cluster_xpath_by_name(self, cluster_name: str) -> str:
        """
        Generate the xpath of a cluster's checkbox given its name.

        :param cluster_name: the name of the cluster to find (case-sensitive)
        :type cluster_name: str
        :return: the xpath of the cluster's check-box
        """
        return f'input[../span[text()="{cluster_name}"]]'

    def _validate_url(self, url):
        """
        Ensure that the given URL is a valid URL.

        Since the URL is not entered by the user, it is always valid.

        :param url: the url to validate
        :type url: str
        """
        return

    def _wait_until_page_is_loaded(self):
        """Wait until the page has finished loading."""
        self._browser.wait_until_element_exists_by_xpath("//div[@data-bind='foreach: custom_job_interest_options']")
