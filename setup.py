#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0',
'astroid>=1.5.3',
'autopep8>=1.3.3',
'branca>=0.3.0',
'certifi>=2017.7.27.1',
'chardet>=3.0.4',
'click>=6.7',
'colorama>=0.4.0',
'cssselect>=1.0.1',
'decorator>=4.1.2',
'dicttoxml>=1.7.4',
'folium>=0.6.0',
'geocoder>=1.32.1',
'geographiclib>=1.49',
'geoip2>=2.6.0',
'geopy>=1.17.0',
'idna>=2.6',
'ip2geotools>=0.1.3',
'IP2Location>=8.0.0',
'isort>=4.2.15',
'Jinja2>=2.10',
'lazy-object-proxy>=1.3.1',
'lxml>=4.1.0',
'MarkupSafe>=1.0',
'maxminddb>=1.3.0',
'mccabe>=0.6.1',
'numpy>=1.15.3',
'packaging>=16.8',
'pip-review>=1.0',
'pycodestyle>=2.3.1',
'pylint>=1.7.4',
'pyparsing>=2.2.0',
'pyquery>=1.3.0',
'ratelim>=0.1.6',
'requests>=2.20.0',
'scipy>=1.1.0',
'six>=1.11.0',
'urllib3>=1.23',
'wrapt>=1.10.11',
 ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Oldřich Klíma",
    author_email='xklima27@vutbr.cz',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="An extension of the ip2geotools package that refines the estimation of the location of different geolocation databases using statistical methods.",
    entry_points={
        'console_scripts': [
            'ip2geotools_locator=ip2geotools_locator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ip2geotools_locator',
    name='ip2geotools_locator',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Ionicson/ip2geotools-locator',
    version='1.1.2',
    zip_safe=False,
)
