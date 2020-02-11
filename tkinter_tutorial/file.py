from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

root = Tk()


def open():
    global my_image
    root.filename = filedialog.askopenfilename(initialdir=".", title="Select A File", filetypes=(("png files", "*.png"),("all files", "*.*")))
    my_label = Label(root, text=root.filename).pack()
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    Label(image=my_image).pack()

my_btn = Button(root, text="Open File", command=open).pack()

root.mainloop()

#NOTES
# root.filename gives the path by using filedialog
