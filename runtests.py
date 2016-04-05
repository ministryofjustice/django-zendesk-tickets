#!/usr/bin/env python
import argparse
import os
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner

DEFAULT_SETTINGS = dict(
    DEBUG=True,
    SECRET_KEY='a' * 24,
    ROOT_URLCONF='zendesk_tickets.tests.urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'zendesk_tickets',
    ),
    MIDDLEWARE_CLASSES=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ],
    SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [],
            'loaders': ['zendesk_tickets.tests.DummyTemplateLoader']
        },
    }],
    ZENDESK_BASE_URL='https://test.notzendesk.com',
    ZENDESK_API_USERNAME='zendesk_user',
    ZENDESK_API_TOKEN='api_token',
    ZENDESK_REQUESTER_ID=111111,
    ZENDESK_GROUP_ID=222222,
    ZENDESK_CUSTOM_FIELDS={
        'referer': 31,
        'username': 32,
        'user_agent': 33,
        'contact_email': 34
    }
)


def runtests():
    if 'setup.py' in sys.argv:
        # allows `python setup.py test` as well as `./runtests.py`
        sys.argv = ['runtests.py']

    parser = argparse.ArgumentParser()
    parser.add_argument('test_labels', nargs='*', default=['zendesk_tickets.tests'])
    parser.add_argument('--verbosity', type=int, choices=list(range(4)), default=1)
    parser.add_argument('--noinput', dest='interactive',
                        action='store_false', default=True)
    args = parser.parse_args()
    test_labels = args.test_labels

    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    django.setup()

    failures = DiscoverRunner(verbosity=args.verbosity, interactive=args.interactive,
                              failfast=False).run_tests(test_labels)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
