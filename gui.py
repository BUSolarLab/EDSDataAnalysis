from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import sqlite3

root = Tk()
root.title("EDS Data Analysis Tool")
root.geometry("850x500")
#root.configure(background="white")

# function to get csv file path
def find_file():
    # clear the entry field
    file_entry.delete(0, END)
    # clear the color for the testing modes
    testing_label = Label(root, text="Testing Data", borderwidth=1.4, relief="solid", width=20, height=3)
    testing_label.grid(row=1, column=0, padx=18)
    manual_label = Label(root, text="Manual Data", borderwidth=1.4, relief="solid", width=20, height=3)
    manual_label.grid(row=1, column=1)
    noon_label = Label(root, text="Noon Data", borderwidth=1.4, relief="solid", width=20, height=3)
    noon_label.grid(row=1, column=2, padx=18)
    # get the path for the csv file
    root.filename = filedialog.askopenfilename(initialdir=".", title="Select A CSV File", filetypes=(("CSV Files", "*.csv"),("All Files", "*.*")))
    # insert the path to the entry field
    file_entry.insert(0, root.filename)
    # based on path, figure out which mode
    mode = root.filename.split("/")[-1]
    if mode == 'manual_data.csv':
        manual_label = Label(root, text="Manual Data", borderwidth=1.4, relief="solid", width=20, height=3, bg="green")
        manual_label.grid(row=1, column=1)
    elif mode == 'testing_data.csv':
        testing_label = Label(root, text="Testing Data", borderwidth=1.4, relief="solid", width=20, height=3, bg="green")
        testing_label.grid(row=1, column=0)
    elif mode == 'noon_data.csv':
        noon_label = Label(root, text="Noon Data", borderwidth=1.4, relief="solid", width=20, height=3, bg="green")
        noon_label.grid(row=1, column=2)


# labels for Application Title
title_label = Label(root, text="EDS DATA ANALYSIS TOOL", font=("Helvetica", 18))
title_label.grid(row=0, column=3, padx=10, pady=10)
bu_label = Label(root, text="BOSTON UNIVERSITY", font=("Arial", 10))
bu_label.grid(row=1, column=3, padx=10)

# labels for showing testing/manual/noon moode
testing_label = Label(root, text="Testing Data", borderwidth=1.4, relief="solid", width=20, height=3)
testing_label.grid(row=1, column=0, padx=18)
manual_label = Label(root, text="Manual Data", borderwidth=1.4, relief="solid", width=20, height=3)
manual_label.grid(row=1, column=1)
noon_label = Label(root, text="Noon Data", borderwidth=1.4, relief="solid", width=20, height=3)
noon_label.grid(row=1, column=2, padx=18)

# button to get the path of the data csv file
file_btn = Button(root, text="Find CSV File", command=find_file, borderwidth=2, relief="raised")
file_btn.grid(row=0,column=0, padx=10, pady=10)

# entry field to display path for data csv file
file_entry = Entry(root, width=45)
file_entry.grid(row=0, column=1, columnspan=2)


root.mainloop()
