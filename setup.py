#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020 Robert Aranha
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Populate long description from README
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='StockTicker',
    version='1.0.0',
    description='Simple stock ticker using tkinter and yfinance api',
    long_description=long_description,
    author='Robert Aranha',
    author_email='rearanha@uwaterloo.ca',
    url='https://github.com/RobAranha/stockTicker',
    license='Apache',
    python_requires='>=3.4',
    install_requires=[
        'certifi==2020.4.5.1',
        'chardet==3.0.4',
        'DateTime==4.3',
        'idna==2.9',
        'lxml==4.6.2',
        'multitasking==0.0.9',
        'numpy==1.18.4',
        'pandas==1.0.3',
        'pandas-datareader==0.8.1',
        'python-dateutil==2.8.1',
        'pytz==2020.1',
        'requests==2.23.0',
        'six==1.14.0',
        'urllib3==1.25.9',
        'yfinance==0.1.54',
        'zope.interface==5.1.0'
    ],
    classifiers = [
        'Development Status :: 4 -Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows :: Windows 10'
    ]
)
