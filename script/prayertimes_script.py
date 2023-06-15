import pandas as pd

# Read the prayer times csv file
df = pd.read_csv('../data/prayertimes.csv')

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

########### Variables ###########

# get the column names for the morning times
morning_column_names = df.iloc[:, 3:6].columns

# get the column names for all time columns
time_column_names = df.iloc[:, 3:].columns

# get the month name in 3 letter format
month = get_month_name(df)

########### Main ###########

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
print(df)

# export df to text file with delimeter as --
df.to_csv('../export/prayertimes_final.txt', sep='-', index=False)