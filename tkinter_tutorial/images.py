from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Tkinter Tutorials")

# using icons
#root.iconbitmap('./cake.png')

# using images
my_img = ImageTk.PhotoImage(Image.open("./images/cake.png"))
my_label = Label(image = my_img)
my_label.pack()

# exit button
button_quit = Button(root, text="Exit Program", command=root.quit)
button_quit.pack()



root.mainloop()

#NOTES
# built in image import, only GIF and PIN bla bla
# so neel PIL, Python Image Library, or PILLOW
