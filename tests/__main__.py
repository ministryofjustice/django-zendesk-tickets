import pathlib
import sys

if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.runner import DiscoverRunner

    tests_path = pathlib.Path(__file__).parent
    root_path = tests_path.parent

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
            'DIRS': [tests_path / 'templates'],
            'APP_DIRS': True,
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

    if not settings.configured:
        settings.configure(**test_settings)
        django.setup()

    test_runner = DiscoverRunner(verbosity=2, failfast=False, interactive=False, top_level=root_path)
    version_message = f'Testing on django {django.__version__}'
    if hasattr(test_runner, 'log'):
        test_runner.log(version_message)
    else:
        print(version_message, file=sys.stderr)
    failures = test_runner.run_tests(['tests'])
    sys.exit(failures)
