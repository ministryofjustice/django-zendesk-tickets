import importlib
import os
import sys

from setuptools import setup

package_info = importlib.import_module('zendesk_tickets')
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

tests_require = ['flake8>=3.5,<4']
if sys.version_info < (3, 4):
    django_version = '>=1.10,<2'
    tests_require.append('mock>=2,<3')
else:
    django_version = '>=1.10,<2.1'

setup_extensions = importlib.import_module('zendesk_tickets.setup_extensions')

setup(
    name='django-zendesk-tickets',
    version=package_info.__version__,
    author=package_info.__author__,
    url='https://github.com/ministryofjustice/django-zendesk-tickets',
    packages=['zendesk_tickets'],
    include_package_data=True,
    license='MIT',
    description='Django views and forms that submit tickets to Zendesk',
    long_description=README,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass=setup_extensions.command_classes,
    install_requires=['Django%s' % django_version, 'requests', 'six'],
    tests_require=tests_require,
    test_suite='runtests.runtests',
)
