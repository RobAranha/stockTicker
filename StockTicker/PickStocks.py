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
import ctypes
from StockTicker.DataFetcher import pull_ticker_list
from StockTicker.DataFetcher import remove_ticker
from StockTicker.DataFetcher import add_ticker
from StockTicker.AdvancedMenu import open_adv_menu
from StockTicker.Details import open_details

# Opens the menu when the menu button is pressed in the ticker tape
def open_menu(root):
    class StockMenu(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            # Load ticker_list data
            self.ticker_list = pull_ticker_list()
            # if indiviudal string is imported, convert to array
            if not isinstance(self.ticker_list, list):
                new_arr = [self.ticker_list]
                self.ticker_list = new_arr
            self.winfo_toplevel().title("menu")

            # Build header information
            input_label = tk.Label(self, text="Ticker Symbol:")
            self.input_box = tk.Entry(self, width=10)
            my_button = tk.Button(self, text="Add Ticker", command=lambda: self.add_ticker(root))
            input_label.grid(row=0, column=0)
            self.input_box.grid(row=1, column=0)
            my_button.grid(row=2, column=0)
            self.bind("<Return>", (lambda event: self.add_ticker(root)))

            advanced_button = tk.Button(self, text="Advanced", command=lambda: self.open_advanced())
            advanced_button.grid(row=1, column=1, columnspan=2)

            self.stocks = {}
            self.del_buttons = {}
            self.detail_buttons = {}

            # Update menu
            self.update_display(root)

        # Clears all ticker symbols from menu
        def clear(self):
            for x in self.grid_slaves():
                if int(x.grid_info()["row"]) > 2:
                    x.grid_forget()

        # Deletes a single symbol at given row
        def del_stock(self, row, root):
            remove_ticker(self.ticker_list[row])
            del self.ticker_list[row]
            self.update_display(root)  # update list
            root.refresh_data()

        # Opens the details menu for the selected stock
        def details(self, stock):
            open_details(stock)

        # Clears all ticker symbols, adds all symbols stored in ticker_list to menu, and resizes menu
        def update_display(self, root):
            # Clear all symbols
            self.clear()

            # Add symbols stored in ticker_list
            for x in range(len(self.ticker_list)):
                # Add symbol
                new_stock = tk.Label(self, text=self.ticker_list[x])
                self.stocks[x] = new_stock
                self.stocks[x].grid(row=x + 3, column=0)
                # Add delete button
                del_button = tk.Button(self, text="Remove", command=lambda row=x: self.del_stock(row, root))
                self.del_buttons[x] = del_button
                self.del_buttons[x].grid(row=x + 3, column=1)
                # Add details button
                detail_button = tk.Button(self, text="Details", command=lambda row=x: self.details(self.ticker_list[row]))
                self.detail_buttons[x] = detail_button
                self.detail_buttons[x].grid(row=x + 3, column=2)

            # Resize menu for new row
            user32 = ctypes.windll.user32
            height = 85 + len(self.ticker_list) * 25
            screen_size = '185x' + str(height)
            screen_position = '+' + str(user32.GetSystemMetrics(0) - 194) + '+' + str(
                user32.GetSystemMetrics(1) - height - 95)
            self.geometry(screen_size + screen_position)

        # Get user input from inputBox, add ticker symbol to ticker_list, and save data
        def add_ticker(self, root):
            ticker = self.input_box.get()

            # Add symbol to ticker list if not blank or already in ticker list
            if ticker != "" and ticker not in self.ticker_list:
                self.ticker_list.append(ticker)
                self.input_box.delete(0, tk.END)
                # update menu
                self.update_display(root)
                # save ticker_list data
                add_ticker(ticker)
                # Refresh Data
                root.refresh_data()

        # Opens the advanced menu
        def open_advanced(self):
            open_adv_menu()

    app = StockMenu()
    app.mainloop()
