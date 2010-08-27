#!/usr/bin/python
#
# Copyright 2010 Anthony Campbell (anthonycampbell.co.uk)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Required imports
from setuptools import setup, find_packages

__author__ = "Anthony Campbell (anthonycampbell.co.uk)"
__date__ = "$25-Aug-2010 00:46:21$"

# Define classifiers
CLASSIFIERS = [
    'Intended Audience :: End Users/Desktop',
    'Development Status :: 3 - Alpha',
    'Environment :: Plugins',
    'Topic :: Utilities',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Natural Language :: English',
    'Programming Language :: Python']

# Set additional attributes
long_description = open('README.txt').read() + open('CHANGES.txt').read()

# Setup
setup (
    # Package
    name = 'phosort',
    version = '1.0.7',
    packages = find_packages(),

    # Package dependencies
    install_requires=[
        'hachoir-core >= 1.3.3',
        'hachoir-parser >= 1.3.4',
        'hachoir-metadata >= 1.3.3'
    ],

    # PyPI egg details
    author = 'Anthony Campbell (anthonycampbell.co.uk)',
    author_email = 'acampbell3000 [[at] googlemail [dot]] com',
    summary = 'Simple script to sort a directory of photos and videos.',
    url = 'http://pypi.python.org/pypi/phosort',
    download_url = 'http://pypi.python.org/pypi/phosort#downloads',
    license = 'License :: OSI Approved :: Apache Software License',
    long_description = long_description,
    classifiers = CLASSIFIERS,
)

