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
import json


font= font_header = ("Arial", 12, "bold")
font_label = ("Arial", 12)
settings_file = "settings.json"

# Loads settings from settings file
def load_settings():
    settings = open(settings_file)
    data = json.load(settings)
    settings.close()
    return data


def open_adv_menu():
    class adv_menu(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            #fetch settings data
            data = load_settings()

            #set size and position
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            screen_size = '450x615'
            screen_position = '+' + str(int(screen_width/2)) + '+' + str(int(screen_height / 8))
            self.geometry(screen_size + screen_position)
            self.winfo_toplevel().title("Advanced Menu")

            #Build canvas objects
            self.header = tk.Label(self, text="Advanced Menu", font= ("Arial", 14, "bold", "underline"))

            self.header_general_controls = tk.Label(self, text="General Controls", font= font_header)
            self.label_speed = tk.Label(self, text="Speed", font= font_label)
            self.input_speed = tk.Entry(self, width=10)
            self.label_update_frequency = tk.Label(self, text="Update Frequency (Seconds)", font= font_label)
            self.input_update_frequency = tk.Entry(self, width=10)
            self.label_send_emails = tk.Label(self, text="Send Emails (True/False)", font= font_label)
            self.input_send_emails = tk.Entry(self, width=10)
            self.label_ticker_colour = tk.Label(self, text="Ticker Colour (#XXXXXX)", font= font_label)
            self.input_ticker_colour = tk.Entry(self, width=10)
            self.label_ticker_background_colour = tk.Label(self, text="   Background Colour (#XXXXXX)   ", font= font_label)
            self.input_ticker_background_colour = tk.Entry(self, width=10)

            self.header_email_controls = tk.Label(self, text="Email Controls", font= font_header)
            self.label_from_address = tk.Label(self, text="From Address", font= font_label)
            self.input_from_address = tk.Entry(self, width=30)
            self.label_to_address = tk.Label(self, text="To Address", font= font_label)
            self.input_to_address = tk.Entry(self, width=30)
            self.label_password_location = tk.Label(self, text="Password Location", font= font_label)
            self.input_password_location = tk.Entry(self, width=30)
            self.label_email_frequency = tk.Label(self, text="Email Frequency (Minutes)", font= font_label)
            self.input_email_frequency = tk.Entry(self, width=10)
            self.label_email_start_time = tk.Label(self, text="Email Start Time (Hours)", font= font_label)
            self.input_email_start_time = tk.Entry(self, width=10)
            self.label_email_end_time = tk.Label(self, text="Email End Time (Hours)", font= font_label)
            self.input_email_end_time = tk.Entry(self, width=10)

            self.header_stock_details = tk.Label(self, text="Stock Details", font=font_header)
            self.label_min_option_vol = tk.Label(self, text="Min Option Volume", font=font_label)
            self.input_min_option_vol = tk.Entry(self, width=10)
            self.label_min_option_open_interest = tk.Label(self, text="Min Option Open Interest", font=font_label)
            self.input_min_option_open_interest  = tk.Entry(self, width=10)
            self.label_option_refresh = tk.Label(self, text="Option Refresh Time (Seconds)", font=font_label)
            self.input_option_refresh = tk.Entry(self, width=10)

            self.header_email_alerts = tk.Label(self, text="Email Alerts", font= font_header)
            self.label_upswing = tk.Label(self, text="Upswing Threashold (%)", font= font_label)
            self.input_upswing = tk.Entry(self, width=10)
            self.label_price_target = tk.Label(self, text="Price Target [S,#]", font= font_label)
            self.input_price_target = tk.Entry(self, width=30)

            self.save_button = tk.Button(self, text="Save", font=font_label, command=lambda: self.save())
            self.label_save_status= tk.Label(self, text="", font= font_header)

            #Fill canvas
            self.header.grid(row=0, column=1, columnspan=2)

            self.header_general_controls.grid(row=1, column=1, pady=(15,0))
            self.label_speed.grid(row=2, column=1)
            self.input_speed.grid(row=2, column=2)
            self.label_update_frequency.grid(row=3, column=1)
            self.input_update_frequency.grid(row=3, column=2)
            self.label_send_emails.grid(row=4, column=1)
            self.input_send_emails.grid(row=4, column=2)
            self.label_ticker_colour.grid(row=5, column=1)
            self.input_ticker_colour.grid(row=5, column=2)
            self.label_ticker_background_colour.grid(row=6, column=1)
            self.input_ticker_background_colour.grid(row=6, column=2)

            self.header_email_controls.grid(row=7, column=1, pady=(15,0))
            self.label_from_address.grid(row=8, column=1)
            self.input_from_address.grid(row=8, column=2)
            self.label_to_address.grid(row=9, column=1)
            self.input_to_address.grid(row=9, column=2)
            self.label_password_location.grid(row=10, column=1)
            self.input_password_location.grid(row=10, column=2)
            self.label_email_frequency.grid(row=11, column=1)
            self.input_email_frequency.grid(row=11, column=2)
            self.label_email_start_time.grid(row=12, column=1)
            self.input_email_start_time.grid(row=12, column=2)
            self.label_email_end_time.grid(row=13, column=1)
            self.input_email_end_time.grid(row=13, column=2)

            self.header_stock_details.grid(row=14, column=1, pady=(15,0))
            self.label_min_option_vol.grid(row=15, column=1)
            self.input_min_option_vol.grid(row=15, column=2)
            self.label_min_option_open_interest.grid(row=16, column=1)
            self.input_min_option_open_interest.grid(row=16, column=2)
            self.label_option_refresh.grid(row=17, column=1)
            self.input_option_refresh.grid(row=17, column=2)

            self.header_email_alerts.grid(row=18, column=1, pady=(15,0))
            self.label_upswing.grid(row=19, column=1)
            self.input_upswing.grid(row=19, column=2)
            self.label_price_target.grid(row=20, column=1)
            self.input_price_target.grid(row=20, column=2)

            self.label_save_status.grid(row=21, column=2, pady=(5, 0))
            self.save_button.grid(row=21, column=1, pady=(5, 0))

            #Fill settings data
            self.input_speed.insert(0, data['speed'])
            self.input_update_frequency.insert(0, data['update_frequency'])
            self.input_send_emails.insert(0, data['send_emails'])
            self.input_ticker_colour.insert(0, data['ticker_colour'])
            self.input_ticker_background_colour.insert(0, data['ticker_background_colour'])
            self.input_from_address.insert(0, data['from_address'])
            self.input_to_address.insert(0, data['to_address'])
            self.input_password_location.insert(0, data['password_location'])
            self.input_email_frequency.insert(0, data['email_frequency'])
            self.input_email_start_time.insert(0, data['email_start_time'])
            self.input_email_end_time.insert(0, data['email_end_time'])
            self.input_min_option_vol.insert(0, data['min_volume'])
            self.input_min_option_open_interest.insert(0, data['min_open_interest'])
            self.input_option_refresh.insert(0, data['option_update_frequency'])
            self.input_upswing.insert(0, data['upswing_threshold'])
            self.input_price_target.insert(0, data['price_target'])

        # Get values from all input boxes and save data to settings file
        def save(self):
            settings = open(settings_file, 'r')
            data = json.load(settings)
            settings.close()

            settings = open(settings_file, 'w')
            data['speed'] = self.input_speed.get()
            data['update_frequency'] = self.input_update_frequency.get()
            data['send_emails'] = self.input_send_emails.get()
            data['ticker_colour'] = self.input_ticker_colour.get()
            data['ticker_background_colour'] = self.input_ticker_background_colour.get()
            data['from_address'] = self.input_from_address.get()
            data['to_address'] = self.input_to_address.get()
            data['password_location'] = self.input_password_location.get()
            data['email_frequency'] = self.input_email_frequency.get()
            data['email_start_time'] = self.input_email_start_time.get()
            data['email_end_time'] = self.input_email_end_time.get()
            data['min_volume'] = self.input_min_option_vol.get()
            data['min_open_interest'] = self.input_min_option_open_interest.get()
            data['option_update_frequency'] = self.input_option_refresh.get()
            data['upswing_threshold'] = self.input_upswing.get()
            data['price_target'] = self.input_price_target.get()
            json.dump(data, settings)
            settings.close()

            self.label_save_status['text'] = ""
            self.label_save_status['text'] = "Save Successful"


    app = adv_menu()
    app.mainloop()
