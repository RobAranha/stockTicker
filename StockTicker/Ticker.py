import sys
import ctypes
import tkinter as tk
from StockTicker.PickStocks import openMenu
from StockTicker.DataFetcher import getAllStockData


fontType = ("Arial", 12, "bold")

class TickerTape(tk.Tk):
    def __init__(self, data, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #set size and position
        user32 = ctypes.windll.user32
        screenSize = str(user32.GetSystemMetrics(0)) + 'x25'
        self.screenWidth = int(screenSize[0:4])
        screenPosition = '+0+' + str(user32.GetSystemMetrics(1) - 64)
        self.geometry(screenSize + screenPosition)
        self.canvas = tk.Canvas(self, width=self.screenWidth)

        #set background colors
        self.configure(background='purple4')
        self.canvas.configure(background='black')

        #disable resizing and window options (minimize, resize, close)
        self.resizable(0, 0)
        self.overrideredirect(1)

        #set movement speed in x and y direction, and time
        self.x = 2
        self.y = 0
        self.time = 0

        # set additional properties for data storage and ticker symbols
        self.data = data
        self.symbols = {}

        #add quit and menu button
        self.canvas.create_rectangle(self.screenWidth-39, 0, self.screenWidth, 22,
                                     outline="#33B5E5", fill="#33B5E5")
        quitButton = tk.Button(self.canvas, text="X", width=10, font="Arial, 12", command=self.quit)
        menuButton = tk.Button(self.canvas, text="!", width=10, font="Arial, 12", command=self.menu)
        # set button background color
        quitButton.configure(width=1, activebackground="#33B5E5")
        menuButton.configure(width=1, activebackground="#33B5E5")
        #add buttons to canvas
        quitButton_window = self.canvas.create_window(self.screenWidth - 9.5, 10, window=quitButton)
        menuButton_window = self.canvas.create_window(self.screenWidth - 29.5, 10, window=menuButton)

        # add canvas to tkinder window
        self.canvas.pack()

        # move symbols
        self.movement()


    # move ticker symbols, and reset position once offscreen
    def movement(self):
        # if symbols are added or removed fully reset ticker, else delay reset till ticker itteration ends
        if len(self.symbols) != len(self.data[0]):
            # remove all symbols
            for x in range(0, len(self.symbols)):
                self.canvas.delete(self.symbols[x].txt)
                self.symbols.pop(x)
            # Add new symbols
            for x in range(0, len(self.data[0])):
                symb = symbol(self.canvas, self, self.data[0, x], self.data[1, x], self.data[2, x], x)
                self.symbols[x] = symb
            self.canvas.place(x=1, y=1)

        # move individual ticker symbols and get coordinates
        for x in range(0, len(self.symbols)):
            self.canvas.move(self.symbols[x].txt, self.x, self.y)
            coor = str((self.canvas.coords(self.symbols[x].txt)))
            coor = int(coor[1:coor.index(".")])
            #remove ticker symbol once it goes off screen and add to begining of ticker list
            if coor > self.screenWidth + 200:
                self.canvas.delete(self.symbols[x].txt)
                self.symbols.pop(x)
                symb = symbol(self.canvas, self, self.data[0, x], self.data[1, x], self.data[2, x],
                              max(0, len(self.symbols) - self.screenWidth / 200))
                self.symbols[x] = symb

        # Refresh data every minute
        self.time = self.time + 50
        if self.time > 60000:
            self.data = getAllStockData()
            print("Refreshing")
            self.time = 0

        # call movement after delay
        self.after(50, self.movement)


    # functionality for quit button
    def quit(self):
        sys.exit()


    # functionality for menu button
    def menu(self):
        openMenu()


class symbol(tk.Frame):
    # build symbol, set position and text
    def __init__(self, parent, controller, symb, price, diff, count):
        tk.Frame.__init__(self,parent)
        self.xPos = -200 * count - 100
        self.txt = parent.create_text(self.xPos, 10, fill="white", font=fontType, width=200,
                                      text=symb + " : " + str(price) + " : " + str(diff))