from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkintertable import TableCanvas, TableModel
import sqlite3
import pandas as pd
import numpy as np
import math
import datetime
from manual_functions import get_avg_manual_data
from noon_functions import get_avg_noon_data
from testing_functions import get_avg_testing_data

# constants
manual_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV_Before(V)', 'OCV_After(V)', 'SCC_Before(A)', 'SCC_After(A)', 'EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'EDS_PR_Before', 'EDS_PR_After', 'EDS_SR_Before', 'EDS_SR_After']
noon_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV(V)', 'SCC(A)', 'Power(W)', 'PR', 'SR']
testing_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV_Before(V)', 'OCV_After(V)', 'SCC_Before(A)', 'SCC_After(A)', 'CTRL1_OCV(V)', 'CTRL1_SCC(A)', 'CTRL2_OCV(V)', 'CTRL2_SCC(A)', 'EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'CTRL1_PWR(W)', 'CTRL2_PWR(W)']

root = Tk()
root.title("EDS Data Analysis Tool")
root.geometry("1100x550")
#root.grid_columnconfigure(1,weight=1)
#root.grid_rowconfigure(1,weight=1)
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
    global mode
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

# function to update the table
def get_table():
    # get the average day number
    global window
    window = avg_entry.get()
    # check which mode selected
    if mode == 'manual_data.csv':
        man_df = get_avg_manual_data(manual_cols_list, int(window))
        x = man_df.to_csv("manual_sorted.csv")
        table.importCSV("manual_sorted.csv")
    elif mode == "noon_data.csv":
        man_df = get_avg_noon_data(noon_cols_list, int(window))
        x = man_df.to_csv("noon_sorted.csv")
        table.importCSV("noon_sorted.csv")
    elif mode == "testing_data.csv":
        man_df = get_avg_testing_data(testing_cols_list, int(window))
        x = man_df.to_csv("testing_sorted.csv")
        table.importCSV("testing_sorted.csv")
    # clear the entry field
    avg_entry.delete(0, END)

# labels for Application Title
title_label = Label(root, text="EDS DATA ANALYSIS TOOL", font=("Helvetica", 18))
title_label.grid(row=0, column=3, padx=10, pady=15)
bu_label = Label(root, text="BOSTON UNIVERSITY", font=("Arial", 12))
bu_label.grid(row=1, column=3, padx=10)

# instructions label
ins_label = Label(root, text="How To Use:",font=("Arial", 11) )
ins_label.grid(row=2, column=3,padx=15, pady=60, sticky=W+N)
ins1_label = Label(root, text=" 1. Select the CSV File",font=("Arial", 10))
ins1_label.grid(row=2, column=3, padx=15, pady=90, sticky=W+N)
ins2_label = Label(root, text=" 2. Select the average days to sort the data",font=("Arial", 10))
ins2_label.grid(row=2, column=3, padx=15, pady=120, sticky=W+N)
ins3_label = Label(root, text=" 3. Observe result or plot",font=("Arial", 10))
ins3_label.grid(row=2, column=3, padx=15, pady=150, sticky=W+N)

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

# label to get average day input
avg_label = Label(root, text="Average Days: ",font=("Arial", 11))
avg_label.grid(row=2, column=3, padx=15, pady=21, sticky=W+N)

# entry field for average day input
avg_entry = Entry(root, width= 35)
avg_entry.grid(row=2, column=3,pady=22, sticky=N+E)

# create button to update the table
table_btn = Button(root, text="Get Table", command=get_table, borderwidth=1.4, relief="solid", width=20, height=3)
table_btn.grid(row=2, column=3, padx=15, pady=100, sticky=W+S)

# create frame for the table
tframe = Frame(root)
tframe.grid(row=2, column=0, columnspan=3, padx=10,pady=20)

# insert the csv table
table = TableCanvas(tframe)
table.thefont = ('Arial',9)
table.show()
'''
man_df = get_avg_manual_data(manual_cols_list, 10)
x = man_df.to_csv("manual_sorted.csv")
table.importCSV("manual_sorted.csv")
table.show()
'''


root.mainloop()
