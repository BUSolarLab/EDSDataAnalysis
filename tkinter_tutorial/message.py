from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()

def popup():
    response = messagebox.askyesno("This is my Popup!", "Hello World!")
    Label(root, text=response).pack()
    if response == 1:
        Label(root, text="You Clicked Yes!").pack()
    else:
        Label(root, text="You Clicked No!").pack()


Button(root, text="Popup", command=popup).pack()

root.mainloop()

#NOTES
# showinfo, showwarning, showerror, askquestion, askokcancel, askyesno