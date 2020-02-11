from tkinter import *

# root widget has to go first
root = Tk()


# Creating a Label Widget
myLabel = Label(root, text="Hellow World!")
# Positioning widget to screen using pack
myLabel.pack()

root.mainloop()


# NOTES
# need to define and put it on the screen
# many ways to put widgets into the screen
# pack
# a GUI is always on a loop. Programs are always on a constant loop
# when using pack, the widget stays the same when resizing the window

