import yfinance as yf
import numpy as np
import threading
from datetime import datetime, timedelta
from pandas_datareader import data as pdr



def get_stock_splits(stock_sym, years):
    stock = yf.Ticker(stock_sym)
    now = datetime.now() - timedelta(days=years * 365)
    data = stock.splits
    stock_splits = []
    for name in data.index:
        if name > now:
            temp = []
            temp.append(str(name).split(" ")[0])
            temp.append(data[name])
            stock_splits.append(temp)
    return stock_splits


def get_stock_dividends(stock_sym, years):
    stock = yf.Ticker(stock_sym)
    now = datetime.now() - timedelta(days=years * 365)
    data = stock.dividends
    stock_dividends = []
    for name in data.index:
        if name > now:
            temp = []
            temp.append(str(name).split(" ")[0])
            temp.append(data[name])
            stock_dividends.append(temp)
    return stock_dividends


def get_stock_earnings(stock_sym):
    stock = yf.Ticker(stock_sym)
    data = stock.calendar
    return str(data[len(data.columns) - 1][0]).split(" ")[0]


def convert(lst):
    return ' '.join(lst)


def get_stock_data_year(stock):
    # set date range for api pull
    data = np.array([])
    now = datetime.now()
    last_day = now - timedelta(days=365)

    # fetch a dataframe from Yahoo finance apifor stock from lastDay to now
    df = pdr.get_data_yahoo(stock, last_day, now)
    rows = len(df.index)
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # add adjusted close for each day in the past year
    for row in df.iterrows():
        data = np.append(data, row[1].Adj_Close)

    return data


def get_high_low_vol(stock):
    data = get_stock_data_year(stock)
    #Based on 252 trading days in a year and 21 trading days in a month
    data_month = data[231:]
    data_three_month = data[189:]

    high = round(np.amax(data), 2)
    low = round(np.amin(data), 2)
    std_month = round(np.std(data_month), 5)
    std_three_month = round(np.std(data_three_month), 5)
    std_year = round(np.std(data), 5)

    return [low, high, std_month, std_three_month, std_year]


def parse_date(val, stock):
    val = val[len(stock):len(stock) + 8]
    year = val[:2]
    month = val[2:4]
    day = val[4:6]
    return( "20" + year + "-" + month + "-" + day)

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


def get_stock_options2(stock_sym):
    stock = yf.Ticker(stock_sym)
    data = stock.options
    threads = []
    options = []
    for option in data:
        process_thread = threading.Thread(target=thread_get_option_chain, args=(option, stock_sym, options,))
        threads.append(process_thread)
        process_thread.start()

    for t in threads:
        t.join()
    return options


#print(get_stock_splits("AAPL", 10))
#print(get_stock_dividends("AAPL", 5))
#print(get_stock_earnings("AAPL"))
print(get_stock_options("AAPL"))
print(get_stock_options2("AAPL"))
#print(get_stock_data_year(["AAPL"]))
#print(get_high_low_vol("AAPL"))

#val = "200828"
#print(parse_date(val))

# fetch a dataframe from Yahoo finance apifor stock from lastDay to now
#df = pdr.get_data_yahoo(stock_sym, last_day, now)
#print(df)

#options = stock.options

#for option in options:
#    print(stock.option_chain(option))