import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner

test_settings = dict(
    DEBUG=True,
    SECRET_KEY='a' * 50,
    ROOT_URLCONF='tests.urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'zendesk_tickets',
    ),
    MIDDLEWARE=[
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
            'loaders': ['tests.utils.DummyTemplateLoader'],
        },
    }],
    ZENDESK_BASE_URL='https://zendesk.local/',
    ZENDESK_API_USERNAME='zendesk_user',
    ZENDESK_API_TOKEN='api_token',
    ZENDESK_REQUESTER_ID=111111,
    ZENDESK_GROUP_ID=222222,
    ZENDESK_CUSTOM_FIELDS={
        'referer': 31,
        'username': 32,
        'user_agent': 33,
        'contact_email': 34,
    },
)


def run():
    if not settings.configured:
        settings.configure(**test_settings)
        django.setup()
    failures = DiscoverRunner(verbosity=2, failfast=False, interactive=False).run_tests(['tests'])
    sys.exit(failures)


if __name__ == '__main__':
    run()
