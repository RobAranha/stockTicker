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

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Populate long description from README
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='StockTicker',
    version='1.0.0',
    description='Add stock ticker above desktop tool bar',
    long_description=long_description,
    author='Robert Aranha',
    author_email='rearanha@uwaterloo.ca',
    license='GNU GPLv3',
    py_modules=['DataFetcher', 'PickStocks'],
    packages=['StockTicker'],
    install_requires=[
        'numpy',
        'yfinance',
        'pandas-datareader',
        'datetime'
    ]
)
