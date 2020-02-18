from tkinter import *
from scipy import stats
from tkinter import filedialog
from tkintertable import TableCanvas, TableModel
import sqlite3
import pandas as pd
import numpy as np
import math
import datetime
from manual_functions import get_avg_manual_data, read_data
from noon_functions import get_avg_noon_data
from testing_functions import get_avg_testing_data
import matplotlib.pyplot as plt

# global variables
global soiling_rate
soiling_rate = ""
mode = ""

# header constants for the csv files
manual_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV_Before(V)', 'OCV_After(V)', 'SCC_Before(A)', 'SCC_After(A)', 'EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'EDS_PR_Before', 'EDS_PR_After', 'EDS_SR_Before', 'EDS_SR_After']
noon_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV(V)', 'SCC(A)', 'Power(W)', 'PR', 'SR']
testing_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV_Before(V)', 'OCV_After(V)', 'SCC_Before(A)', 'SCC_After(A)', 'CTRL1_OCV(V)', 'CTRL1_SCC(A)', 'CTRL2_OCV(V)', 'CTRL2_SCC(A)', 'EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'CTRL1_PWR(W)', 'CTRL2_PWR(W)']

root = Tk()
root.title("EDS Data Analysis Tool")
root.geometry("1000x455")

# function to clear the mode buttons
def clear_mode_buttons():
    testing_label.config(bg="white")
    manual_label.config(bg="white")
    noon_label.config(bg="white")

# function to specify output path
def select_output():
    # clear  entry fields
    out_entry.delete(0, END)
    # clear errors
    error_label.config(text="")
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
    # clear errors
    error_label.config(text="")
    # get the path for the csv file
    root.filename = filedialog.askopenfilename(initialdir=".", title="Select A CSV File", filetypes=(("CSV Files", "*.csv"),("All Files", "*.*")))
    # insert the path to the entry field
    file_entry.insert(0, root.filename)
    # based on path, figure out which mode
    global mode
    mode = root.filename.split("/")[-1]
    if mode == 'manual_data.csv':
        manual_label.config(bg="green")
    elif mode == 'testing_data.csv':
        testing_label.config(bg="green")
    elif mode == 'noon_data.csv':
        noon_label.config(bg="green")

# load sorted ata
def load_sorted(name):
    # file location for the csv file
    file = name
    # return pandas dataframe of the csv file
    df = pd.read_csv(file)
    # remove all NaN entries
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    return df

# show the soiling rates in new window
def show_sr():
    # new window for soiling rate data
    sr_window = Toplevel()
    sr_window.geometry("300x400")
    sr_title = Label(sr_window, text="Soiling Rate Values:", font=("Arial", 15)).pack()
    if mode ==  'manual_data.csv':
        pre,post = calc_soiling_rate(mode)
        message = "EDS1 Soiling Rate: " + pre + "%(PRE), " + post + "%(POST)"
        sr_contents = Label(sr_window, text=message).pack()
    elif mode == 'noon_data.csv':
        labels = ['EDS1_PRE', 'EDS2_PRE', 'EDS3_PRE', 'EDS4_PRE', 'EDS5_PRE', 'CTRL1_PRE', 'CTRL2_PRE','EDS1_POST','EDS2_POST','EDS3_POST','EDS4_POST','EDS5_POST','CTRL1_POST','CTRL2_POST']
        data = calc_soiling_rate(mode)
        # prepare the label message
        eds1 = "EDS1 Soiling Rate: " + str(data['EDS1_PRE']) + "%(PRE), " + str(data['EDS1_POST']) + "%(POST)"
        eds2 = "EDS2 Soiling Rate: " + str(data['EDS2_PRE']) + "%(PRE), " + str(data['EDS2_POST']) + "%(POST)"
        eds3 = "EDS3 Soiling Rate: " + str(data['EDS3_PRE']) + "%(PRE), " + str(data['EDS3_POST']) + "%(POST)"
        eds4 = "EDS4 Soiling Rate: " + str(data['EDS4_PRE']) + "%(PRE), " + str(data['EDS4_POST']) + "%(POST)"
        eds5 = "EDS5 Soiling Rate: " + str(data['EDS5_PRE']) + "%(PRE), " + str(data['EDS5_POST']) + "%(POST)"
        ctrl1 = "CTRL1 Soiling Rate: " + str(data['CTRL1_PRE']) + "%(PRE), " + str(data['CTRL1_POST']) + "%(POST)"
        ctrl2 = "CTRL2 Soiling Rate: " + str(data['CTRL2_PRE']) + "%(PRE), " + str(data['CTRL2_POST']) + "%(POST)"
        message = eds1 + '\n' + eds2 + '\n' + eds3 + '\n' + eds4 + '\n' + eds5 + '\n' + ctrl1 + '\n' + ctrl2
        # display the message
        sr_contents = Label(sr_window, text=message).pack()
    elif mode == 'testing_data.csv':
        #display error in the new window
        error_msg = Label(sr_window, text="No SR measurement for this mode", fg = 'red').pack()
    else:
        #display error in the new window
        error_msg = Label(sr_window, text="Please Select Valid CSV File For Analysis", fg = 'red').pack()

# function to calculate the soiling rate of the table's data
def calc_soiling_rate(mode):
    # check which mode of operation
    if mode == 'manual_data.csv':
        # get the file to find the soiling rate
        output = output_loc+"/manual_sorted.csv"
        df = load_sorted(output)
        # get the soiling ratio values
        sr_before = df['EDS_SR_Before']
        sr_after = df['EDS_SR_After']
        # calculate the soiling rate values
        soiling_rate_before = stats.theilslopes(sr_before, range(len(sr_before)), 0.90)[0].round(2)
        soiling_rate_after = stats.theilslopes(sr_after, range(len(sr_after)), 0.90)[0].round(2)
        # return the soiling rates
        return (str(soiling_rate_before), str(soiling_rate_after))
    elif mode == 'noon_data.csv':
        # get the file to find the soiling rate
        output = output_loc+"/noon_sorted.csv"
        df = load_sorted(output)
        labels = ['EDS1_PRE', 'EDS2_PRE', 'EDS3_PRE', 'EDS4_PRE', 'EDS5_PRE', 'CTRL1_PRE', 'CTRL2_PRE','EDS1_POST','EDS2_POST','EDS3_POST','EDS4_POST','EDS5_POST','CTRL1_POST','CTRL2_POST']
        # declare soiling ratio dictionary
        soiling_ratios = {
            'EDS1_PRE':[],
            'EDS2_PRE':[],
            'EDS3_PRE':[],
            'EDS4_PRE':[],
            'EDS5_PRE':[],
            'CTRL1_PRE':[],
            'CTRL2_PRE':[],
            'EDS1_POST':[],
            'EDS2_POST':[],
            'EDS3_POST':[],
            'EDS4_POST':[],
            'EDS5_POST':[],
            'CTRL1_POST':[],
            'CTRL2_POST':[],
        }
        # get the soiling ratio values
        counter = 0
        for x in df['SR']:
            if counter == 14:
                counter = 0
                soiling_ratios[labels[counter]].append(x)
                counter = counter + 1
            else:
                soiling_ratios[labels[counter]].append(x)
                counter = counter + 1
        # declare soiling rate dictionary
        soiling_rates = {
            'EDS1_PRE':0,
            'EDS2_PRE':0,
            'EDS3_PRE':0,
            'EDS4_PRE':0,
            'EDS5_PRE':0,
            'CTRL1_PRE':0,
            'CTRL2_PRE':0,
            'EDS1_POST':0,
            'EDS2_POST':0,
            'EDS3_POST':0,
            'EDS4_POST':0,
            'EDS5_POST':0,
            'CTRL1_POST':0,
            'CTRL2_POST':0,
        }
        # calculate the soiling rate values
        for y in labels:
            soiling_rates[y] = stats.theilslopes(soiling_ratios[y], range(len(soiling_ratios[y])), 0.90)[0].round(2)
        # return the dictionary
        return soiling_rates
    elif mode == 'testing_data.csv':
        # update the soiling rate value
        sr_label.config(text= "Soiling Rate: N/A (This mode does not measure SR)")
    else:
        # return error
        error_label.config(text="Select Valid CSV File For Analysis")

# error check the average day entry field
def avg_entry_check(window):
    if window == '':
        error_label.config(text="Please fill in the average days entry field")
        return False
    elif window.isalpha():
        error_label.config(text="Please input a valid number in the average days entry field")
        return False
    elif int(window) <= 0:
        error_label.config(text="Please input a valid number in the average days entry field")
        return False
    else:
        return True

# function to update the table
def get_table():
    # clear errors
    error_label.config(text="")
    # get the average day number
    global window
    window = avg_entry.get()
    # error check the window variable
    avg_check = avg_entry_check(window)
    if avg_check:
        # check which mode selected
        if mode == 'manual_data.csv':
            man_df = get_avg_manual_data(manual_cols_list, int(window))
            output = output_loc+"/manual_sorted.csv"
            x = man_df.to_csv(output)
            # upload csv to the table
            table.importCSV(output)
        elif mode == "noon_data.csv":
            man_df = get_avg_noon_data(noon_cols_list, int(window))
            output = output_loc+"/noon_sorted.csv"
            x = man_df.to_csv(output)
            # upload csv to the table
            table.importCSV(output)
        elif mode == "testing_data.csv":
            man_df = get_avg_testing_data(testing_cols_list, int(window))
            output = output_loc+"/testing_sorted.csv"
            x = man_df.to_csv(output)
            # upload csv to the table
            table.importCSV(output)
        else:
            error_label.config(text="Select Valid CSV File For Analysis!")

# plot the table
def plot_table():
    # clear errors
    error_label.config(text="")
    # check which mode selected
    if mode == 'manual_data.csv':
        # get the file to find the soiling rate
        output = output_loc+"/manual_sorted.csv"
        df = load_sorted(output)
        # get desired columns names to plot
        cols = ['SCC_Before(A)', 'SCC_After(A)','EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'EDS_PR_Before', 'EDS_PR_After', 'EDS_SR_Before', 'EDS_SR_After']
        # get the desired column data from the table
        data = {
            'SCC_Before(A)':[],
            'SCC_After(A)':[],
            'EDS_PWR_Before(W)':[],
            'EDS_PWR_After(W)':[],
            'EDS_PR_Before': [],
            'EDS_PR_After': [],
            'EDS_SR_Before': [],
            'EDS_SR_After': []
        }
        for x in cols:
            for y in df[x]:
                data[x].append(y)
        # get the dates for x axis
        dates = ()
        for x in df['Date']:
            x = x.replace("/2020", "")
            dates = dates + (x,)
        # plot the data (x,y)
        plt.figure(figsize=(12, 6))
        if plot_mode.get() == 'Isc':
            # plot a scatter plot
            plt.scatter(range(len(data['SCC_Before(A)'])),data['SCC_Before(A)'], label="Pre EDS")
            plt.scatter(range(len(data['SCC_After(A)'])),data['SCC_After(A)'], label="Post EDS")
            # add the plot title
            plt.title("Manual Mode - Isc(A)")
            # add the legend
            plt.legend(loc='upper right')
            # add axis limits
            x1,x2,y1,y2 = plt.axis()
            plt.axis([x1, x2, 0, 10])
            plt.xticks(np.arange(0, x2, 1), dates, fontsize=8, rotation=80)
        elif plot_mode.get() == 'Power':
            # plot a scatter plot
            plt.scatter(range(len(data['EDS_PWR_Before(W)'])), data['EDS_PWR_Before(W)'], label="Pre EDS")
            plt.scatter(range(len(data['EDS_PWR_Before(W)'])), data['EDS_PWR_After(W)'], label = "Post EDS")
            # add the plot title
            plt.title("Manual Mode - Power(W)")
            # add the legend
            plt.legend(loc='upper right')
            # add axis limits
            x1,x2,y1,y2 = plt.axis()
            plt.axis([x1, x2, 0, 50])
            plt.xticks(np.arange(0, x2, 1), dates, fontsize=8, rotation=80)
        elif plot_mode.get() == 'PR':
            # plot a scatter plot
            plt.scatter(range(len(data['EDS_PR_Before'])),data['EDS_PR_Before'], label="Pre EDS")
            plt.scatter(range(len(data['EDS_PR_After'])),data['EDS_PR_After'], label="Post EDS")
            # add the plot title
            plt.title("Manual Mode - PR")
            # add the legend
            plt.legend(loc='upper right')
            # add axis limits
            x1,x2,y1,y2 = plt.axis()
            plt.axis([x1, x2, -1, 100])
            plt.xticks(np.arange(0, x2, 1), dates, fontsize=8, rotation=80)
        elif plot_mode.get() == 'SR':
            # plot a scatter plot
            plt.scatter(range(len(data['EDS_SR_Before'])),data['EDS_SR_Before'], label="Pre EDS")
            plt.scatter(range(len(data['EDS_SR_After'])),data['EDS_SR_After'], label="Post EDS")
            # add the plot title
            plt.title("Manual Mode - SR")
            # add the legend
            plt.legend(loc='upper right')
            # add axis limits
            x1,x2,y1,y2 = plt.axis()
            plt.axis([x1, x2, -1, 100])
            plt.xticks(np.arange(0, x2, 1), dates, fontsize=8, rotation=80)
        #show the plot
        plt.show()
    elif mode == "noon_data.csv":
        # get the file location and declare constants
        output = output_loc+"/noon_sorted.csv"
        df = load_sorted(output)
        labels = ['EDS1_PRE', 'EDS2_PRE', 'EDS3_PRE', 'EDS4_PRE', 'EDS5_PRE', 'CTRL1_PRE', 'CTRL2_PRE','EDS1_POST','EDS2_POST','EDS3_POST','EDS4_POST','EDS5_POST','CTRL1_POST','CTRL2_POST']
        cols = ['SCC(A)', 'Power(W)', 'PR', 'SR']
        # declare dictionary to store data, each metric has 2 lists, one for pre and post data
        data = {
            'EDS1':{
                'SCC(A)':[[],[]],
                'Power(W)':[[],[]],
                'PR':[[],[]],
                'SR':[[],[]]
            },
            'EDS2':{
                'SCC(A)':[[],[]],
                'Power(W)':[[],[]],
                'PR':[[],[]],
                'SR':[[],[]]
            },
            'EDS3':{
                'SCC(A)':[[],[]],
                'Power(W)':[[],[]],
                'PR':[[],[]],
                'SR':[[],[]]
            },
            'EDS4':{
                'SCC(A)':[[],[]],
                'Power(W)':[[],[]],
                'PR':[[],[]],
                'SR':[[],[]]
            },
            'EDS5':{
                'SCC(A)':[[],[]],
                'Power(W)':[[],[]],
                'PR':[[],[]],
                'SR':[[],[]]
            },
            'CTRL1':{
                'SCC(A)':[[],[]],
                'Power(W)':[[],[]],
                'PR':[[],[]],
                'SR':[[],[]]
            },
            'CTRL2':{
                'SCC(A)':[[],[]],
                'Power(W)':[[],[]],
                'PR':[[],[]],
                'SR':[[],[]]
            }
        }
        # get the data
        counter = 0
        for x in cols:
            for y in df[x]:
                if counter == 0:
                    data['EDS1'][x][0].append(y)
                    counter += 1
                elif counter == 1:
                    data['EDS2'][x][0].append(y)
                    counter += 1
                elif counter == 2:
                    data['EDS3'][x][0].append(y)
                    counter += 1
                elif counter == 3:
                    data['EDS4'][x][0].append(y)
                    counter += 1
                elif counter == 4:
                    data['EDS5'][x][0].append(y)
                    counter += 1
                elif counter == 5:
                    data['CTRL1'][x][0].append(y)
                    counter += 1
                elif counter == 6:
                    data['CTRL2'][x][0].append(y)
                    counter += 1
                elif counter == 7:
                    data['EDS1'][x][1].append(y)
                    counter += 1
                elif counter == 8:
                    data['EDS2'][x][1].append(y)
                    counter += 1
                elif counter == 9:
                    data['EDS3'][x][1].append(y)
                    counter += 1
                elif counter == 10:
                    data['EDS4'][x][1].append(y)
                    counter += 1
                elif counter == 11:
                    data['EDS5'][x][1].append(y)
                    counter += 1
                elif counter == 12:
                    data['CTRL1'][x][1].append(y)
                    counter += 1
                elif counter == 13:
                    data['CTRL2'][x][1].append(y)
                    counter = 0
        # get the dates for x axis
        dates = ()
        date_counter = 0
        for x in df['Date']:
            if date_counter == 13:
                x = x.replace("/2020", "")
                dates = dates + (x,)
                date_counter = 0
            else:
                date_counter += 1
        # plot the data
        plt.figure(figsize=(12, 6))
        panels = ['EDS1', 'EDS2', 'EDS3', 'EDS4', 'EDS5', 'CTRL1', 'CTRL2']
        if plot_mode.get() == 'Isc':
            counter = 0
            for x in range(7):
                # add subplot
                plt.subplot(2,4,x+1)
                # add title
                plt.title("Noon Mode " + panels[x] + " - Isc(A)")
                # add scatter plots
                plt.scatter(range(len(data[panels[x]]['SCC(A)'][0])),data[panels[x]]['SCC(A)'][0], label="Pre EDS")
                plt.scatter(range(len(data[panels[x]]['SCC(A)'][1])),data[panels[x]]['SCC(A)'][1], label="Post EDS")
                # add the legend
                plt.legend(loc='upper right')
                # add axis limits
                x1,x2,y1,y2 = plt.axis()
                plt.axis([x1, x2, 0, 10])
                plt.xticks(np.arange(0, x2, 1), dates, fontsize=8, rotation=80)
        elif plot_mode.get() == 'Power':
            for x in range(7):
                # add subplot
                plt.subplot(2,4,x+1)
                # add title
                plt.title("Noon Mode " + panels[x] + " - Power(W)")
                # add scater plots
                plt.scatter(range(len(data[panels[x]]['Power(W)'][0])),data[panels[x]]['Power(W)'][0], label="Pre EDS")
                plt.scatter(range(len(data[panels[x]]['Power(W)'][1])),data[panels[x]]['Power(W)'][1], label="Post EDS")
                # add the legend
                plt.legend(loc='upper right')
                # add axis limits
                x1,x2,y1,y2 = plt.axis()
                plt.axis([x1, x2, 0, 50])
                plt.xticks(np.arange(0, x2, 1), dates, fontsize=8, rotation=80)
        elif plot_mode.get() == 'PR':
            for x in range(7):
                plt.subplot(2,4,x+1)
                # add title
                plt.title("Noon Mode "+ panels[x] + " - PR")
                # add scatter plots
                plt.scatter(range(len(data[panels[x]]['PR'][0])),data[panels[x]]['PR'][0], label="Pre EDS")
                plt.scatter(range(len(data[panels[x]]['PR'][1])),data[panels[x]]['PR'][1], label="Post EDS")
                # add the legend
                plt.legend(loc='upper right')
                # add axis limits
                x1,x2,y1,y2 = plt.axis()
                plt.axis([x1, x2, -1, 100])
                plt.xticks(np.arange(0, x2, 1), dates, fontsize=8, rotation=80)
        elif plot_mode.get() == 'SR':
            for x in range(7):
                # add subplot
                plt.subplot(2,4,x+1)
                # add title
                plt.title("Noon Mode "+ panels[x] + " - SR")
                # add scatter plots
                plt.scatter(range(len(data[panels[x]]['SR'][0])),data[panels[x]]['SR'][0], label="Pre EDS")
                plt.scatter(range(len(data[panels[x]]['SR'][1])),data[panels[x]]['SR'][1], label="Post EDS")
                # add the legend
                plt.legend(loc='upper right')
                # add axis limits
                x1,x2,y1,y2 = plt.axis()
                plt.axis([x1, x2, -1, 100])
                plt.xticks(np.arange(0, x2, 1), dates, fontsize=8, rotation=80)
        #show the plot
        plt.tight_layout(1)
        plt.show()
    elif mode == "testing_data.csv":
        # error message since no plotting for testing data
        error_label.config(text="No Plotting Feature for Testing Data")
    else:
        error_label.config(text="Select Valid CSV File For Analysis")

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
testing_label = Label(root, text="Testing Data", borderwidth=1.4, relief="solid", width=18, height=3)
testing_label.grid(row=1, column=0, padx=18)
manual_label = Label(root, text="Manual Data", borderwidth=1.4, relief="solid", width=18, height=3)
manual_label.grid(row=1, column=1)
noon_label = Label(root, text="Noon Data", borderwidth=1.4, relief="solid", width=18, height=3)
noon_label.grid(row=1, column=2, padx=18)

# button to get the path of the data csv file
file_btn = Button(root, text="Find CSV File", command=find_file, borderwidth=2, relief="raised")
file_btn.grid(row=0,column=0, padx=20, pady=20, sticky=W)

# entry field to display path for data csv file
file_entry = Entry(root, width=40)
file_entry.grid(row=0, column=1, columnspan=2, padx=2, sticky=W)

# button to display soiling rate values
sr_btn = Button(root, text="Get Soiling Rate", command=show_sr)
sr_btn.grid(row=2, column=0, columnspan=3, pady=209, sticky=S)

# create label for output path
out_btn = Button(root, text="Select Output Location", command=select_output, borderwidth=2, relief="raised")
out_btn.grid(row=2, column=0, padx=20, pady=177,sticky=S+W)

# entry field for the output path
out_entry = Entry(root, width=40)
out_entry.grid(row=2, column=1, columnspan=2, padx=5,pady=175, sticky=S+W)

# label for error message
error_label = Label(root, text="", fg='red',font=("Arial", 15))
error_label.grid(row=2, column=3,padx=10,pady=177,sticky=S+W)

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
plot_btn = Button(root, text="Plot Table", command=plot_table, font=("Arial", 14),borderwidth=1.4, relief="solid", width=18, height=3)
plot_btn.grid(row=2, column=3, padx=200, pady=60, sticky=N)

# create radio button for plotting
plot_mode = StringVar()
plot_mode.set("Power")
radio_btn1 = Radiobutton(root, text="Isc", variable=plot_mode, value="Isc")
radio_btn1.grid(row=2, column=3, sticky=N+W, pady=120, padx=200)
radio_btn2 = Radiobutton(root, text="Power", variable=plot_mode, value="Power")
radio_btn2.grid(row=2, column=3, sticky=N+W, pady=150, padx=200)
radio_btn3 = Radiobutton(root, text="PR", variable=plot_mode, value="PR")
radio_btn3.grid(row=2, column=3, sticky=N+W, pady=180, padx=200)
radio_btn4 = Radiobutton(root, text="SR", variable=plot_mode, value="SR")
radio_btn4.grid(row=2, column=3, sticky=N+W, pady=210, padx=200)

# create frame for the table
tframe = Frame(root)
tframe.grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky=N)

# insert the csv table
table = TableCanvas(tframe)
table.thefont = ('Arial',10)
table.show()

root.mainloop()
