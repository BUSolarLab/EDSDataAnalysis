from tkinter import *
from PIL import ImageTk, Image


root = Tk()

def show():
    myLabel = Label(root, text=var.get()).pack()


var = IntVar()

c = Checkbutton(root, text = "Check this box, I dare you!", variable=var)
c.pack()


myButton = Button(root, text="Show", command=show).pack()


root.mainloop()

#NOTES
# square boxes, on or off type of button
# when check box, value is either 0 or 1
# onvalue = "On"
# offvalue = "Off"
# if wanna use StringVar()
# c.deselect(), can deselect the check box by default