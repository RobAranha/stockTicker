import numpy as np
import tkinter as tk
import ctypes


def openMenu():
    class StockMenu(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            # load tickerList data
            self.file = 'data.txt'
            self.tickerList = np.loadtxt(self.file, dtype=str).tolist()
            # if indiviudal string is imported, convert to array
            if not isinstance(self.tickerList, list):
                newArr = [self.tickerList]
                self.tickerList = newArr

            # set size and position
            user32 = ctypes.windll.user32
            height = 80 + len(self.tickerList) * 21
            screenSize = '135x' + str(height)
            screenPosition = '+' + str(user32.GetSystemMetrics(0) - 145) + '+' + str(
                user32.GetSystemMetrics(1) - height - 95)
            self.geometry(screenSize + screenPosition)

            # Build header information
            inputLabel = tk.Label(self, text="Ticker Symbol:")
            self.inputBox = tk.Entry(self, width=10)
            myButton = tk.Button(self, text="Add Ticker", command=self.addTicker)
            inputLabel.grid(row=0, column=0)
            self.inputBox.grid(row=1, column=0)
            myButton.grid(row=2, column=0)
            self.bind("<Return>", (lambda event: self.addTicker()))

            self.stocks = {}
            self.delButtons = {}

            # update menu
            self.updateDisplay()

        # clears all ticker symbols from menu
        def clear(self):
            for x in self.grid_slaves():
                if int(x.grid_info()["row"]) > 2:
                    x.grid_forget()

        # deletes a single symbol at given row
        def delStock(self, row):
            del self.tickerList[row]
            self.updateDisplay()  # update list
            # noinspection PyTypeChecker
            np.savetxt(self.file, np.array(self.tickerList), fmt='%s')  # save data

        # clears all ticker symbols, adds all symbols stored in tickerList to menu, and resizes menu
        def updateDisplay(self):
            # clear all symbols
            self.clear()

            # add symbols stored in tickerList
            for x in range(len(self.tickerList)):
                # add symbol
                newStock = tk.Label(self, text=self.tickerList[x])
                self.stocks[x] = newStock
                self.stocks[x].grid(row=x + 3, column=0)
                # add delete button
                delButton = tk.Button(self, text="Remove", command=lambda row=x: self.delStock(row))
                self.delButtons[x] = delButton
                self.delButtons[x].grid(row=x + 3, column=1)

            # resize menu for new row
            user32 = ctypes.windll.user32
            height = 80 + len(self.tickerList) * 25
            screenSize = '135x' + str(height)
            screenPosition = '+' + str(user32.GetSystemMetrics(0) - 145) + '+' + str(
                user32.GetSystemMetrics(1) - height - 95)
            self.geometry(screenSize + screenPosition)

        # get user input from inputBox, add ticker symbol to tickerList, and save data
        def addTicker(self):
            # get input from textbox
            ticker = self.inputBox.get()

            # add symbol to ticker list if not blank or already in ticker list
            if ticker != "" and ticker not in self.tickerList:
                self.tickerList.append(ticker)
                self.inputBox.delete(0, tk.END)
                # update menu
                self.updateDisplay()

            # save tickerList to data file
            # noinspection PyTypeChecker
            np.savetxt(self.file, np.array(self.tickerList), fmt='%s')

    app = StockMenu()
    app.mainloop()