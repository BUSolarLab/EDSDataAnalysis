from tkinter import *
from PIL import ImageTk, Image

root = Tk()

def open():
    global my_img
    top = Toplevel()
    my_img = ImageTk.PhotoImage(Image.open("images/cake.png"))
    my_label = Label(top, image=my_img).pack()
    btn2 = Button(top, text="close window", command=top.destroy).pack()


btn = Button(root, text="Open Second Window", command=open).pack()


#lbl = Label(top, text="Hellow World").pack()


root.mainloop()

#NOTES
# showinfo, showwarning, showerror, askquestion, askokcancel, askyesno