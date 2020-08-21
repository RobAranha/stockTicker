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
import tkinter as tk
import ctypes
from StockTicker.DataFetcher import pull_ticker_list
from StockTicker.DataFetcher import remove_ticker
from StockTicker.DataFetcher import add_ticker
from StockTicker.AdvancedMenu import open_adv_menu


def openMenu(root):
    class StockMenu(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            # load ticker_list data
            self.ticker_list = pull_ticker_list()
            # if indiviudal string is imported, convert to array
            if not isinstance(self.ticker_list, list):
                new_arr = [self.ticker_list]
                self.ticker_list = new_arr

            # set size and position
            user32 = ctypes.windll.user32
            height = 85 + len(self.ticker_list) * 25
            screen_size = '135x' + str(height)
            screen_position = '+' + str(user32.GetSystemMetrics(0) - 145) + '+' + str(
                user32.GetSystemMetrics(1) - height - 95)
            self.geometry(screen_size + screen_position)

            self.winfo_toplevel().title("Menu")

            # Build header information
            input_label = tk.Label(self, text="Ticker Symbol:")
            self.input_box = tk.Entry(self, width=10)
            my_button = tk.Button(self, text="Add Ticker", command=lambda: self.add_ticker(root))
            input_label.grid(row=0, column=0)
            self.input_box.grid(row=1, column=0)
            my_button.grid(row=2, column=0)
            self.bind("<Return>", (lambda event: self.add_ticker(root)))

            advanced_button = tk.Button(self, text="Adv.", command=lambda: self.open_advanced())
            advanced_button.grid(row=1, column=1)

            self.stocks = {}
            self.del_buttons = {}

            # update menu
            self.update_display(root)


        # clears all ticker symbols from menu
        def clear(self):
            for x in self.grid_slaves():
                if int(x.grid_info()["row"]) > 2:
                    x.grid_forget()


        # deletes a single symbol at given row
        def del_stock(self, row, root):
            remove_ticker(self.ticker_list[row])
            del self.ticker_list[row]
            self.update_display(root)  # update list
            root.refresh_data()


        # clears all ticker symbols, adds all symbols stored in ticker_list to menu, and resizes menu
        def update_display(self, root):
            # clear all symbols
            self.clear()

            # add symbols stored in ticker_list
            for x in range(len(self.ticker_list)):
                # add symbol
                new_stock = tk.Label(self, text=self.ticker_list[x])
                self.stocks[x] = new_stock
                self.stocks[x].grid(row=x + 3, column=0)
                # add delete button
                del_button = tk.Button(self, text="Remove", command=lambda row=x: self.del_stock(row, root))
                self.del_buttons[x] = del_button
                self.del_buttons[x].grid(row=x + 3, column=1)

            # resize menu for new row
            user32 = ctypes.windll.user32
            height = 80 + len(self.ticker_list) * 25
            screen_size = '135x' + str(height)
            screen_position = '+' + str(user32.GetSystemMetrics(0) - 145) + '+' + str(
                user32.GetSystemMetrics(1) - height - 95)
            self.geometry(screen_size + screen_position)


        # get user input from inputBox, add ticker symbol to ticker_list, and save data
        def add_ticker(self, root):
            # get input from textbox
            ticker = self.input_box.get()

            # add symbol to ticker list if not blank or already in ticker list
            if ticker != "" and ticker not in self.ticker_list:
                self.ticker_list.append(ticker)
                self.input_box.delete(0, tk.END)
                # update menu
                self.update_display(root)
                # save ticker_list data
                add_ticker(ticker)
                # Refresh Data
                root.refresh_data()

        def open_advanced(self):
            open_adv_menu()

    app = StockMenu()
    app.mainloop()
