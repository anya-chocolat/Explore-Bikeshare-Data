#!/usr/bin/env python
# coding: utf-8

# In[40]:


import time
import pandas as pd
import numpy as np


# In[41]:


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


# In[42]:


# additional functions to use inside the get_filters() function
# get user input for city (chicago, new york city, washington)
def get_city():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) city - name of the city to analyze
    """

    city_question = 'Would you like to see data for Chicago, New York City, or Washington? '
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input(city_question).lower()
        if city == 'new york':
            city = 'new york city'
        if city in cities:
            return city
        else:
            print('Invalid input! Please type Chicago, New York City, or Washington.')


# In[43]:


# get user input for month (all, january, february, ... , june)
def get_month():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """

    month_question = 'Which month - January, February, March, April, May, June, or all of them? '
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input(month_question).lower()
        if month in months:
            return month
        else:
            print('Invalid input! Please type the name of the month or "all".')


# In[44]:


# get user input for day of week (all, monday, tuesday, ... sunday)
def get_day():
    """
    Asks user to specify a day of week to analyze.

    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    day_question = 'Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all of them? '
    days = ['all', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input(day_question).lower()
        if day in days:
            return day
        else:
            print('Invalid input! Please type one day of the week or the word "all".')


# In[45]:


# the final filtering function
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    city = get_city()

    # get user input for filtering (by month, by day, both or none)
    while True:
        filter_question = 'Would you like to filter the data by month, by day, both or none? '
        filter_answer = input(filter_question).lower()

        if filter_answer in ['by month', 'month']:
            print('Filtering by month.')
            # get user input for month and set day to "all"
            month = get_month()
            day = 'all'
            break
        elif filter_answer in ['by day', 'day']:
            print('Filtering by day.')
            # get user input for day and set month to "all"
            month = 'all'
            day = get_day()
            break
        elif filter_answer in ['by both', 'both']:
            print('Filtering by both month and day.')
            # get user inputs for both day and month
            month = get_month()
            day = get_day()
            break
        elif filter_answer in ['by none', 'none']:
            print('No filtering selected.')
            # set month and day to "all"
            month = 'all'
            day = 'all'
            break
        else:
            print('Invalid choice. Please try again.')

    print('-' * 40)
    return city, month, day


# In[46]:


# helper functions for convert the numbers of month and day of week to their names
def number_to_month(month):
    """
    Converts numeric value of month to its corresponding month name.

    Args:
        month (int): Numeric value of the month.

    Returns:
        str: Month name.
    """
    months = {
        1: 'january',
        2: 'february',
        3: 'march',
        4: 'april',
        5: 'may',
        6: 'june'
    }

    return months.get(month, None)

# Convert day number to day name


def number_to_day(day):
    """
    Converts numeric value of day of week to its corresponding name.

    Args:
        day (int): Numeric value of the day.

    Returns:
        str: Day name.
    """
    days = {
        1: 'monday',
        2: 'tuesday',
        3: 'wednesday',
        4: 'thursday',
        5: 'friday',
        6: 'saturday',
        7: 'sunday',
    }

    return days.get(day, None)


# In[58]:


# the final function for loading the filtered data
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    filename = CITY_DATA[city]
    df = pd.read_csv(filename, usecols=lambda x: x != 'Unnamed: 0')

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['month'] = df['month'].apply(lambda x: number_to_month(x))
    df['day'] = df['Start Time'].dt.dayofweek
    df['day'] = df['day'].apply(lambda x: number_to_day(x))

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day]

    return df


# In[48]:


# the function for displaying the data upon user request
def display_raw_data(df):
    """
    Displays raw data from the DataFrame in chunks of 5 lines at the user's request.

    Args:
        df (DataFrame): The DataFrame containing the data.

    Returns:
        None
    """
    # initialize starting index and iterate until user says 'no' or there is no more raw data to display
    start_index = 0
    while True:
        display_data = input(
            'Would you like to see 5 lines of raw data? Enter "yes" or "no": ').lower()

        if display_data in ['yes', 'y']:
            if start_index >= len(df):
                print('No more raw data to display.')
                break

            # display the next 5 lines of raw data
            print(df[start_index: start_index + 5])

            # increment the starting index for the next iteration
            start_index += 5
        elif display_data in ['no', 'n']:
            break
        else:
            print('Invalid input. Please enter "yes" or "no".')


# In[49]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is:', common_month)

    # display the most common day of week
    common_day = df['day'].mode()[0]
    print('The most common day of the week is:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    print(f'This took {(time.time() - start_time)} seconds.')
    print('-'*40)


# In[50]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', common_end_station)

    # display most frequent combination of start station and end station trip
    frequent_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    start_station = frequent_combination[0]
    end_station = frequent_combination[1]
    print('The most frequent combination of start and end stations:')
    print('Start Station:', start_station)
    print('End Station:', end_station)

    print(f'This took {(time.time() - start_time)} seconds.')
    print('-'*40)


# In[51]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)

    print(f'This took {(time.time() - start_time)} seconds.')
    print('-'*40)


# In[60]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('Counts of user types:')
    for user_type, count in user_type_counts.items():
        print(f'{user_type}: {count}')

    # display counts of gender
    gender_counts = df['Gender'].value_counts()
    print('Counts of gender:')
    for gender, count in gender_counts.items():
        print(f'{gender}: {count}')

    # display earliest, most recent, and most common year of birth
    earliest_birth_year = df['Birth Year'].min()
    most_recent_birth_year = df['Birth Year'].max()
    most_common_birth_year = df['Birth Year'].mode()[0]
    print('Earliest birth year:', int(earliest_birth_year))
    print('Most recent birth year:', int(most_recent_birth_year))
    print('Most common birth year:', int(most_common_birth_year))

    print(f'This took {(time.time() - start_time)} seconds.')
    print('-'*40)


# In[53]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            break


# In[61]:


if __name__ == "__main__":
    main()


# In[ ]:
