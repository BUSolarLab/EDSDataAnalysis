from tkinter import *

root = Tk()

e = Entry(root, width=50)
e.pack()
e.insert(0, "Enter Your Name: ")

def myClick():
    myLabel = Label(root, text= e.get())
    myLabel.pack()

# a button is a widget
myButton = Button(root, text="Enter Your Name!", command=myClick)

myButton.pack()

root.mainloop()

# NOTES
# bg does not work for mac
# bg is background color, fg is foreground color (font color)
# can put default text in text box using insert