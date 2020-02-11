from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="Look! I clicked a Button!!")
    myLabel.pack()

# a button is a widget
myButton = Button(root, text="Click Me!", command=myClick,fg="blue",bg="white")

myButton.pack()

root.mainloop()

# NOTES
# bg does not work for mac
# bg is background color, fg is foreground color (font color)