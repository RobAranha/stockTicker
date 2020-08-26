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
from StockTicker.AdvancedMenu import load_settings
from StockTicker.statusMessages import check_email_updates
from pandas_datareader import data as pdr
import os

yf.pdr_override()
time = 0


def convert(lst):
    return ' '.join(lst)


# pulls data[Ticker symbol, market price, daily change] for selected
# stock and appends to data array
def get_stock_data(stock):
    # set date range for api pull
    now=datetime.now()
    time_delay = 24
    if (now.weekday() == 5):        # if sunday, pull data for last 48 hours
       time_delay = time_delay + 24
    elif (now.weekday() == 0 or now.weekday() == 6 or (now.weekday() == 1 and now.time().hour <= 8)):  # if sunday, pull data for last 48 hours
       time_delay = time_delay + 48
    if now.time().hour >= 20 or now.time().hour <= 8:
        time_delay = time_delay + 24

    last_day = now - timedelta(hours=time_delay)

    # fetch a dataframe from Yahoo finance apifor stock from lastDay to now
    df = pdr.get_data_yahoo(convert(stock), last_day, now)
    rows = len(df.index)
    # Change how data is being returned to be more fluent
    stock_close = np.zeros(len(stock))
    stock_prev_close = np.zeros(len(stock))
    for col in df:
        if col[0] == "Adj Close" or col[0] == "A":
            stock_close[stock.index(col[1])] = df[col].tolist()[rows - 1]
            stock_prev_close[stock.index(col[1])] = df[col].tolist()[0]

    stock_diff = np.subtract(stock_close, stock_prev_close)
    # Round to 2 decimals
    stock_close = np.around(stock_close, decimals=2)
    stock_diff = np.around(stock_diff, decimals=2)
    # Append to data array
    data = np.array([stock,stock_close,stock_diff])

    return data


def get_stock_data_year(stock):
    # set date range for api pull
    data = np.array([])
    now = datetime.now()
    last_day = now - timedelta(days=365)

    # fetch a dataframe from Yahoo finance api for stock from lastDay to now
    df = pdr.get_data_yahoo(stock, last_day, now)
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # add adjusted close for each day in the past year
    for row in df.iterrows():
        data = np.append(data, row[1].Adj_Close)

    return data


def get_high_low_vol(stock):
    data = get_stock_data_year(stock)
    #Based on 252 trading days in a year, 21 trading days in a month and 5 trading days in a week
    data_week = data[247:]
    data_month = data[231:]

    current = round(data[len(data) - 1], 2)
    last_change = round(data[len(data) - 1] - data[len(data) - 2], 2)
    high = round(np.amax(data), 2)
    low = round(np.amin(data), 2)
    std_week = round(np.std(data_week), 5)
    std_month = round(np.std(data_month), 5)
    std_year = round(np.std(data), 5)

    return [str(current), str(last_change), str(low), str(high), str(std_week), str(std_month), str(std_year)]


# Returns an array of stock data for all ticker symbols in data.txt
def get_all_stock_data():
    ticker_list = pull_ticker_list()
    settings = load_settings()
    check_email_updates.email_wait_time = timedelta(minutes=int(settings['email_frequency']))

    # Loop through each element in tickerList,
    # pulling market information and filling data array
    if isinstance(ticker_list, list):
        data = get_stock_data(ticker_list)
    else:
        data = get_stock_data([ticker_list])

    # Check for email updates
    if settings['send_emails'] == "True":
        try:
            check_email_updates.last_email_time
        except:
            check_email_updates.last_email_time = datetime.now() - check_email_updates.email_wait_time
        check_email_updates(data)
    return data


def get_stock_splits(stock_sym):
    stock = yf.Ticker(stock_sym)
    data = stock.splits
    stock_splits = []
    return_val = ""
    count = 0

    for name in data.index:
        temp = []
        temp.append(str(name).split(" ")[0])
        temp.append(data[name])
        stock_splits.append(temp)

    for i in reversed(range(len(stock_splits))):
        return_val = return_val + str(stock_splits[i][0]) + ": " + str(stock_splits[i][1])
        count = count + 1
        if count == 3 or count == len(stock_splits):
            break
        return_val = return_val + " | "
    return return_val


def get_stock_dividends(stock_sym):
    stock = yf.Ticker(stock_sym)
    data = stock.dividends
    stock_dividends = []
    return_val = ""
    count = 0

    for name in data.index:
        temp = []
        temp.append(str(name).split(" ")[0])
        temp.append(data[name])
        stock_dividends.append(temp)

    for i in reversed(range(len(stock_dividends))):
        return_val = return_val + str(stock_dividends[i][0]) + ": " + str(stock_dividends[i][1])
        count = count + 1
        if count == 3 or count == len(stock_dividends):
            break
        return_val = return_val + " | "
    return return_val


def get_stock_earnings(stock_sym):
    stock = yf.Ticker(stock_sym)
    data = stock.calendar
    if len(data) == 1:
        return str(data[len(data.columns) - 1][0]).split(" ")[0]
    else:
        return(str(data[0][0]).split(" ")[0] + " - " + str(data[1][0]).split(" ")[0])



def parse_date(val, stock):
    val = val[len(stock):len(stock) + 8]
    year = val[:2]
    month = val[2:4]
    day = val[4:6]
    return "20" + year + "-" + month + "-" + day


def thread_get_option_chain(option, stock_sym, options):
    stock = yf.Ticker(stock_sym)
    for option in stock.option_chain(option):
        for row in option.iterrows():
            data_row = [parse_date(row[1].contractSymbol, stock_sym),
                        row[1].contractSymbol[len(stock_sym) + 6: len(stock_sym) + 7],
                        row[1].strike, row[1].lastPrice, row[1].bid, row[1].ask,
                        round(row[1].change, 4), round(row[1].percentChange, 4), row[1].volume,
                        row[1].openInterest, round(row[1].impliedVolatility, 4)]
            options.append(data_row)


def get_stock_options(stock_sym):
    stock = yf.Ticker(stock_sym)
    data = stock.options
    options_temp = []
    options = []
    for option in data:
        options_temp.append([stock.option_chain(option)])

    for option_set in options_temp:
        for option in option_set:
            for row in option[0].iterrows():
                data_row = [parse_date(row[1].contractSymbol, stock_sym),
                            row[1].contractSymbol[len(stock_sym) + 6: len(stock_sym) + 7],
                            row[1].strike, row[1].lastPrice, row[1].bid,
                            row[1].ask, row[1].change, row[1].percentChange, row[1].volume,
                            row[1].openInterest, round(row[1].impliedVolatility, 4)]
                options.append(data_row)

    return options


# Chnages the working directory to the current file directory
def set_directory():
    abspath = os.path.abspath(__file__)
    directory = os.path.dirname(abspath).rpartition("\\")[0]
    os.chdir(directory)


# Removes sym from the database file
def remove_ticker(sym):
    set_directory()

    connection = sql.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("DELETE from data WHERE Ticker='" + sym + "'")
    connection.commit()
    connection.close()


# Adds sym to the database file
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


def get_time():
    global time
    return time


def inc_time(val):
    global time
    time = time + val
