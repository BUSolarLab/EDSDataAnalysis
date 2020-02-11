from tkinter import *
from PIL import ImageTk, Image


root = Tk()
root.geometry("400x400")

vertical = Scale(root, from_=0, to=200)
vertical.pack()

horizontal = Scale(root, from_=0, to=200, orient=HORIZONTAL)
horizontal.pack()

def slide():
    my_label = Label(root, text=horizontal.get()).pack()
    root.geometry(str(horizontal.get())+"x"+ str(vertical.get()))





my_btn = Button(root, text="Click Me!", command=slide).pack()

root.mainloop()

#NOTES
# default slider is vertical