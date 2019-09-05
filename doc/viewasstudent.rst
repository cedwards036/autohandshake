ViewAsStudent
================
.. module:: autohandshake
.. autoclass:: ViewAsStudent
    :members:

Example
-------
::

    from autohandshake import HandshakeSession, ViewAsStudent, CareerInterestsPage

    student_id = 198427
    career_clusters = ['Finance Cluster', 'STEM Cluster']

    with HandshakeSession(school_url, email) as browser:
        with ViewAsStudent(student_id, browser):
            interests_page = CareerInterestsPage(student_id, browser)
            for cluster in career_clusters:
                interests_page.select_cluster_by_name(cluster)
            interests_page.save_interests()