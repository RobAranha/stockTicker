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

import sys
import ctypes
import threading
import tkinter as tk
from StockTicker.PickStocks import open_menu
from StockTicker.DataFetcher import get_all_stock_data
from StockTicker.AdvancedMenu import load_settings

font_type = ("Arial", 12, "bold")


class min_button(tk.Tk):
    def __init__(self, tape, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set size and position
        user32 = ctypes.windll.user32
        screen_size = str(user32.GetSystemMetrics(0)) + 'x25'
        self.screen_width = int(screen_size[0:4])
        self.geometry("22x22+" + str(self.screen_width - 22) + "+" +
                      str(user32.GetSystemMetrics(1) - 64))
        self.canvas = tk.Canvas(self, width="15", height="22")

        # Set background colors
        self.configure(background='purple4')
        self.canvas.configure(background='black')

        # Disable resizing and window options (minimize, resize, close)
        self.resizable(0, 0)
        self.overrideredirect(1)

        # Add max button
        max_button = tk.Button(self.canvas, text="+", width=10,
                               font="Arial, 12", command=lambda: tape.max(tape))
        max_button.configure(width=1, activebackground="#33B5E5")
        self.canvas.create_window(10, 10,
                                  window=max_button)
        self.canvas.pack()


class ticker_tape(tk.Tk):
    def __init__(self, data, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Fetch settings data
        settings = load_settings()

        # Set size and position
        user32 = ctypes.windll.user32
        screen_size = str(user32.GetSystemMetrics(0)) + 'x25'
        self.screen_width = int(screen_size[0:4])
        screen_position = '+0+' + str(user32.GetSystemMetrics(1) - 64)
        self.geometry(screen_size + screen_position)
        self.canvas = tk.Canvas(self, width=self.screen_width)

        # Set background colors
        self.configure(background='purple4')
        self.canvas.configure(background=settings['ticker_background_colour'])

        # Disable resizing and window options (minimize, resize, close)
        self.resizable(0, 0)
        self.overrideredirect(1)
        self.attributes("-topmost", True)

        # Set movement speed in x and y direction, time, and update frequency
        self.x = float(settings['speed'])
        self.update_frequency = float(settings['update_frequency']) * 1000
        self.y = 0
        self.time = 0

        # Set additional properties for data storage and ticker symbols
        self.data = data
        self.symbols = {}

        # Add quit and menu button
        quit_button = tk.Button(self.canvas, text="X", width=10, font="Arial, 12", command=self.quit)
        menu_button = tk.Button(self.canvas, text="!", width=10, font="Arial, 12", command=self.menu)
        min_button = tk.Button(self.canvas, text="-", width=10, font="Arial, 12", command=self.min)
        # Set button background color
        quit_button.configure(width=1, activebackground="#33B5E5")
        menu_button.configure(width=1, activebackground="#33B5E5")
        min_button.configure(width=1, activebackground="#33B5E5")
        # Add buttons to canvas
        self.canvas.create_window(self.screen_width - 10, 10, window=quit_button)
        self.canvas.create_window(self.screen_width - 29, 10, window=menu_button)
        self.canvas.create_window(self.screen_width - 48, 10, window=min_button)

        # Add canvas to tkinder window
        self.canvas.pack()

        # Move symbols
        self.movement()


    # Move ticker symbols, and reset position once offscreen
    def movement(self):
        # If symbols are added/removed fully reset ticker, else delay reset till ticker itteration ends
        if len(self.symbols) != len(self.data[0]):
            # Remove all symbols
            for x in range(0, len(self.symbols)):
                self.canvas.delete(self.symbols[x].txt)
                self.symbols.pop(x)
            # Add new symbols
            for x in range(0, len(self.data[0])):
                symb = symbol(self.canvas, self, self.data[0, x], self.data[1, x], self.data[2, x], x)
                self.symbols[x] = symb
            self.canvas.place(x=1, y=1)

        # Move individual ticker symbols and get coordinates
        for x in range(0, len(self.symbols)):
            self.canvas.move(self.symbols[x].txt, self.x, self.y)
            coor = str((self.canvas.coords(self.symbols[x].txt)))
            coor = int(coor[1:coor.index(".")])
            # Remove ticker symbol once it goes off screen and add to begining of ticker list
            if coor > self.screen_width + 200:
                self.canvas.delete(self.symbols[x].txt)
                self.symbols.pop(x)
                symb = symbol(self.canvas, self, self.data[0, x], self.data[1, x], self.data[2, x],
                              max(0, len(self.symbols) - self.screen_width / 200))
                self.symbols[x] = symb

        # Refresh data on time interval
        self.time = self.time + 15
        if self.time >  self.update_frequency:
            self.refresh_data()

        # Call movement after delay
        self.after(15, self.movement)


    # Refresh all data in second thread and update symbols
    def thread_second(self):
        self.data = get_all_stock_data()
        for i in range(len(self.symbols)):
            stock = self.canvas.itemcget(self.symbols[i].txt, 'text')
            stock = stock.replace(" ", "").split(":")
            sym = stock[0]
            current = self.data[1][self.data[0].tolist().index(stock[0])]
            change = self.data[2][self.data[0].tolist().index(stock[0])]
            val = sym + " : " + current + " : " + change
            self.canvas.itemconfig(self.symbols[i].txt, text=val)


    # Functionality for stock data refresh
    def refresh_data(self):
        # Call function to refresh data as a subprocess
        print("Refreshing")
        process_thread = threading.Thread(target=self.thread_second)
        process_thread.start()
        # Reset time for next update
        self.time = 0


    # Functionality for quit button
    def quit(self):
        sys.exit()


    # Functionality for menu button
    def menu(self):
        open_menu(self)

    # Hide ticker tape
    def min(self):
        self.withdraw()
        temp = min_button(self)

    # Unhide ticker tape
    def max(self, ticker):
        ticker.deiconify()


class symbol(tk.Frame):
    # build symbol, set position and text
    def __init__(self, parent, controller, symb, price, diff, count):
        settings = load_settings()
        tk.Frame.__init__(self,parent)

        # Set symbol starting position and value
        self.xPos = -200 * count - 100
        self.txt = parent.create_text(self.xPos, 10, fill=settings['ticker_colour'], font=font_type,
                                      width=200, text=symb + " : " + str(price) + " : " + str(diff))