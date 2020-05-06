from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Populate long description from README
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'StockTicker',
    version = '1.0.0',
    description = 'Add stock ticker above desktop tool bar',
    long_description = long_description,
    author = 'Robert Aranha',
    author_email = 'rearanha@uwaterloo.ca',
    license = 'GNU GPLv3',
    py_modules = ['DataFetcher', 'PickStocks'],
    packages = ['StockTicker'],
    install_requires = [
        'numpy',
        'yfinance',
        'pandas-datareader',
        'datetime'
    ]
)