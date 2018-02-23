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

    from zendesk_tickets import views

    url(r'^submit_ticket/$', views.TicketView.as_view(
        success_url='/',
        template_name='app_name/submit_ticket_page.html',
        ticket_subject='Website Feedback',
        ticket_tags=['website', 'feedback']
        ticket_template_name='app_name/feedback_ticket.txt',
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

.. image:: https://travis-ci.org/ministryofjustice/django-zendesk-tickets.svg?branch=master
    :target: https://travis-ci.org/ministryofjustice/django-zendesk-tickets

Please report bugs and open pull requests on `GitHub`_.

Use ``python setup.py test`` to run all tests.

If any localisable strings change, run ``python setup.py makemessages compilemessages``.

Distribute a new version to `PyPi`_ by updating the ``VERSION`` tuple in ``zendesk_tickets`` and
run ``python setup.py compilemessages sdist bdist_wheel upload``.


Copyright
---------

Copyright (C) 2018 HM Government (Ministry of Justice Digital Services).
See LICENSE.txt for further details.

.. _Zendesk: https://developer.zendesk.com/rest_api
.. _GitHub: https://github.com/ministryofjustice/django-zendesk-tickets
.. _PyPi: https://pypi.org/project/django-zendesk-tickets/
