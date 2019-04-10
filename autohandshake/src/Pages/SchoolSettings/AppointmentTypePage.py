from typing import Optional

from autohandshake.src.HandshakeBrowser import HandshakeBrowser
from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL


class AppointmentTypePage(Page):
    """A settings page for a single appointment type."""

    def __init__(self, type_id: int, browser: HandshakeBrowser):
        """
        Load the appointment type settings page for the type with the given id

        :param type_id: the id of the appointment type to load
        :type type_id: int
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        self._id = type_id
        super().__init__(f'{BASE_URL}/appointment_types/{type_id}/edit', browser)

    def get_settings(self) -> dict:
        settings = {}

        # collect fields from first page
        settings['id'] = self._id
        settings['name'] = self._browser.get_element_attribute_by_xpath(
            "//*[@id='appointment_type_name']", "value")
        settings['description'] = self._browser.get_element_attribute_by_xpath(
            "//*[@id='appointment_type_description']", "value")
        settings['length'] = int(self._browser.get_element_attribute_by_xpath(
            "//*[@id='appointment_type_length']", "value"))
        settings['categories'] = self._parse_multi_option_appt_type_field(
            's2id_appointment_type_appointment_category_ids')
        settings['drop_in_enabled'] = self._browser.element_is_selected_by_xpath(
            "//*[@id='appointment_type_drop_in_enabled']")
        settings['pre_message'] = self._browser.get_element_attribute_by_xpath(
            "//*[@id='appointment_type_pre_message']", "value")
        settings['pre_survey'] = self._parse_survey_drop_down('s2id_appointment_type_pre_survey_id')
        settings['post_message'] = self._browser.get_element_attribute_by_xpath(
            "//*[@id='appointment_type_post_message']", "value")
        settings['post_survey'] = self._parse_survey_drop_down('s2id_appointment_type_post_survey_id')
        settings['staff_survey'] = self._parse_survey_drop_down('s2id_appointment_type_advisor_survey_id')

        # switch to second page
        self._browser.click_element_by_xpath("//a[text()='Requirements']")
        self._browser.wait_until_element_exists_by_xpath(
            "//*[@id='student_screen_cumulative_gpa_required']")

        # collect fields from second page
        settings['school_years'] = self._parse_school_year_requirements()
        settings['cum_gpa_required'] = self._browser.element_is_selected_by_xpath(
            "//*[@id='student_screen_cumulative_gpa_required']")
        settings['cum_gpa'] = float(self._browser.get_element_attribute_by_xpath(
            "//*[@id='student_screen_cumulative_gpa']", "value"))
        settings['major_groups'] = self._parse_major_group_qualifications()
        settings['colleges'] = self._parse_multi_option_appt_type_field(
            's2id_student_screen_college_ids')
        settings['labels'] = self._parse_multi_option_appt_type_field(
            's2id_student_screen_institution_label_ids')
        settings['career_clusters'] = self._parse_multi_option_appt_type_field(
            's2id_student_screen_custom_job_interest_option_ids')

        return settings

    def validate_url(self, url):
        """
        Ensure that the given URL is a valid login URL.

        Since the URL is not entered by the user, it is always valid.

        :param url: the url to validate
        :type url: str
        """
        return

    def wait_until_page_is_loaded(self):
        """Wait until the page has finished loading."""
        self._browser.wait_until_element_exists_by_xpath("//input[@id='appointment_type_name']")

    def _parse_multi_option_appt_type_field(self, parent_div_id: str) -> list:
        """
        Extract all selected values from a multi-value text field.

        :param parent_div_id: the id of the parent div of the field
        :type parent_div_id: str
        :return: a list of all selected values in the field
        :rtype: list
        """
        return self._browser.get_elements_attribute_by_xpath(
            f"//*[@id='{parent_div_id}']//*[@class='select2-search-choice']//div",
            "text")

    def _parse_survey_drop_down(self, parent_div_id: str) -> Optional[str]:
        """
        Extract the name of the selected survey from a survey drop-down.

        :param parent_div_id: the id of the parent div of the drop-down
        :type parent_div_id: str
        :return: the name of the selected survey, if any
        :rtype: str
        """
        non_choices = ['Pre Survey...', 'Post Survey...', 'Advisor Survey...']
        survey_name = self._browser.get_element_attribute_by_xpath(
            f"//*[@id='{parent_div_id}']//*[@class='select2-chosen']", "text")
        if survey_name in non_choices:
            return None
        return survey_name

    def _parse_school_year_requirements(self) -> Optional[list]:
        """
        Extract the selected school years from the requirements page

        :return: a list of selected school years, if any
        :rtype: list
        """
        element_mapping = {
            1: 'Freshman',
            2: 'Sophomore',
            3: 'Junior',
            4: 'Senior',
            5: 'Masters',
            6: 'Doctorate',
            7: 'Alumni',
            8: 'Postdoctoral Studies',
        }
        school_years_required = []
        for i in range(1, 9):
            if self._browser.element_is_selected_by_xpath(
                    f"//*[@id='student_screen_school_year_ids_{i}']"):
                school_years_required.append(element_mapping[i])
        if not school_years_required:
            return None
        return school_years_required

    def _parse_major_group_qualifications(self) -> Optional[list]:
        """
        Extract the selected major groups and majors from the requirements page.

        Selected major groups will be prefixed with "major_group: " and any
        individual majors will be prefixed with "indv_major: "

        :return: a list of selected majors and major groups, if any
        :rtype: list
        """
        major_qualifications = []
        groups = self._browser.get_elements_attribute_by_xpath("//*[contains(@class, 'label-primary')]/span", "text")
        indv_majors = self._browser.get_elements_attribute_by_xpath("//*[contains(@class, 'label-info')]/span", "text")
        for group in groups:
            major_qualifications.append('major_group: ' + group)
        for indv_major in indv_majors:
            major_qualifications.append('indv_major: ' + indv_major)
        if not major_qualifications:
            return None
        return major_qualifications
