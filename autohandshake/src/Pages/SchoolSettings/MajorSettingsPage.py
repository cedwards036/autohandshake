from autohandshake.src.Pages import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL
from typing import List


class MajorSettingsPage(Page):

    def __init__(self, browser: HandshakeBrowser):
        """
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        majors_base_url = f'{BASE_URL}/schools/{browser.school_id}/school_majors'
        url_query = '?ajax=true&query=&category=ManageSchoolMajors&page=1&per_page=5000&sort_direction=asc&sort_column=default&followed_only=false&qualified_only=&core_schools_only=false&including_all_facets_in_searches=false'
        super().__init__(majors_base_url + url_query,
                         browser)

    @Page.require_user_type(UserType.STAFF)
    def get_major_mapping(self) -> List[dict]:
        """
        Get a list of all the school's majors and their associated major groups.

        :return: a list of major-to-major-group mapping dicts, of the form:
                 {'major': 'major name', 'groups': ['group 1', 'group 2', etc]}
        :rtype: list
        """
        mappings = []

        majors = self._browser.get_elements_attribute_by_xpath("//tbody/tr/td[1]/a", "text")
        group_strings = self._browser.get_elements_attribute_by_xpath("//tbody/tr/td[2]/a", "text")

        for i in range(len(majors)):
            groups = self._parse_major_groups_string(group_strings[i])
            mappings.append({
                'major': majors[i],
                'groups': groups
            })

        return mappings

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
        self._browser.wait_until_element_exists_by_xpath("//tbody/tr")

    def _parse_major_groups_string(self, groups_string: str) -> List[str]:
        """
        Parse a comma-separated list of major groups into a list of distinct groups.

        :param groups_string: a comma-separated string of major groups
        :type groups_string: str
        :return: a list of the separate major groups
        :rtype: list
        """
        groups_with_commas_in_them = [
            'City, Urban, Regional Planning',
            'Parks, Recreation & Leisure Studies',
            'Radio, Television, Media'
        ]
        groups = groups_string.split(', ')
        for group in groups_with_commas_in_them:
            groups = self._correct_oversplit_string(groups, group)
        return groups

    @staticmethod
    def _correct_oversplit_string(str_list: List[str], joined_str: str) -> List[str]:
        """
        If every word in the given joined string is present in the given list,
        replace the separate words with a single instance of the joined string.

        Ex: you want to split the string "London, England, Boston" into the list
        ["London, England", "Boston"]. Merely splitting the string on commas will
        give you ["London", "England", "Boston"]. Calling this function with the
        arguments ["London", "England", "Boston"] and "London, England" will
        return the list ["London, England", "Boston"].

        :param str_list: a list of strings containing at least one overly-split
                         series of sub-strings
        :type str_list: list
        :param joined_str: the full string with which to replace the overly-split,
                           separate elements of this string in the list
        :type joined_str: str
        :return: the original list with all disparate elements of joined_str
                 replaced by the full joined_str
        :rtype: list
        """
        group_is_in_list = True
        group_words = joined_str.split(', ')
        for word in group_words:
            if not word in str_list:
                group_is_in_list = False

        if group_is_in_list:
            new_list = []
            for group_name in str_list:
                if not group_name in group_words:
                    new_list.append(group_name)
            new_list.append(joined_str)
            return new_list
        return str_list
