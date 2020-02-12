import pandas as pd
import numpy as np
import math
import datetime

'''
MANUAL DATA FUNCTIONS
'''

def read_data(name):
    # file location for the csv file
    file = name #"./manual_data.csv"
    # return pandas dataframe of the csv file
    df = pd.read_csv(file)
    # remove all NaN entries
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    a=df.iterrows()
    i = 0
    for index,row in a:
        if math.isnan(row[2]):
            break
        else:
            i = i + 1
    table = df[0:i]
    
    return table


def sort_dates(eds_cols, window):
    # read the noon_data csv file
    df = read_data("./manual_data.csv")
    # declare initial variables
    col_name = 'Date'
    counter = 0
    date_string = ''
    new_col = {col_name:[]}
    # go through the Date column of the noon data csv file
    for x in df[col_name]:
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


def sort_time(eds_cols, window):
    # read the noon_data csv file
    df = read_data("./manual_data.csv")
    # declare initial variables
    col_name = 'Time'
    counter = 0
    time_data = []
    new_col = {col_name:[]}
    # go through the Time column of the noon data csv file
    for x in df[col_name]:
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


def sort_labels(eds_cols, window):
    # read the noon_data csv file
    df = read_data("./manual_data.csv")
    # declare initial variables
    col_name = 'EDS(#)'
    counter = 0
    new_col = {col_name:[]}
    # go through the labels column of the noon data csv file
    for x in df[col_name]:
        if counter == window-1:
            # append EDS number
            new_col[col_name].append("1")
            # reset counter
            counter = 0
        else:
            # increase counter
            counter = counter + 1
    eds_cols.update(new_col)
    return eds_cols



def sort_data(name, eds_cols, window):
    # read the noon_data csv file
    df = read_data("./manual_data.csv")
    # declare initial variables
    col_name = name
    counter = 0
    data = []
    avg = 0
    new_col = {col_name:[]}
    # go through the measurements data columns of the noon data csv file
    for x in df[col_name]:
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


def get_avg_manual_data(cols_list, window):
    # read the noon_data csv file
    df = read_data("./manual_data.csv")
    # declare new dictionary for avg data
    eds_cols = {}
    # sort the date
    eds_cols = sort_dates(eds_cols, window)
    # sort the time
    eds_cols = sort_time(eds_cols, window)
    # sort the pre/post, EDS number
    eds_cols = sort_labels(eds_cols, window)
    # sort all the numerical data
    for x in cols_list:
        eds_cols = sort_data(x, eds_cols, window)
    # create new dataframe
    eds_df = pd.DataFrame(eds_cols)
    return eds_df