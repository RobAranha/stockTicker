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

import smtplib
import numpy as np
from datetime import datetime
from email.message import EmailMessage
from StockTicker.AdvancedMenu import load_settings


# Get text from external file and return value
def get_local_pass(path):
    password = np.loadtxt(path, dtype=str).tolist()
    return password


# Check if an email should be sent based on email alert settings
def check_email_updates(data):
    # Fetch settings
    settings = load_settings()

    new_status = False
    message = ""
    percent_upswing = float(settings['upswing_threshold'])

    # Check for large upswings
    for i in range(len(data[0])):
        stock_open = float(data[1][i]) - float(data[2][i])
        if float(data[2][i]) / stock_open >= percent_upswing / 100:
            new_status = True
            message = message + "Stock: " + str(data[0][i]) + ", Open: " + str(stock_open) +\
                      ", Change: " + str(data[2][i]) + ", (" +\
                      str(round(float(data[2][i]) / stock_open* 100, 5)) + "%)\n"

    # Check for price targets
    targets = settings['price_target'].replace(" ", "")
    targets = targets.split(";")
    for i in range(len(targets)):
        targets[i] = targets[i].split(",")

    for i in range(len(targets)):
        if data[1][data[0].tolist().index(targets[i][0])] >= targets[i][1]:
            new_status = True
            message = message + "Stock: " + str(data[0][i]) + " is currently trading at : " +\
                      str(data[1][i]) + "\n"

    # Check if email should be sent
    if new_status:
        print("new status update!")
        if datetime.now() >= check_email_updates.last_email_time +\
                check_email_updates.email_wait_time and\
                datetime.now().hour >= int(settings['email_start_time']) and\
                datetime.now().hour <= int(settings['email_end_time']):
            print("New Email!", message)
            check_email_updates.last_email_time = datetime.now()
            send_email(settings, str(percent_upswing * 100) + "% Stock Jump", message)
    else:
        print("no status updates to share based on a", percent_upswing, "upswing")


# Send email using outlook email service
def send_email(settings, subject, message):
    # Set up email server connection
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.ehlo()
    server.starttls()

    # Log in
    username = settings['from_address']
    password = get_local_pass(settings['password_location'])
    server.login(username, password)

    # Build email and ser parameters
    msg = EmailMessage()
    msg['From'] = settings['from_address']
    msg['To'] = settings['to_address']
    msg['Subject'] = subject
    msg.set_content(message)

    # Send email
    server.send_message(msg)
    server.quit()