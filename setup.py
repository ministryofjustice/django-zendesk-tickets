import importlib
import os
import sys

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

__version__ = importlib.import_module('zendesk_tickets').__version__
with open('README.rst') as readme:
    README = readme.read()

tests_require = ['flake8>=2.5,<3.0']
if sys.version_info < (3, 3):
    tests_require.append('mock>=1.3')

setup(
    name='django-zendesk-tickets',
    version=__version__,
    author='Ministry of Justice Digital Services',
    url='https://github.com/ministryofjustice/django-zendesk-tickets',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    license='MIT',
    description='Django views and forms that submit tickets to Zendesk',
    long_description=README,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['Django>=1.9,<1.10', 'requests', 'six'],
    tests_require=tests_require,
    test_suite='runtests.runtests',
)
