import os
import sys

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

tests_require = []
if sys.version_info < (3, 3):
    tests_require.append('mock>=1.3')

setup(
    name='django-zendesk-tickets',
    version='0.4',
    packages=['zendesk_tickets'],
    include_package_data=True,
    license='MIT License',
    description='',
    long_description=README,
    install_requires=['Django>=1.9', 'requests'],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Python Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='runtests.runtests',
    tests_require=tests_require,
)
