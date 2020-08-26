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

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import ctypes
import threading
from StockTicker.DataFetcher import get_stock_splits
from StockTicker.DataFetcher import get_stock_dividends
from StockTicker.DataFetcher import get_stock_earnings
from StockTicker.DataFetcher import get_stock_options
from StockTicker.DataFetcher import get_high_low_vol
from StockTicker.AdvancedMenu import load_settings
from StockTicker.DataFetcher import get_time

font = font_header = ("Arial", 12, "bold")
font_label = ("Arial", 12)


def open_details(stock):
    class details(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            # Set size and position
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            screen_size = '700x460'
            screen_position = '+' + str(int(screen_width / 3)) + '+' + str(int(screen_height / 5))
            self.geometry(screen_size + screen_position)
            self.winfo_toplevel().title(stock + " - Details")

            # Build canvas objects
            self.header = tk.Label(self, text=stock, font=font_header, width=20, anchor='w')
            self.label_earnings = tk.Label(self, text="Earnings Release: Loading",
                                           font=font_label, width=66, anchor='w')
            self.label_dividends = tk.Label(self, text="Dividends: Loading ",
                                            font=font_label, width=66, anchor='w')
            self.label_splits = tk.Label(self, text="Splits: Loading", font=font_label,
                                         justify=tk.LEFT, width=66, anchor='w')
            self.label_options = tk.Label(self, text="Option Quotes: Loading", font=font_header)
            self.high_low = tk.Label(self, text="Low/High: Loading", font=font_header, width=20,
                                     anchor="e")

            self.frame_vol = tk.Frame(self)
            self.label_vol_week = tk.Label(self.frame_vol, text="Std (1 week): Loading",
                                           font=font_label, width=20, anchor='w')
            self.label_vol_month = tk.Label(self.frame_vol, text="Std (1 month): Loading",
                                            font=font_label, width=20, anchor='w')
            self.label_vol_year = tk.Label(self.frame_vol, text="Std (1 year): Loading",
                                           font=font_label, width=20, anchor='w')

            self.label_vol_week.pack(side=tk.LEFT, anchor='w')
            self.label_vol_month.pack(side=tk.LEFT, anchor='w')
            self.label_vol_year.pack(side=tk.LEFT, anchor='w')

            # Build Options Window
            self.my_fram = tk.Frame(self)
            self.options = ttk.Treeview(self.my_fram)  # , width='86', height='15')
            options_scroll_bar = tk.Scrollbar(self.my_fram, orient="vertical",
                                              command=self.options.yview)
            options_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
            self.options.config(yscrollcommand=options_scroll_bar.set)

            # Set table columns
            self.options_data = []
            columns = ["Expiration", "Type", "Strike", "Last Price", "Bid", "Ask", "Change",
                       "% Change",
                       "Volume", "Open Interest", "Implied Vol"]
            self.options["columns"] = columns
            for i in range(1, len(columns) + 1):
                self.options.heading("#" + str(i), text=columns[i - 1])
                self.options.column("#" + str(i), width=50)
            self.options.column("#0", width=0)
            self.options.column("#1", width=75)
            self.options.column("#4", width=60)
            self.options.column("#8", width=65)
            self.options.column("#10", width=80)
            self.options.column("#11", width=90)

            # Temporary tree view to maintain canvas size during updates
            self.temp_options = ttk.Treeview(self.my_fram)
            self.temp_options.pack(side=tk.LEFT, fill=tk.Y)
            self.temp_options["columns"] = columns
            for i in range(1, len(columns) + 1):
                self.temp_options.heading("#" + str(i), text=columns[i - 1])
                self.temp_options.column("#" + str(i), width=50)
            self.temp_options.column("#0", width=0)
            self.temp_options.column("#1", width=75)
            self.temp_options.column("#4", width=60)
            self.temp_options.column("#8", width=65)
            self.temp_options.column("#10", width=80)
            self.temp_options.column("#11", width=90)

            # Build objects for option filters
            self.frame_filters = tk.Frame(self)
            self.label_type_filter = tk.Label(self.frame_filters, text="Type", width=4,
                                              font=font_label)
            self.input_type_filter = tk.Entry(self.frame_filters, width=12)
            self.label_date_filter = tk.Label(self.frame_filters, text="   Exp. Date", width=10,
                                              font=font_label)
            self.input_date_filter = tk.Entry(self.frame_filters, width=12)
            self.label_strike_filter = tk.Label(self.frame_filters, text="   Strike Price",
                                                width=11, font=font_label)
            self.input_strike_filter = tk.Entry(self.frame_filters, width=12)
            self.button_filter = tk.Button(self, text="Filter", width=12, font=font_label,
                                           anchor='center', command=lambda: self.filter_options())
            self.label_type_filter.pack(side=tk.LEFT, anchor='w')
            self.input_type_filter.pack(side=tk.LEFT, anchor='w')
            self.label_date_filter.pack(side=tk.LEFT, anchor='w')
            self.input_date_filter.pack(side=tk.LEFT, anchor='w')
            self.label_strike_filter.pack(side=tk.LEFT, anchor='w')
            self.input_strike_filter.pack(side=tk.LEFT, anchor='w')

            # Place objects in window
            self.header.grid(row=0, column=0, columnspan=2)
            self.high_low.grid(row=0, column=4, columnspan=3)
            self.label_earnings.grid(row=1, column=0, columnspan=6, pady=(5, 0))
            self.label_dividends.grid(row=2, column=0, columnspan=6)
            self.label_splits.grid(row=3, column=0, columnspan=6)
            self.frame_vol.grid(row=4, column=0, columnspan=6, pady=(5, 0))

            self.label_options.grid(row=5, column=0, columnspan=6, pady=(5, 0))
            self.my_fram.grid(row=6, column=0, columnspan=6, padx=(10, 0))

            self.frame_filters.grid(row=7, column=0, columnspan=6)

            self.button_filter.grid(row=8, column=0, columnspan=6, pady=(5, 0))
            self.bind("<Return>", (lambda event: self.filter_options()))

            process_thread = threading.Thread(target=self.thread_get_options, args=(stock,))
            process_thread.start()
            process_thread = threading.Thread(target=self.thread_get_stock_data, args=(stock,))
            process_thread.start()
            process_thread = threading.Thread(target=self.thread_get_earnings, args=(stock,))
            process_thread.start()
            process_thread = threading.Thread(target=self.thread_get_dividends, args=(stock,))
            process_thread.start()
            process_thread = threading.Thread(target=self.thread_get_splits, args=(stock,))
            process_thread.start()

            settings = load_settings()
            self.time = get_time() + 1000
            self.option_time = 0
            self.refresh_time = int(settings['update_frequency']) * 1000
            self.options_refresh_time = int(settings['option_update_frequency']) * 1000

            self.refresh()

        def refresh(self):
            if self.option_time > self.options_refresh_time:
                self.label_options.config(text="Option Quotes - Refreshing")
                process_thread = threading.Thread(target=self.thread_get_options, args=(stock,))
                process_thread.start()
                self.option_time = 0
            else:
                self.option_time = self.option_time + 15
            if self.time > self.refresh_time:
                process_thread = threading.Thread(target=self.thread_get_stock_data, args=(stock,))
                process_thread.start()
                self.time = 0
            else:
                self.time = self.time + 15
            self.after(15, self.refresh)

        def filter_options(self):
            type_filter = self.input_type_filter.get()
            date_filter = self.input_date_filter.get()
            strike_filter = self.input_strike_filter.get()
            data_subset = []
            settings = load_settings()

            # Remove data from old tree
            self.options.delete(*self.options.get_children())

            # Build subset of new data
            for i in range(len(self.options_data)):
                if ((date_filter == "" or date_filter == self.options_data[i][0]) and
                        (type_filter == "" or type_filter == self.options_data[i][1]) and
                        (strike_filter == "" or int(strike_filter) == int(self.options_data[i][2]))):
                    data_subset.append(self.options_data[i])

            # Write new data to treeview
            for i in range(len(data_subset)):
                if not (np.isnan(data_subset[i][8])) and \
                        not (np.isnan(data_subset[i][9])) and \
                        int(data_subset[i][8]) >= int(settings["min_volume"]) and \
                        int(data_subset[i][9]) >= int(settings["min_open_interest"]):
                    self.options.insert("", tk.END, values=data_subset[i])

        def thread_get_stock_data(self, stock):
            try:
                stock_data = get_high_low_vol(stock)
                current = stock_data[0]
                last_change = stock_data[1]
                high_low = stock_data[2] + "/" + stock_data[3]
                vol_week = stock_data[4]
                vol_month = stock_data[5]
                vol_year = stock_data[6]
            except:
                current = "N/A"
                last_change = "N/A"
                high_low = "No Data Found"
                vol_week = "No Data Found"
                vol_month = "No Data Found"
                vol_year = "No Data Found"
            self.header.config(text=stock + " : " + current + " : " + last_change)
            self.high_low.config(text="Low/High: " + high_low)
            self.label_vol_week.config(text="Vol (1 week): " + vol_week)
            self.label_vol_month.config(text="Vol (1 month): " + vol_month)
            self.label_vol_year.config(text="Vol (1 year): " + vol_year)

        def thread_get_earnings(self, stock):
            try:
                earnings = get_stock_earnings(stock)
            except:
                earnings = "No Data Found"
            self.label_earnings.config(text="Earnings Release: " + earnings)

        def thread_get_dividends(self, stock):
            try:
                dividends = get_stock_dividends(stock)
            except:
                dividends = "No Data Found"
            self.label_dividends.config(text="Dividends: " + dividends)

        def thread_get_splits(self, stock):
            try:
                splits = get_stock_splits(stock)
            except:
                splits = "No Data Found"
            self.label_splits.config(text="Splits: " + splits)

        def thread_get_options(self, stock):
            # Fill objects for options
            try:
                self.options_data = get_stock_options(stock)
                self.temp_options.pack()
                self.options.pack_forget()
                self.filter_options()
                self.options.pack()
                self.temp_options.pack_forget()
                self.label_options.config(text="Option Quotes")
            except:
                self.label_options.config(text="Option Quotes: No Data Found")

    app = details()
    app.mainloop()
