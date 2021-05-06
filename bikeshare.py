"""
This program analyzes bikeshare data for 3 majour US cities and
interactively displays important summary statistics.
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nWhich city would you like to select first? chicago,new york city or washington?\n: ").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input(
        "Invalid entry.Please select one of the following :chicago,new york city or washington: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("\nPlease select a month from the following list: january, february, march, april, may, june or type 'all' if you'd like to see all months\n").lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input("Invalid entry.Please select a month from the list above").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nPlease enter a day of the week.Please select from the following list:monday, tuesday, wednesday, thursday, friday, saturday,sunday or type 'all' if you'd like to see all days of the week.\n").lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday', 'all']:
        day=input("Invalid entry.Please select a day of the week from the list above.").lower()

    print('-'*40)
    return city, month, day


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
    # read data from .csv file
    df = pd.read_csv(CITY_DATA[city])

    # ask users whether they would like to review the raw data first
    show_raw_data = input('Would you like to see the first 5 rows of raw data? Please type yes or no: ').lower()
    if show_raw_data == 'yes':
        number_rows =  len(df.index)
        i = int(input('Please, enter the row number you want to see the data from: '))
        while show_raw_data == 'yes':
            print(df.iloc[i:i+5, :])
            i+=5
            #check for the end of data set
            if i >= number_rows:
                print('-->>The end of data set is reached.\n')
                break
            show_raw_data = input('To see the next 5 rows type in "yes" otherwise "no" ').lower()
            if show_raw_data == 'no':
                break

    # convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # filter by month to create the new dataframe
    df = df[df['month'] == month]

    #filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Start_Station)

    # TO DO: display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', End_Station)

    # TO DO: display most frequent combination of start station and end station trip
    Combination_Trip = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost Commonly used combination of start station and end station trip:', Start_Station, " & ", End_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # TO DO: display total travel time
    print("The total travel time is: {}".format(str(df['duration'].sum())))

    # TO DO: display mean travel time
    print("The mean travel time is: {}".format(str(df['duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of user types:")
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available for this gender type.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        Earliest_Year = df['Birth Year'].min()
        print('\nEarliest Year:', Earliest_Year)
    except KeyError:
        print("\nEarliest Year:\nNo data available for this birth year.")
    try:
        Most_Recent_Year =df['Birth Year'].max()
        print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
        print("\nMost Recent Year:\nNo data available for this birth year.")
    try:
        Most_Common_Year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
        print("\nMost Common Year :\nNo data available for this birth year")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
