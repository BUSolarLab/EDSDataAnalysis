from tkinter import *
from PIL import ImageTk, Image


root = Tk()

def show():
    myLabel = Label(root, text=clicked.get()).pack()

clicked = StringVar()
clicked.set("Monday")

options = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

drop = OptionMenu(root, clicked, *options)
drop.pack()

myButton = Button(root, text="Show Selection", command=show).pack()

root.mainloop()

#NOTES
# also known as options menu
# clicked is the var
# options with * for the inputs of the dropdown

