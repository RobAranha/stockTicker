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

import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import sqlite3 as sql
from StockTicker.statusMessages import check_email_updates
from pandas_datareader import data as pdr

import os
import time

yf.pdr_override()

def convert(lst):
    return ' '.join(lst)

# pulls data[Ticker symbol, market price, daily change] for selected
# stock and appends to data array
def get_stock_data(stock, data):
    # set date range for api pull
    now=datetime.now()
    if (datetime.today().weekday() == 6):        # if sunday, pull data for last 48 hours
        last_day = now - timedelta(hours=48)
    else:
        last_day = now - timedelta(hours=24)

    # fetch a dataframe from Yahoo finance apifor stock from lastDay to now

    df = pdr.get_data_yahoo(convert(stock), last_day, now)
    rows = len(df.index)
    # Change how data is being returned to be more fluent
    stock_close = np.zeros(len(stock))
    stock_open = np.zeros(len(stock))
    for col in df:
        #print(df.columns.get_loc(col))
        if col[0] == "Adj Close":
            stock_close[stock.index(col[1])] = df[col].tolist()[rows - 1]
        if col[0] == "Open":
            stock_open[stock.index(col[1])] = df[col].tolist()[rows - 1]

    stock_diff = np.subtract(stock_close, stock_open)
    # Round to 2 decimals
    stock_close = np.around(stock_close, decimals=2)
    stock_diff = np.around(stock_diff, decimals=2)
    # Append to data array
    data = np.array([stock,stock_close,stock_diff])

    return data


def set_directory():
    # Set working directory to read in data file ...StockTicker\
    abspath = os.path.abspath(__file__)
    directory = os.path.dirname(abspath).rpartition("\\")[0]
    os.chdir(directory)


def remove_ticker(sym):
    set_directory()

    connection = sql.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("DELETE from data WHERE Ticker='" + sym + "'")
    connection.commit()
    connection.close()


def add_ticker(sym):
    set_directory()

    connection = sql.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data VALUES ('" + sym + "');")
    connection.commit()
    connection.close()


# Returns a list of all ticker symbols in data.db
def pull_ticker_list():
    set_directory()

    # get ticker list from saved data file, load to tickerList
    connection = sql.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Data")
    ans = list(cursor.fetchall())
    ticker_list = [list(i) for i in ans]
    ticker_list = np.ndarray.flatten(np.array(ticker_list)).tolist()
    connection.close()

    return ticker_list

# Returns an array of stock data for all ticker symbols in data.txt
def get_all_stock_data():
    ticker_list = pull_ticker_list()
    data = np.array([[],[],[]])             #[Ticker symbol, market price, daily change]
    check_email_updates.email_wait_time = timedelta(hours=1)
    count = 0
    # Loop through each element in tickerList,
    # pulling market information and filling data array
    if isinstance(ticker_list, list):
        data = get_stock_data(ticker_list, data)
    else:
        data = get_stock_data(ticker_list, data)

    try:
        check_email_updates.last_email_time
    except:
        check_email_updates.last_email_time = datetime.now() - check_email_updates.email_wait_time
    check_email_updates(data)
    print(data)
    return data
