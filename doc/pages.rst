=====
Pages
=====

.. automodule:: autohandshake

AccessRequestPage
=================
.. autoclass:: AccessRequestPage
    :members:

.. autoclass:: RequestStatus
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, AccessRequestPage, RequestStatus

    with HandshakeBrowser(school_url, email) as browser:
        access_request_page = AccessRequestPage(browser)
        rejected_requests = access_request_page.get_request_data(RequestStatus.REJECTED)
        successful_requests = access_request_page.get_request_data(RequestStatus.SUCCESSFUL)
        all_requests = access_request_page.get_request_data()

AppointmentCalendarPage
=======================

.. autoclass:: AppointmentCalendarPage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, AppointmentCalendarPage
    import datetime

    with HandshakeBrowser(school_url, email) as browser:
        calendar_page = AppointmentCalendarPage(browser)
        unfilled = calendar_page.get_unfilled_blocks(start_date = datetime.datetime(2019, 4, 3).date(),
                                                     end_date = datetime.datetime(2019, 4, 10).date(),
                                                     include_mediums = True)

AppointmentTypePage
===================

.. autoclass:: AppointmentTypePage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, AppointmentTypePage

    stem_appt_type_id = 21849

    with HandshakeBrowser(school_url, email) as browser:
        type_page = AppointmentTypePage(stem_appt_type_id, browser)
        settings = type_page.get_settings()

AppointmentTypesListPage
========================

.. autoclass:: AppointmentTypesListPage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, AppointmentTypesListPage

    with HandshakeBrowser(school_url, email) as browser:
        types_page = AppointmentTypesListPage(browser)
        all_settings = types_page.get_type_settings()

InsightsPage
============

.. autoclass:: InsightsPage
    :members:

.. autoclass:: FileType
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, InsightsPage, FileType
    import datetime

    # you can use either the full url or just the query string portion to instantiate the page.
    full_url = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD1pcDFLd0ZlSmh4VVdobXYxa212U2xuJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
    query_str = 'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD1pcDFLd0ZlSmh4VVdobXYxa212U2xuJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='

    with HandshakeBrowser(school_url, email) as browser:
        full_url_insights_page = InsightsPage(full_url, browser)
        # load the data into python as a list of dicts for further manipulation
        report_data = full_url_insights_page.get_data()

        query_insights_page = InsightsPage(query_str, browser)
        # change the date range filter of the report before downloading the results as an excel file
        query_insights_page.set_date_range_filter('Appointments', 'Start Date Date',
                                                  start_date = datetime.datetime(2018, 1, 1),
                                                  end_date = datetime.datetime(2019, 1, 1))
        query_insights_page.download_file(download_dir = 'C:\\Users\\user425\\Downloads\\',
                                          file_name = 'appointment_data_by_status.xlsx',
                                          file_type = FileType.EXCEL)



MajorSettingsPage
=================

.. autoclass:: MajorSettingsPage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, MajorSettingsPage

    with HandshakeBrowser(school_url, email) as browser:
        major_settings_page = MajorSettingsPage(browser)
        mapping = major_settings_page.get_major_mapping()


InterviewSchedulePage
=====================

.. autoclass:: InterviewSchedulePage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, InterviewSchedulePage

    schedule_id = 452361

    with HandshakeBrowser(school_url, email) as browser:
        interview_page = InterviewSchedulePage(schedule_id, browser)
        contacts = interview_page.get_contacts()
        reserved_rooms = interview_page.get_reserved_rooms()


SurveyPage
==========

.. autoclass:: SurveyPage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, SurveyPage

    survey_id = 8279252
    download_dir = 'C:\\Users\\username\\Downloads\\'

    with HandshakeBrowser(school_url, email) as browser:
        survey = SurveyPage(survey_id, browser)
        filepath = survey.download_responses(download_dir)
        # do something with the downloaded file


CareerInterestsPage
===================

.. autoclass:: CareerInterestsPage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, ViewAsStudent, CareerInterestsPage

    student_id = 198427
    career_clusters = ['Finance Cluster', 'STEM Cluster']

    with HandshakeBrowser(school_url, email) as browser:
        with ViewAsStudent(student_id, browser):
            interests_page = CareerInterestsPage(student_id, browser)
            for cluster in career_clusters:
                interests_page.select_cluster_by_name(cluster)
            interests_page.save_interests()


WaitingRoomPage
===================

.. autoclass:: WaitingRoomPage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, ViewAsStudent, CareerInterestsPage

    with HandshakeBrowser(school_url, email) as browser:
        waiting_room = WaitingRoomPage(browser)
        waiting_room_data = waiting_room.get_checkin_data()


EventsPage
==========

.. autoclass:: EventsPage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, EventsPage

    saved_search = 'This is a Case Sensitive Saved Search Name'
    download_dir = 'C:\\Users\\username\\Downloads\\'

    with HandshakeBrowser(school_url, email) as browser:
        events_page = EventsPage(browser)
        events_page.load_saved_search(saved_search)
        filepath = events_page.download_event_data(download_dir, wait_time=500)
        # do something with the downloaded file


LabelSettingsPage
=================

.. autoclass:: LabelSettingsPage
    :members:

Example
-------
::

    from autohandshake import HandshakeBrowser, LabelSettingsPage

    with HandshakeBrowser(school_url, email) as browser:
        label_settings_page = LabelSettingsPage(browser)
        label_data = label_settings_page.get_label_data()
        # do something with label data
