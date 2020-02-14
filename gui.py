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

# global variables

# header constants for the csv files
manual_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV_Before(V)', 'OCV_After(V)', 'SCC_Before(A)', 'SCC_After(A)', 'EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'EDS_PR_Before', 'EDS_PR_After', 'EDS_SR_Before', 'EDS_SR_After']
noon_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV(V)', 'SCC(A)', 'Power(W)', 'PR', 'SR']
testing_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV_Before(V)', 'OCV_After(V)', 'SCC_Before(A)', 'SCC_After(A)', 'CTRL1_OCV(V)', 'CTRL1_SCC(A)', 'CTRL2_OCV(V)', 'CTRL2_SCC(A)', 'EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'CTRL1_PWR(W)', 'CTRL2_PWR(W)']

root = Tk()
root.title("EDS Data Analysis Tool")
root.geometry("960x435")

# function to clear the mode buttons
def clear_mode_buttons():
    # clear the color for the testing modes
    testing_label = Label(root, text="Testing Data", borderwidth=1.4, relief="solid", width=18, height=3)
    testing_label.grid(row=1, column=0, padx=18)
    manual_label = Label(root, text="Manual Data", borderwidth=1.4, relief="solid", width=18, height=3)
    manual_label.grid(row=1, column=1)
    noon_label = Label(root, text="Noon Data", borderwidth=1.4, relief="solid", width=18, height=3)
    noon_label.grid(row=1, column=2, padx=18)

# function to specify output path
def select_output():
    # clear  entry fields
    out_entry.delete(0, END)
    # use filedialog to select output location
    out_dir = filedialog.askdirectory(initialdir=".",title="Select A Folder To Store Output")
    # insert to entry field
    out_entry.insert(0, out_dir)
    # store in location
    global output_loc
    output_loc = out_dir

# function to get csv file path
def find_file():
    # clear the entry field
    file_entry.delete(0, END)
    # clear the color for the testing modes
    clear_mode_buttons()
    # get the path for the csv file
    root.filename = filedialog.askopenfilename(initialdir=".", title="Select A CSV File", filetypes=(("CSV Files", "*.csv"),("All Files", "*.*")))
    # insert the path to the entry field
    file_entry.insert(0, root.filename)
    # based on path, figure out which mode
    global mode
    mode = root.filename.split("/")[-1]
    if mode == 'manual_data.csv':
        manual_label = Label(root, text="Manual Data", borderwidth=1.4, relief="solid", width=18, height=3, bg="green")
        manual_label.grid(row=1, column=1)
    elif mode == 'testing_data.csv':
        testing_label = Label(root, text="Testing Data", borderwidth=1.4, relief="solid", width=18, height=3, bg="green")
        testing_label.grid(row=1, column=0)
    elif mode == 'noon_data.csv':
        noon_label = Label(root, text="Noon Data", borderwidth=1.4, relief="solid", width=18, height=3, bg="green")
        noon_label.grid(row=1, column=2)

# function to update the table
def get_table():
    # get the average day number
    global window
    window = avg_entry.get()
    # check which mode selected
    if mode == 'manual_data.csv':
        man_df = get_avg_manual_data(manual_cols_list, int(window))
        output = output_loc+"/manual_sorted.csv"
        x = man_df.to_csv(output)
        table.importCSV(output)
    elif mode == "noon_data.csv":
        man_df = get_avg_noon_data(noon_cols_list, int(window))
        output = output_loc+"/noon_sorted.csv"
        x = man_df.to_csv(output)
        table.importCSV(output)
    elif mode == "testing_data.csv":
        man_df = get_avg_testing_data(testing_cols_list, int(window))
        output = output_loc+"/testing_sorted.csv"
        x = man_df.to_csv(output)
        table.importCSV(output)
    # clear the entry field
    avg_entry.delete(0, END)

# labels for Application Title
title_label = Label(root, text="EDS DATA ANALYSIS TOOL", font=("Helvetica", 20))
title_label.grid(row=0, column=3, padx=10,pady=15, sticky=W)
bu_label = Label(root, text="BOSTON UNIVERSITY", font=("Arial", 14))
bu_label.grid(row=1, column=3, padx=10,sticky=W)

# instructions label
ins_label = Label(root, text="How To Use:",font=("Arial", 13))
ins_label.grid(row=2, column=3,padx=10, pady=120, sticky=N+W)
ins_label1 = Label(root, text=" 1. Select the CSV File To Analyze",font=("Arial", 11))
ins_label1.grid(row=2, column=3, padx=10, pady=150, sticky=W+N)
ins_label2 = Label(root, text=" 2. Select Output File Location",font=("Arial", 11))
ins_label2.grid(row=2, column=3, padx=10, pady=180, sticky=W+N)
ins_label3 = Label(root, text=" 3. Click Table Button",font=("Arial", 11))
ins_label3.grid(row=2, column=3, padx=10, pady=210, sticky=W+N)
ins_label4 = Label(root, text=" 4. Plot Metrics",font=("Arial", 11))
ins_label4.grid(row=2, column=3, padx=10, pady=240, sticky=W+N)

# labels for showing testing/manual/noon moode
clear_mode_buttons()

# button to get the path of the data csv file
file_btn = Button(root, text="Find CSV File", command=find_file, borderwidth=2, relief="raised")
file_btn.grid(row=0,column=0, padx=20, pady=20, sticky=W)

# entry field to display path for data csv file
file_entry = Entry(root, width=40)
file_entry.grid(row=0, column=1, columnspan=2, padx=2, sticky=W)

# create label for output path
out_btn = Button(root, text="Select Output Location", command=select_output, borderwidth=2, relief="raised")
out_btn.grid(row=2, column=0, padx=20, pady=202,sticky=S+W)

# entry field for the output path
out_entry = Entry(root, width=40)
out_entry.grid(row=2, column=1, columnspan=2, padx=5,pady=200, sticky=S+W)

# label to get average day input
avg_label = Label(root, text="Average Days: ",font=("Arial", 14))
avg_label.grid(row=2, column=3, padx=10, pady=21, sticky=W+N)

# entry field for average day input
avg_entry = Entry(root, width= 25)
avg_entry.grid(row=2, column=3,padx=120, pady=19, sticky=N+W)

# create button to update the table
table_btn = Button(root, text="Get Table", command=get_table, font=("Arial", 14),borderwidth=1.4, relief="solid", width=18, height=3)
table_btn.grid(row=2, column=3, padx=10, pady=60, sticky=N+W)

# create button to plot the table
plot_btn = Button(root, text="Plot Table", command=get_table, font=("Arial", 14),borderwidth=1.4, relief="solid", width=18, height=3)
plot_btn.grid(row=2, column=3, padx=200, pady=60, sticky=N)

# create radio button for plotting
plot_mode = StringVar()
plot_mode.set("Power")
radio_btn1 = Radiobutton(root, text="Power", variable=plot_mode, value="Power")
radio_btn1.grid(row=2, column=3, sticky=N+W, pady=120, padx=200)
radio_btn2 = Radiobutton(root, text="PR", variable=plot_mode, value="PR")
radio_btn2.grid(row=2, column=3, sticky=N+W, pady=150, padx=200)
radio_btn3 = Radiobutton(root, text="SR", variable=plot_mode, value="SR")
radio_btn3.grid(row=2, column=3, sticky=N+W, pady=180, padx=200)
radio_btn4 = Radiobutton(root, text="Soiling Rate", variable=plot_mode, value="Soiling Rate")
radio_btn4.grid(row=2, column=3, sticky=N+W, pady=210, padx=200)

# create frame for the table
tframe = Frame(root)
tframe.grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky=N)

# insert the csv table
table = TableCanvas(tframe)
table.thefont = ('Arial',10)
table.show()

root.mainloop()
