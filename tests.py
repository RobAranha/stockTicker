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
import datetime as dt
from pandas_datareader import data as pdr


yf.pdr_override()

#pulls data[Ticker symbol, market price, daily change] for selected stock and appends to data array
def getStockData(stock, data):
    # set date range for api pull
    now=dt.datetime.now()
    if (dt.datetime.today().weekday() == 6):                           # if sunday, pull data for last 48 hours
        lastDay = now - dt.timedelta(hours=48)
    else:
        lastDay = now - dt.timedelta(hours=24)

    # fetch a dataframe from Yahoo finance api for stock from lastDay to now
    df = pdr.get_data_yahoo(stock, lastDay, now)
    df.insert(0, "Stock_Name", stock)
    df["Diff"] = df["Close"].sub(df["Open"], axis = 0)
    rows = len(df.index)

    # parse individual information for last row in data frame
    stockName = df.iloc[rows-1:rows, 0:1].values.flatten(order='C')
    stockClose = df.iloc[rows-1:rows, 4:5].values.flatten(order='C')
    stockDiff = df.iloc[rows - 1:rows, 7:8].values.flatten(order='C')

    # Round to 2 decimals
    stockClose = np.around(stockClose, decimals=2)
    stockDiff = np.around(stockDiff, decimals=2)

    # Append to data array
    newData = np.stack((stockName, stockClose, stockDiff))
    data = np.append(data, newData, axis=1)

    return data


#Returns an array of stock data for all ticker symbols in data.txt
def testStockData():
    # get ticker list from saved data file, load to tickerList
    tickerList = ['AAPL', 'AMD', 'NVDA']

    # data: [Ticker symbol, market price, daily change]
    data = np.array([[],[],[]])

    # Loop through each element in tickerList, pulling market information and filling data array
    if isinstance(tickerList, list):
       for x in tickerList:
            data = getStockData(x, data)
    else:
        data = getStockData(tickerList, data)

    return data

temp = testStockData()
print(temp)
