import pandas as pd
import numpy as np
import math
import datetime

def read_data(name):
    # file location for the csv file
    file = name
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
    df = read_data("./noon_data.csv")
    # declare initial variables
    col_name = 'Date'
    counter = 0
    date_string = ''
    new_col = {col_name:[]}
    # go through the Date column of the noon data csv file
    for x in df[col_name]:
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

def sort_time(eds_cols, window):
    # read the noon_data csv file
    df = read_data("./noon_data.csv")
    # declare initial variables
    col_name = 'Time'
    counter = 0
    index_counter = 0
    pre_data = [0,0,0,0,0,0,0]
    post_data = [0,0,0,0,0,0,0]
    new_col = {col_name:[]}
    # go through the Time column of the noon data csv file
    for x in df[col_name]:
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

def sort_labels(eds_cols, window):
    # read the noon_data csv file
    df = read_data("./noon_data.csv")
    # declare initial variables
    col_name = 'PRE/POST'
    col_name2 = 'EDS/CTRL(#)'
    counter = 0
    new_col = {col_name:[]}
    new_col2= {col_name2:[]}
    # go through the labels column of the noon data csv file
    for x in df[col_name]:
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

def sort_data(name, eds_cols, window):
    # read the noon_data csv file
    df = read_data("./noon_data.csv")
    # declare initial variables
    col_name = name #'Temperature(C)'
    counter = 0
    index_counter = 0
    pre_data = [0,0,0,0,0,0,0]
    post_data = [0,0,0,0,0,0,0]
    new_col = {col_name:[]}
    # go through the measurements data columns of the noon data csv file
    for x in df[col_name]:
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

def get_avg_noon_data(cols_list, window):
    # read the noon_data csv file
    df = read_data("./noon_data.csv")
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