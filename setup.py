import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-zendesk-tickets',
    version='0.3',
    packages=['zendesk_tickets'],
    include_package_data=True,
    license='MIT License',
    description='',
    long_description=README,
    install_requires=['Django>=1.8', 'requests', ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Python Developers',
    ],
    test_suite='runtests.runtests'
)
