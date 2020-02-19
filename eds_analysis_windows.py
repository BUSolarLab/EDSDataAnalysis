from tkinter import *
from scipy import stats
from tkinter import filedialog
from tkintertable import TableCanvas, TableModel
import pandas as pd
import numpy as np
import math
import datetime
import matplotlib.pyplot as plt
import os
import idna
import sys

'''MANUAL MODE PARSING'''
class manual_mode:
    def __init__(self):
        self.df = pd.read_csv("./inputs/manual_data.csv")
    
    # read the csv data file
    def read_data(self):
        # remove all NaN entries
        self.df.drop(self.df.filter(regex="Unname"),axis=1, inplace=True)
        a=self.df.iterrows()
        i = 0
        for index,row in a:
            if math.isnan(row[2]):
                break
            else:
                i = i + 1
        table = self.df[0:i]
        return table
    
    # sort the date column of the csv file
    def sort_dates(self, eds_cols, window):
        # declare initial variables
        col_name = 'Date'
        counter = 0
        date_string = ''
        new_col = {col_name:[]}
        # go through the Date column of the noon data csv file
        for x in self.df[col_name]:
            if window == 1:
                # no date string modification
                new_col[col_name].append(x)
            elif counter == 0:
                # store the first date to date_string
                date_string = date_string + x + '-'
                # increase counter
                counter = counter + 1
            elif counter == (window-1):
                # store the last date
                date_string = date_string + x
                # store to dictionary for dataframe for pre and post entry
                new_col[col_name].append(date_string)
                # reset date_string
                date_string = ''
                # reset counter
                counter = 0
            else:
                # increase counter
                counter = counter + 1
        eds_cols.update(new_col)
        return eds_cols

    # sort the time column of the csv file
    def sort_time(self, eds_cols, window):
        # declare initial variables
        col_name = 'Time'
        counter = 0
        time_data = []
        new_col = {col_name:[]}
        # go through the Time column of the noon data csv file
        for x in self.df[col_name]:
            # convert time to seconds
            a,b,c = x.split(':')
            hour = int(a)*60*60
            minute = int(b)*60
            second = int(c)
            total_sec = hour + minute + second
            if counter == window-1:
                # append the nth data for post time
                time_data.append(total_sec)
                # take average seconds
                time_avg = sum(time_data)/window
                # convert seconds back to time string using datetime
                time = str(datetime.timedelta(seconds = int(time_avg)))
                # append to the dictionary
                new_col[col_name].append(time)
                # reset counter
                counter = 0
                time_data = []
            else:
                # append time data for pre measurements
                time_data.append(total_sec)
                # increase counter
                counter = counter + 1
        eds_cols.update(new_col)
        return eds_cols
    
    # sort panel labels from the cvs file
    def sort_labels(self, eds_cols, window):
        # declare initial variables
        col_name = 'EDS(#)'
        counter = 0
        new_col = {col_name:[]}
        # go through the labels column of the noon data csv file
        for x in self.df[col_name]:
            if counter == window-1:
                # append EDS number 1 since manual mode is EDS1 only
                new_col[col_name].append("1")
                # reset counter
                counter = 0
            else:
                # increase counter
                counter = counter + 1
        eds_cols.update(new_col)
        return eds_cols

    # sort the desired data from other columns from the csv file
    def sort_data(self, name, eds_cols, window):
        # declare initial variables
        col_name = name
        counter = 0
        data = []
        avg = 0
        new_col = {col_name:[]}
        # go through the measurements data columns of the noon data csv file
        for x in self.df[col_name]:
            if counter == window-1:
                # seperate pre and post for nth data
                data.append(x)
                # get average value from pre post lists
                avg = sum(data)/window
                # append results to new dataframe
                new_col[col_name].append(avg)
                # reset counter
                counter = 0
                data=[]
            else:
                # append the data
                data.append(x)
                # increase counter
                counter = counter + 1
        eds_cols.update(new_col)
        return eds_cols
    
    # main function that calls everything
    def get_avg_manual_data(self, cols_list, window):
        # check if window is 1 day
        if window == 1:
            return self.df
        # declare new dictionary for avg data
        eds_cols = {}
        # sort the date
        eds_cols = self.sort_dates(eds_cols, window)
        # sort the time
        eds_cols = self.sort_time(eds_cols, window)
        # sort the pre/post, EDS number
        eds_cols = self.sort_labels(eds_cols, window)
        # sort all the numerical data
        for x in cols_list:
            eds_cols = self.sort_data(x, eds_cols, window)
        # create new dataframe
        eds_df = pd.DataFrame(eds_cols)
        return eds_df

'''NOON MODE PARSING'''
class noon_mode:
    def __init__(self):
        self.df = pd.read_csv("./inputs/noon_data.csv")
    
    # read the csv file
    def read_data(self):
        # remove all NaN entries
        self.df.drop(self.df.filter(regex="Unname"),axis=1, inplace=True)
        a=self.df.iterrows()
        i = 0
        for index,row in a:
            if math.isnan(row[2]):
                break
            else:
                i = i + 1
        table = self.df[0:i]
        return table
    
    # sort the date column of the csv file
    def sort_dates(self,eds_cols, window):
        # declare initial variables
        col_name = 'Date'
        counter = 0
        date_string = ''
        new_col = {col_name:[]}
        # go through the Date column of the noon data csv file
        for x in self.df[col_name]:
            if counter == 0:
                # store the first date to date_string
                date_string = date_string + x + '-'
                # increase counter
                counter = counter + 1
            elif counter == ((window*14)-1):
                # store the last date
                date_string = date_string + x
                # store to dictionary for dataframe for pre and post entry
                for x in range (14):
                    new_col[col_name].append(date_string)
                # reset date_string
                date_string = ''
                # reset counter
                counter = 0
            else:
                # increase counter
                counter = counter + 1
        eds_cols.update(new_col) 
        return eds_cols
    
    # sort the time column of the csv file
    def sort_time(self,eds_cols, window):
        # declare initial variables
        col_name = 'Time'
        counter = 0
        index_counter = 0
        pre_data = [0,0,0,0,0,0,0]
        post_data = [0,0,0,0,0,0,0]
        new_col = {col_name:[]}
        # go through the Time column of the noon data csv file
        for x in self.df[col_name]:
            # convert time to seconds
            a,b,c = x.split(':')
            hour = int(a)*60*60
            minute = int(b)*60
            second = int(c)
            total_sec = hour + minute + second
            if counter == ((window*14)-1):
                # modify nth time data
                post_data[6] = post_data[6] + total_sec
                # take average seconds for pre data
                avg_pre_data = []
                for x in pre_data:
                    avg_pre_data.append(x/window)
                # take average seconds for post data
                avg_post_data = []
                for x in post_data:
                    avg_post_data.append(x/window)
                # convert seconds back to time string using datetime for pre data
                pre_time = []
                for x in avg_pre_data:
                    pre_time.append(str(datetime.timedelta(seconds = int(x))))
                # convert seconds back to time string using datetime for post data
                post_time = []
                for x in avg_post_data:
                    post_time.append(str(datetime.timedelta(seconds = int(x))))
                # append to the dictionary
                total_data = pre_time + post_time
                new_col[col_name] = new_col[col_name]+ total_data
                # reset counter
                index_counter = 0
                counter = 0
                pre_data = [0,0,0,0,0,0,0]
                post_data = [0,0,0,0,0,0,0]
                total_data = []
            else:
                # check if its pre or post date points
                if index_counter < 7:
                    pre_data[index_counter] = pre_data[index_counter] + total_sec
                    # increase counters
                    index_counter = index_counter + 1
                    counter = counter + 1
                else:
                    if index_counter == 14:
                        pre_data[0] = pre_data[0] + total_sec
                        # increase counters
                        index_counter = 1
                        counter = counter + 1
                    else:
                        # modify time data
                        post_data[index_counter-7] = post_data[index_counter-7] + total_sec
                        # increase counters
                        index_counter = index_counter + 1
                        counter = counter + 1
        eds_cols.update(new_col)
        return eds_cols

    # sort the panel labels for the csv file
    def sort_labels(self,eds_cols, window):
        # declare initial variables
        col_name = 'PRE/POST'
        col_name2 = 'EDS/CTRL(#)'
        counter = 0
        new_col = {col_name:[]}
        new_col2= {col_name2:[]}
        # go through the labels column of the noon data csv file
        for x in self.df[col_name]:
            if counter == ((window*14)-1):
                # append PRE
                for x in range(7):
                    new_col[col_name].append("PRE")
                # append EDS number
                for x in range(5):
                    new_col2[col_name2].append("EDS"+str(x+1))
                # append CTRL unmber
                new_col2[col_name2].append("CTRL1")
                new_col2[col_name2].append("CTRL2")

                # append POST
                for x in range(7):
                    new_col[col_name].append("POST")
                # append EDS number
                for x in range(5):
                    new_col2[col_name2].append("EDS"+str(x+1))
                # append CTRL unmber
                new_col2[col_name2].append("CTRL1")
                new_col2[col_name2].append("CTRL2")
                # reset counter
                counter = 0
            else:
                # increase counter
                counter = counter + 1
        eds_cols.update(new_col)
        eds_cols.update(new_col2)
        return eds_cols
    
    # sort the desired data from other columns from the csv file
    def sort_data(self,name, eds_cols, window):
        # declare initial variables
        col_name = name #'Temperature(C)'
        counter = 0
        index_counter = 0
        pre_data = [0,0,0,0,0,0,0]
        post_data = [0,0,0,0,0,0,0]
        new_col = {col_name:[]}
        # go through the measurements data columns of the noon data csv file
        for x in self.df[col_name]:
            if counter == ((window*14)-1):
                # modify nth time data
                post_data[6] = post_data[6] + x
                # take average seconds for pre data
                avg_pre_data = []
                for i in pre_data:
                    avg_pre_data.append(i/window)
                # take average seconds for post data
                avg_post_data = []
                for i in post_data:
                    avg_post_data.append(i/window)
                # append to the dictionary
                total_data = avg_pre_data + avg_post_data
                new_col[col_name] = new_col[col_name]+ total_data
                # reset counter
                index_counter = 0
                counter = 0
                pre_data = [0,0,0,0,0,0,0]
                post_data = [0,0,0,0,0,0,0]
                total_data = []
            else:
                # check if its pre or post date points
                if index_counter < 7:
                    pre_data[index_counter] = pre_data[index_counter] + x
                    # increase counters
                    index_counter = index_counter + 1
                    counter = counter + 1
                else:
                    if index_counter == 14:
                        pre_data[0] = pre_data[0] + x
                        # increase counters
                        index_counter = 1
                        counter = counter + 1
                    else:
                        # modify time data
                        post_data[index_counter-7] = post_data[index_counter-7] + x
                        # increase counters
                        index_counter = index_counter + 1
                        counter = counter + 1
        eds_cols.update(new_col)
        return eds_cols
    
    # main function that calls all functions
    def get_avg_noon_data(self,cols_list, window):
        # check if window is just 1 day
        if window == 1:
            return self.df
        # declare new dictionary for avg data
        eds_cols = {}
        # sort the date
        eds_cols = self.sort_dates(eds_cols, window)
        # sort the time
        eds_cols = self.sort_time(eds_cols, window)
        # sort the pre/post, EDS number
        eds_cols = self.sort_labels(eds_cols, window)
        # sort all the numerical data
        for x in cols_list:
            eds_cols = self.sort_data(x, eds_cols, window)
        # create new dataframe
        eds_df = pd.DataFrame(eds_cols)
        return eds_df

'''TESTING MODE PARSING'''
class testing_mode:
    def __init__(self):
        self.df = pd.read_csv("./inputs/testing_data.csv")
    
    # read the data of the csv file
    def read_data(self):
        # remove all NaN entries
        self.df.drop(self.df.filter(regex="Unname"),axis=1, inplace=True)
        a=df.iterrows()
        i = 0
        for index,row in a:
            if math.isnan(row[2]):
                break
            else:
                i = i + 1
        table = self.df[0:i]
        return table
    
    # sort the date column of this csv file
    def sort_dates(self,eds_cols, window):
        # declare initial variables
        col_name = 'Date'
        counter = 0
        date_string = ''
        new_col = {col_name:[]}
        # go through the Date column of the noon data csv file
        for x in self.df[col_name]:
            if counter == 0:
                # store the first date to date_string
                date_string = date_string + x + '-'
                # increase counter
                counter = counter + 1
            elif counter == ((window*5)-1):
                # store the last date
                date_string = date_string + x
                # store to dictionary for dataframe for pre and post entry
                for x in range (5):
                    new_col[col_name].append(date_string)
                # reset date_string
                date_string = ''
                # reset counter
                counter = 0
            else:
                # increase counter
                counter = counter + 1
        eds_cols.update(new_col)    
        return eds_cols
    
    # sort time column of the csv file
    def sort_time(self,eds_cols, window):
        # declare initial variables
        col_name = 'Time'
        counter = 0
        index_counter = 0
        time_data = [0,0,0,0,0]
        new_col = {col_name:[]}
        # go through the Time column of the noon data csv file
        for x in self.df[col_name]:
            # convert time to seconds
            a,b,c = x.split(':')
            hour = int(a)*60*60
            minute = int(b)*60
            second = int(c)
            total_sec = hour + minute + second
            if counter == ((window*5)-1):
                # check if its pre or post date points
                time_data[index_counter] = time_data[index_counter] + total_sec
                # take average seconds for pre data
                avg_time_data = []
                for x in time_data:
                    avg_time_data.append(x/window)
                # convert seconds back to time string using datetime for pre data
                time = []
                for x in avg_time_data:
                    time.append(str(datetime.timedelta(seconds = int(x))))
                # append to the dictionary
                new_col[col_name] = new_col[col_name]+ time
                # reset counter
                counter = 0
                index_counter = 0
                time_data = [0,0,0,0,0]
            else:
                if index_counter == 5:
                    index_counter = 0
                # check if its pre or post date points
                time_data[index_counter] = time_data[index_counter] + total_sec
                # increase counters
                counter = counter + 1
                index_counter = index_counter + 1
        eds_cols.update(new_col)
        return eds_cols
    
    # sort the panel labels for the csv file
    def sort_labels(self,eds_cols, window):
        # declare initial variables
        col_name2 = 'EDS(#)'
        counter = 0
        new_col2= {col_name2:[]}
        # go through the labels column of the noon data csv file
        for x in self.df[col_name2]:
            if counter == ((window*5)-1):
                # append EDS number
                for x in range(5):
                    new_col2[col_name2].append("EDS"+str(x+1))
                # reset counter
                counter = 0
            else:
                # increase counter
                counter = counter + 1
        eds_cols.update(new_col2)
        return eds_cols
    
    # sort the desired data from other columns from the csv file
    def sort_data(self,name, eds_cols, window):
        # declare initial variables
        col_name = name
        counter = 0
        index_counter = 0
        data = [0,0,0,0,0]
        new_col = {col_name:[]}
        # go through the measurements data columns of the noon data csv file
        for x in self.df[col_name]:
            if counter == ((window*5)-1):
                # modify nth time data
                data[index_counter] = data[index_counter] + x
                # take average seconds for data
                avg_data = []
                for i in data:
                    avg_data.append(i/window)
                # append to the dictionary
                new_col[col_name] = new_col[col_name]+ avg_data
                # reset counter
                index_counter = 0
                counter = 0
                data = [0,0,0,0,0]
            else:
                if index_counter == 5:
                    index_counter = 0
                # check if its pre or post date points
                data[index_counter] = data[index_counter] + x
                # increase counters
                counter = counter + 1
                index_counter = index_counter + 1
        eds_cols.update(new_col)
        return eds_cols
    
    # main function for all functions
    def get_avg_testing_data(self,cols_list, window):
        # check if window is 1 day
        if window == 1:
            return self.df
        # declare new dictionary for avg data
        eds_cols = {}
        # sort the date
        eds_cols = self.sort_dates(eds_cols, window)
        # sort the time
        eds_cols = self.sort_time(eds_cols, window)
        # sort the pre/post, EDS number
        eds_cols = self.sort_labels(eds_cols, window)
        # sort all the numerical data
        for x in cols_list:
            eds_cols = self.sort_data(x, eds_cols, window)
        # create new dataframe
        eds_df = pd.DataFrame(eds_cols)
        return eds_df

'''MAIN GUI CLASS FOR EDS ANALYSIS'''
class EDS:
    '''INSTANTIATION'''
    def __init__(self, root, manual, noon, testing):
        # initialize the application
        self.root = root
        self.root.title("EDS Data Analysis Tool")
        self.root.geometry("1050x550")

        '''OTHER CLASSES'''
        # instantiate other classes to parse the csv files
        self.manual_mode = manual
        self.noon_mode = noon
        self.testing_mode = testing

        '''CONSTANTS'''
        # header constants from the csv files
        self.manual_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV_Before(V)', 'OCV_After(V)', 'SCC_Before(A)', 'SCC_After(A)', 'EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'EDS_PR_Before', 'EDS_PR_After', 'EDS_SR_Before', 'EDS_SR_After']
        self.noon_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV(V)', 'SCC(A)', 'Power(W)', 'PR', 'SR']
        self.testing_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'OCV_Before(V)', 'OCV_After(V)', 'SCC_Before(A)', 'SCC_After(A)', 'CTRL1_OCV(V)', 'CTRL1_SCC(A)', 'CTRL2_OCV(V)', 'CTRL2_SCC(A)', 'EDS_PWR_Before(W)', 'EDS_PWR_After(W)', 'CTRL1_PWR(W)', 'CTRL2_PWR(W)']
        
        # global variables
        self.mode = ''
        self.output_loc = ''
        self.window = 1

        '''LABELS'''
        # labels for the program title
        self.title_label = Label(root, text="EDS DATA ANALYSIS TOOL", font=("Helvetica", 20))
        self.title_label.grid(row=0, column=3, padx=10,pady=15, sticky=W)
        self.bu_label = Label(root, text="BOSTON UNIVERSITY", font=("Arial", 14))
        self.bu_label.grid(row=1, column=3, padx=10,sticky=W)

        # instructions label
        self.ins_label = Label(root, text="How To Use:",font=("Arial", 13))
        self.ins_label.grid(row=2, column=3,padx=10, pady=120, sticky=N+W)
        self.ins_label1 = Label(root, text=" 1. Select the CSV File To Analyze",font=("Arial", 11))
        self.ins_label1.grid(row=2, column=3, padx=10, pady=150, sticky=W+N)
        self.ins_label2 = Label(root, text=" 2. Select Output File Location",font=("Arial", 11))
        self.ins_label2.grid(row=2, column=3, padx=10, pady=180, sticky=W+N)
        self.ins_label3 = Label(root, text=" 3. Click Table Button",font=("Arial", 11))
        self.ins_label3.grid(row=2, column=3, padx=10, pady=210, sticky=W+N)
        self.ins_label4 = Label(root, text=" 4. Plot Metrics",font=("Arial", 11))
        self.ins_label4.grid(row=2, column=3, padx=10, pady=240, sticky=W+N)

        # labels for showing testing/manual/noon mode
        self.testing_label = Label(root, text="Testing Data", borderwidth=1.4, relief="solid", width=18, height=3)
        self.testing_label.grid(row=1, column=0, padx=18)
        self.manual_label = Label(root, text="Manual Data", borderwidth=1.4, relief="solid", width=18, height=3)
        self.manual_label.grid(row=1, column=1)
        self.noon_label = Label(root, text="Noon Data", borderwidth=1.4, relief="solid", width=18, height=3)
        self.noon_label.grid(row=1, column=2, padx=18)

        # label for error message
        self.error_label = Label(root, text="", fg='red',font=("Arial", 15))
        self.error_label.grid(row=2, column=3,padx=10,pady=177,sticky=S+W)

        # label to get average day input
        self.avg_label = Label(root, text="Average Days: ",font=("Arial", 14))
        self.avg_label.grid(row=2, column=3, padx=10, pady=21, sticky=W+N)

        '''BUTTONS'''
        # button to get the path of the data csv file
        self.file_btn = Button(root, text="Find CSV File", command= self.find_file, borderwidth=2, relief="raised")
        self.file_btn.grid(row=0,column=0, padx=20, pady=20, sticky=W)

        # button to display soiling rate values
        self.sr_btn = Button(root, text="Get Soiling Rate", command= self.show_sr)
        self.sr_btn.grid(row=2, column=0, columnspan=3, pady=135, sticky=S)

        # create label for getting output path
        self.out_btn = Button(root, text="Select Output Location", command= self.select_output, borderwidth=2, relief="raised")
        self.out_btn.grid(row=2, column=0, padx=20, pady=98,sticky=S+W)

        # create button to update the table
        self.table_btn = Button(root, text="Get Table", command= self.get_table, font=("Arial", 14),borderwidth=1.4, relief="solid", width=15, height=3)
        self.table_btn.grid(row=2, column=3, padx=10, pady=60, sticky=N+W)

        # create button to plot the table
        self.plot_btn = Button(root, text="Plot Table", command= self.plot_table, font=("Arial", 14),borderwidth=1.4, relief="solid", width=15, height=3)
        self.plot_btn.grid(row=2, column=3, padx=200, pady=60, sticky=N)

        '''ENTRY FIELDS'''
        # entry field to display path for data csv file
        self.file_entry = Entry(root, width=55)
        self.file_entry.grid(row=0, column=1, columnspan=2, padx=2, sticky=W)

        # entry field for the output path
        self.out_entry = Entry(root, width=55)
        self.out_entry.grid(row=2, column=1, columnspan=2, padx=5,pady=100, sticky=S+W)

        # entry field for average day input
        self.avg_entry = Entry(root, width= 35)
        self.avg_entry.grid(row=2, column=3,padx=150, pady=25, sticky=N+W)

        '''RADIO BUTTON'''
        # create radio button for selecting which plot
        self.plot_mode = StringVar()
        self.plot_mode.set("Power")
        self.radio_btn1 = Radiobutton(root, text="Isc", variable=self.plot_mode, value="Isc")
        self.radio_btn1.grid(row=2, column=3, sticky=N+W, pady=150, padx=260)
        self.radio_btn2 = Radiobutton(root, text="Power", variable=self.plot_mode, value="Power")
        self.radio_btn2.grid(row=2, column=3, sticky=N+W, pady=180, padx=260)
        self.radio_btn3 = Radiobutton(root, text="PR", variable=self.plot_mode, value="PR")
        self.radio_btn3.grid(row=2, column=3, sticky=N+W, pady=210, padx=260)
        self.radio_btn4 = Radiobutton(root, text="SR", variable=self.plot_mode, value="SR")
        self.radio_btn4.grid(row=2, column=3, sticky=N+W, pady=240, padx=260)

        '''FRAME'''
        # create frame for the table
        self.tframe = Frame(root)
        self.tframe.grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky=N)

        '''TABLE CANVAS'''
        # insert the csv table
        self.table = TableCanvas(self.tframe)
        self.table.thefont = ('Arial',10)
        self.table.show()

    '''Button Functions'''
    # function to get csv file path
    def find_file(self):
        # clear the entry field
        self.file_entry.delete(0, END)
        # clear the color for the testing modes
        self.clear_mode_buttons()
        # clear errors
        self.error_label.config(text="")
        # get the path for the csv file
        self.root.filename = filedialog.askopenfilename(initialdir=".", title="Select A CSV File", filetypes=(("CSV Files", "*.csv"),("All Files", "*.*")))
        # insert the path to the entry field
        self.file_entry.insert(0, root.filename)
        # based on path, figure out which mode
        self.mode = root.filename.split("/")[-1]
        if self.mode == 'manual_data.csv':
            self.manual_label.config(bg="green")
        elif self.mode == 'testing_data.csv':
            self.testing_label.config(bg="green")
        elif self.mode == 'noon_data.csv':
            self.noon_label.config(bg="green")
    
    # show the soiling rates in new window
    def show_sr(self):
        # new window for soiling rate data
        self.sr_window = Toplevel()
        self.sr_window.geometry("300x400")
        self.sr_title = Label(self.sr_window, text="Soiling Rate Values:", font=("Arial", 15)).pack()
        if self.mode ==  'manual_data.csv':
            pre,post = self.calc_soiling_rate(self.mode)
            # error check the calculation
            if pre == "error":
                #display error in the new window
                self.error_msg = Label(self.sr_window, text="Please enter a valid avg day entry for analysis", fg = 'red').pack()
            else:
                message = "EDS1 Soiling Rate: " + pre + "%(PRE), " + post + "%(POST)"
                sr_contents = Label(self.sr_window, text=message).pack()
        elif self.mode == 'noon_data.csv':
            data = self.calc_soiling_rate(self.mode)
            # error check the calculation
            if data == "error":
                #display error in the new window
                self.error_msg = Label(self.sr_window, text="Please enter a valid avg day entry for analysis", fg = 'red').pack()
            else:
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
                sr_contents = Label(self.sr_window, text=message).pack()
        elif self.mode == 'testing_data.csv':
            #display error in the new window
            self.error_msg = Label(self.sr_window, text="No SR measurement for this mode", fg = 'red').pack()
        else:
            #display error in the new window
            self.error_msg = Label(self.sr_window, text="Please Select Valid CSV File For Analysis", fg = 'red').pack()
    
    # function to specify output path
    def select_output(self):
        # clear  entry fields
        self.out_entry.delete(0, END)
        # clear errors
        self.error_label.config(text="")
        # use filedialog to select output location
        self.out_dir = filedialog.askdirectory(initialdir=".",title="Select A Folder To Store Output")
        # insert to entry field
        self.out_entry.insert(0, self.out_dir)
        # store in location
        self.output_loc = self.out_dir
    
    # function to update the table
    def get_table(self):
        # clear errors
        self.error_label.config(text="")
        # get the average day number
        self.window = self.avg_entry.get()
        # error check the window variable
        avg_check = self.avg_entry_check(self.window)
        if avg_check:
            # check which mode selected
            if self.mode == 'manual_data.csv':
                man_df = self.manual_mode.get_avg_manual_data(self.manual_cols_list, int(self.window))
                output = self.output_loc+"/manual_sorted.csv"
                x = man_df.to_csv(output)
                # upload csv to the table
                self.table.importCSV(output)
            elif self.mode == "noon_data.csv":
                man_df = self.noon_mode.get_avg_noon_data(self.noon_cols_list, int(self.window))
                output = self.output_loc+"/noon_sorted.csv"
                x = man_df.to_csv(output)
                # upload csv to the table
                self.table.importCSV(output)
            elif self.mode == "testing_data.csv":
                man_df = self.testing_mode.get_avg_testing_data(self.testing_cols_list, int(self.window))
                output = self.output_loc+"/testing_sorted.csv"
                x = man_df.to_csv(output)
                # upload csv to the table
                self.table.importCSV(output)
            else:
                self.error_label.config(text="Select Valid CSV File For Analysis!")
    
    # plot the table
    def plot_table(self):
        # clear errors
        self.error_label.config(text="")
        # check which mode selected
        if self.mode == 'manual_data.csv':
            # get the file to find the soiling rate
            output = self.output_loc+"/manual_sorted.csv"
            df = self.load_sorted(output)
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
            if self.plot_mode.get() == 'Isc':
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
            elif self.plot_mode.get() == 'Power':
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
            elif self.plot_mode.get() == 'PR':
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
            elif self.plot_mode.get() == 'SR':
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
        elif self.mode == "noon_data.csv":
            # get the file location and declare constants
            output = self.output_loc+"/noon_sorted.csv"
            df = self.load_sorted(output)
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
            if self.plot_mode.get() == 'Isc':
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
            elif self.plot_mode.get() == 'Power':
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
            elif self.plot_mode.get() == 'PR':
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
            elif self.plot_mode.get() == 'SR':
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
        elif self.mode == "testing_data.csv":
            # error message since no plotting for testing data
            self.error_label.config(text="No Plotting Feature for Testing Data")
        else:
            self.error_label.config(text="Select Valid CSV File For Analysis")

    '''Non Button Functions'''
    # function to clear the mode buttons
    def clear_mode_buttons(self):
        self.testing_label.config(bg="white")
        self.manual_label.config(bg="white")
        self.noon_label.config(bg="white")
    
    # load sorted data as pandas dataframe
    def load_sorted(self,name):
        # file location for the csv file
        file = name
        # return pandas dataframe of the csv file
        df = pd.read_csv(file)
        # remove all NaN entries
        df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
        return df
    
    # function to calculate the soiling rate of the table's data
    def calc_soiling_rate(self, mode):
        # check which mode of operation
        if self.mode == 'manual_data.csv':
            # get the file to find the soiling rate
            output = self.output_loc+"/manual_sorted.csv"
            df = self.load_sorted(output)
            # get the soiling ratio values
            sr_before = df['EDS_SR_Before']
            sr_after = df['EDS_SR_After']
            # error check the data if it can be computed for soiling rate
            if len(sr_before) == 0:
                return ("error", "error")
            elif len(sr_before) == 1:
                return ("error", "error")
            # calculate the soiling rate values
            soiling_rate_before = stats.theilslopes(sr_before, range(len(sr_before)), 0.90)[0].round(2)
            soiling_rate_after = stats.theilslopes(sr_after, range(len(sr_after)), 0.90)[0].round(2)
            # return the soiling rates
            return (str(soiling_rate_before), str(soiling_rate_after))
        elif self.mode == 'noon_data.csv':
            # get the file to find the soiling rate
            output = self.output_loc+"/noon_sorted.csv"
            df = self.load_sorted(output)
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
            # error check the data to make sure it can compute soiling rate
            if len(soiling_ratios['EDS1_PRE'])==0:
                return "error"
            elif len(soiling_ratios['EDS1_PRE'])==1:
                return "error"
            # calculate the soiling rate values
            for y in labels:
                soiling_rates[y] = stats.theilslopes(soiling_ratios[y], range(len(soiling_ratios[y])), 0.90)[0].round(2)
            # return the dictionary
            return soiling_rates
        elif self.mode == 'testing_data.csv':
            # update the soiling rate value
            self.sr_label.config(text= "Soiling Rate: N/A (This mode does not measure SR)")
        else:
            # return error
            self.error_label.config(text="Select Valid CSV File For Analysis")
    
    # error check the average day entry field
    def avg_entry_check(self, window):
        if self.window == '':
            self.error_label.config(text="Please fill in the average days entry field")
            return False
        elif self.window.isalpha():
            self.error_label.config(text="Please input a valid number in the average days entry field")
            return False
        elif int(self.window) <= 0:
            self.error_label.config(text="Please input a valid number in the average days entry field")
            return False
        else:
            return True

# run the program
root = Tk()
gui = EDS(root, manual_mode(), noon_mode(), testing_mode())
root.mainloop()