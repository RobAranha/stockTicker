from tkinter import *

master = Tk()
master.title("Login")




label = Label(master, text="Enter your username: ")
label.grid(row=0, column=0)


button = Button(master, text="Submit")
button.grid(row=0, column=1)

master.mainloop()
