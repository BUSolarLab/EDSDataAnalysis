from tkinter import *

# root widget has to go first
root = Tk()


# Creating a Label Widget
myLabel1 = Label(root, text="Hello World!")
myLabel2 = Label(root, text="My name is John Elder!")

# Positioning widget to screen using grid
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=5)

root.mainloop()


# NOTES
# grid system positioning, has rows and columns
# when resizing windows, the widget does not change position, it stays

