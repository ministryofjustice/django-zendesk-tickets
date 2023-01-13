#!/usr/bin/env python
import importlib
import os
import sys
import warnings

from setuptools import setup

if sys.version_info[0:2] < (3, 8):
    warnings.warn('This package is tested with Python version 3.8+')

root_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_path, 'README.rst')) as readme:
    README = readme.read()

setup_requires = ['Django>=2.2,<4.3']
install_requires = setup_requires + ['requests']
tests_require = []

package_info = importlib.import_module('zendesk_tickets')
setup_extensions = importlib.import_module('zendesk_tickets.setup_extensions')
command_classes = setup_extensions.command_classes.copy()

setup(
    name='django-zendesk-tickets',
    version=package_info.__version__,
    author=package_info.__author__,
    author_email='dev@digital.justice.gov.uk',
    url='https://github.com/ministryofjustice/django-zendesk-tickets',
    packages=['zendesk_tickets'],
    include_package_data=True,
    license='MIT',
    description='Django views and forms that submit tickets to Zendesk',
    long_description=README,
    keywords='zendesk django tickets',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    cmdclass=command_classes,
    python_requires='>=3.6',  # looser requirement than what's tested
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests.run',
)
