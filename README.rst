Django Zendesk Tickets
======================

An extensible library to add Django views with forms to submit tickets to `Zendesk`_.

Usage
-----

Add these to your ``settings.py``:

.. code-block:: python

    ZENDESK_BASE_URL = 'https://example.zendesk.com'
    ZENDESK_API_USERNAME = ...
    ZENDESK_API_TOKEN = ...
    ZENDESK_REQUESTER_ID = ...
    ZENDESK_GROUP_ID = ...

Add an entry to your urls.py

.. code-block:: python

    from zendesk_tickets.views import TicketView

    path(r'submit-ticket/$', TicketView.as_view(
        success_url='/',
        template_name='app_name/submit-ticket-page.html',
        ticket_subject='Website Feedback',
        ticket_tags=['website', 'feedback']
        ticket_template_name='app_name/feedback-ticket.txt',
    ), name='submit_ticket'),

If you wish to include additional fields, subclass ``BaseTicketForm`` and
add them. If you wish to include them in the body of the ticket, create a new
ticket template and pass it as the ``ticket_template_name``. If you wish
to include them as custom fields, define the following in your ``settings.py``:

.. code-block:: python

    ZENDESK_CUSTOM_FIELDS = {
        'referer': 31,  # zendesk field id
        'username': 32,
        'user_agent': 33,
    }

The three fields in the example above are included in ``TicketForm`` by
default and can be included in your ticket by referencing them in the ticket
template or specifying custom field ids in settings.

Development
-----------

.. image:: https://github.com/ministryofjustice/django-zendesk-tickets/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/ministryofjustice/django-zendesk-tickets/actions/workflows/test.yml

.. image:: https://github.com/ministryofjustice/django-zendesk-tickets/actions/workflows/lint.yml/badge.svg?branch=main
    :target: https://github.com/ministryofjustice/django-zendesk-tickets/actions/workflows/lint.yml

Please report bugs and open pull requests on `GitHub`_.

Use ``python setup.py test`` to run all tests.

If any localisable strings change, run ``python setup.py makemessages compilemessages``.

Distribute a new version to `PyPi`_ by updating the ``VERSION`` tuple in ``zendesk_tickets/__init__.py`` and
publishing a release in GitHub (this triggers a GitHub Actions workflow to automatically upload it).
Alternatively, run ``python setup.py compilemessages sdist bdist_wheel upload`` locally.
Remember to update `History`_.


History
-------

0.16
    Drop support for python 3.6 and 3.7.
    Add support for python 3.11.
    Add experimental support for Django versions 4.0 & 4.1.
    Improve testing and linting.

0.15
    Add support for python 3.9 and 3.10.
    Improve testing and linting.

0.14
    Drop support for python 3.5.
    Improve linting.

0.13
    Drop python 2 support (now compatible with 3.5 - 3.8).
    Support Django 2.2 - 3.2 (both LTS).

0.12
    Improve testing and linting.

0.11
    Support Django 1.10 - 2.0.
    Add class-based Django views.
    Add internationalisation support.

0.10
    Fix display of tickets in Zendesk.

0.9
    Don’t allow self-referential return-to URL.

0.8
    Accept extra template context in views.

0.7
    Use email address of logged-in user when available.

0.6
    Collect email address of form submitter, optionally.

0.5
    Fix bugs.

0.4
    Provide a safe "return back to where you came from" link.

0.3
    Add success view.

0.2
    Fix bugs.

0.1
    Original release.

Copyright
---------

Copyright (C) 2023 HM Government (Ministry of Justice Digital & Technology).
See LICENSE.txt for further details.

.. _Zendesk: https://developer.zendesk.com/rest_api
.. _GitHub: https://github.com/ministryofjustice/django-zendesk-tickets
.. _PyPi: https://pypi.org/project/django-zendesk-tickets/
