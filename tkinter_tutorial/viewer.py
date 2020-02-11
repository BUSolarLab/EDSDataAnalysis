from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Tkinter Tutorials")

# using icons
#root.iconbitmap('./cake.png')

# get images
my_img1 = ImageTk.PhotoImage(Image.open("./images/cake.png"))
my_img2 = ImageTk.PhotoImage(Image.open("./images/cake2.png"))
my_img3 = ImageTk.PhotoImage(Image.open("./images/cake3.png"))
my_img4 = ImageTk.PhotoImage(Image.open("./images/cake4.png"))
my_img5 = ImageTk.PhotoImage(Image.open("./images/cake5.png"))

# compile to a list
image_list = [my_img1, my_img2, my_img3, my_img4, my_img5]

# display to screen
my_label = Label(image = my_img1)
my_label.grid(row=0, column=0, columnspan=3)

def forward(image_number):
    global my_label
    global button_forward
    global button_back
    # delete current picture
    my_label.grid_forget()
    # display new image
    my_label = Label(image = image_list[image_number-1])
    my_label.grid(row=0, column=0, columnspan=3)
    # re define button
    button_forward = Button(root, text=">>", command= lambda: forward(image_number+1))
    button_back = Button(root, text="<<", command = lambda: back(image_number-1))

    if image_number == 5:
        button_forward = Button(root, text=">>", state = DISABLED)
    # re display buttons
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)



def back(image_number):
    global my_label
    global button_forward
    global button_back
    # delete current picture
    my_label.grid_forget()
    # display new image
    my_label = Label(image = image_list[image_number-1])
    my_label.grid(row=0, column=0, columnspan=3)
    # re define button
    button_forward = Button(root, text=">>", command= lambda: forward(image_number+1))
    button_back = Button(root, text="<<", command = lambda: back(image_number-1))
    if image_number == 1:
        button_back = Button(root, text="<<", state = DISABLED)
    # re display buttons
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)

# create buttons
button_back = Button(root, text="<<", command= back, state=DISABLED)
button_exit = Button(root, text="Exit Program", command=root.quit)
button_forward = Button(root, text=">>",  command= lambda: forward(2))

# display to screen
button_back.grid(row=1, column=0)
button_exit.grid(row=1, column=1)
button_forward.grid(row=1, column=2)


root.mainloop()

#NOTES
# built in image import, only GIF and PIN bla bla
# so neel PIL, Python Image Library, or PILLOW
