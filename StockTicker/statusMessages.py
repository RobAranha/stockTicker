import smtplib
import numpy as np
from email.message import EmailMessage
from datetime import datetime, timedelta


def get_local_pass(path):
    password = np.loadtxt(path, dtype=str).tolist()
    return password


def check_email_updates(data):
    new_status = False
    my_email = "StockTicker@Outlook.com"
    message = ""
    percent_upswing = 0.05

    for i in range(len(data[0])):
        print(data[2][i])
        stock_open = float(data[1][i]) - float(data[2][i])
        if float(data[2][i]) / stock_open >= percent_upswing:
            new_status = True
            message = message + "Stock: " + str(data[0][i]) + ", Open: " + str(stock_open) + ", Change: " + str(data[2][i]) + ", (" + str(round(float(data[2][i]) / stock_open* 100, 5)) + "%)\n"

    if new_status:
        print("new status update!")
        new_status = False
        if datetime.now() >= check_email_updates.last_email_time + check_email_updates.email_wait_time and datetime.now().hour >= 9 and datetime.now().hour <= 16:
            print("New Email!", message)
            check_email_updates.last_email_time = datetime.now()
            send_email(my_email, my_email, str(percent_upswing * 100) + "% Stock Jump", message)
    else:
        print("no status updates to share based on a", percent_upswing, "upswing")


def send_email(to_address, from_address, subject, message):
    # Set up email server connection
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.ehlo()
    server.starttls()

    # Log in
    username = "StockTicker@Outlook.com"
    password = get_local_pass(r"C:\Users\robbi\Desktop\temp\myPass.txt")
    print(server.login(username, password))

    # Build email and ser parameters
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(message)

    #Send email
    server.send_message(msg)
    server.quit()