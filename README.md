# AutoHandshake

[![Documentation Status](https://readthedocs.org/projects/autohandshake/badge/?version=latest)](https://autohandshake.readthedocs.io/en/latest/?badge=latest)

## Installation
```pip install autohandshake```

## Summary
A library for automating tasks on the Handshake career services platform.

Current functionality includes the automation of:

* Getting data from Insights
* Getting a complete record of your school's appointment type settings
* Getting a complete record of your school's major mappings
* Getting unfilled appointment slot data from the appointment calendar
* Getting account access request data

Typical usage looks like:
```python
#!/usr/bin/env python

from autohandshake import HandshakeSession, InsightsPage

school_url = 'https://jhu.joinhandshake.com'

with HandshakeSession(login_url=school_url, email=your_email, password=your_password) as browser:
    insights = InsightsPage(link_to_insights_report, browser)
    report_data = insights.get_data()
```

**Important**: this package relies on an automated driver for Google Chrome, so users must have Chrome installed in order to use this package.

## Documentation
You will find complete documentation at [the Read the Docs site](https://autohandshake.readthedocs.io/en/latest/).