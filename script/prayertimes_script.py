import sys
import pandas as pd


# Read the prayer times csv file
df = pd.read_csv('../data/prayertimes.csv')

def check_time_format(num_of_time_columns, col_start, col_end):
    # num_of_time_columns: number of time columns in df
    # Col_start: index of first time column
    # Col_end: index of last time column + 1
    count_errors = 0
    for i in range(num_of_time_columns):
        # Convert df to Series and use regex to check if time format is correct. If correct contiue.
        if  sum(df.iloc[:,col_start:col_end].squeeze().str.fullmatch(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$') == False) == 0:
            continue
        else:
            count_errors += 1
            print('Time format is incorrect in column ' + df.iloc[:,col_start:col_end].columns + '. Expected format is 00:00')
        col_start += 1
        col_end += 1
    # If there are errors exit the script
    if count_errors > 0:
        sys.exit("Error Code 1: Exiting due to incorrect time format")

########### Functions ###########
# # get the month name in 3 letter format
def get_month_name(dataframe):
    month_name = dataframe.columns[1]
    return str(month_name[:3].title())

# trim all outer spaces in the dataframe
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# function to add AM or PM to the time
def add_am_pm(dataframe, column_name):
    if column_name in morning_column_names:
        dataframe[column_name] = dataframe[column_name] + 'AM'
    else:
        dataframe[column_name] = dataframe[column_name] + 'PM'
    return dataframe

# function to convert time from 12 hour to 24 hour format
def convert_to_24_hour_format(dataframe, column_name):
    dataframe[column_name] = pd.to_datetime(dataframe[column_name], format="%I:%M%p").dt.strftime('%H:%M')
    return dataframe

# function to check if number in df series is 2 digits. If not add a 0 in front of it.
def check_if_2_digits(series):
    for i in range(len(series)):
        if len(series[i]) == 1:
            series[i] = '0' + series[i]
    return series

def check_time_format(num_of_time_columns, col_start, col_end):
    # num_of_time_columns: number of time columns in df
    # Col_start: index of first time column
    # Col_end: index of last time column + 1
    count_errors = 0
    for i in range(num_of_time_columns):
        # Convert df to Series and use regex to check if time format is correct. If correct contiue.
        if  sum(df.iloc[:,col_start:col_end].squeeze().str.fullmatch(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$') == False) == 0:
            continue
        else:
            count_errors += 1
            print('Time format is incorrect in column ' + df.iloc[:,col_start:col_end].columns + '. Expected format is 00:00')
        col_start += 1
        col_end += 1
    # If there are errors exit the script
    if count_errors > 0:
        sys.exit("Error Code 1: Exiting due to incorrect time format")

########### Variables ###########

# get the column names for the morning times
morning_column_names = df.iloc[:, 3:6].columns

# get the column names for all time columns
time_column_names = df.iloc[:, 3:].columns

# get the month name in 3 letter format
month = get_month_name(df)

########### Main ###########

# check if time format is correct else exit script
check_time_format(10,3,4)

# add AM to the morning times and PM to the evening times
for name in time_column_names:
    add_am_pm(df, name)

# convert time from 12 hour to 24 hour format
for name in time_column_names:
    convert_to_24_hour_format(df, name)

# Make all day numbers 2 digits. Example 1 to 01
df.iloc[:,1] = check_if_2_digits(df.iloc[:,1].astype(str))

# add the month name to the dataframe as a new column at the start
df.insert(0, 'Month', (month + ' ' + df.iloc[:,1].astype(str)))
df.insert(11, 'Magrib Start', df.iloc[:,11])

# drop the day column
df.drop(df.columns[1], axis=1, inplace=True)
# drop the arbic month column
df.drop(df.columns[2], axis=1, inplace=True)
# drop the date column
df.drop(df.columns[1], axis=1, inplace=True)

# print the dataframe
#print(df)

# export df to text file with delimeter as -
df.to_csv('../export/prayertimes_final.txt', sep='-', index=False)

# Read the file in to memory (if file is large will give memory error)
with open('../export/prayertimes_final.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('-', '--')

# Write the file out again
with open('../export/prayertimes_final.txt', 'w') as file:
  file.write(filedata)