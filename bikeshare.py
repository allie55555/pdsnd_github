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
    # Getting user input for city (chicago, new york city, washington).
    cities = ["chicago", "new york city", "washington"]
    while True:
        city = input("Please enter chicago, new york city or washington: ").lower()
        if city not in cities:
            continue
        elif city in cities:
            break

    # Getting user input for month (all, january, february, ... , june)
    months = ["all", "january", "february", "march", "april", "may", "june"]
    while True:
        month = input("Please enter january, february, march, april, may, june or all: ")
        if month not in months:
            continue
        elif month in months:
            break

    # Getting user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all", "all", "monday", "tuesday", "wedensday", "thursday", "friday", "saterday", "sunday"]
    while True:
        day = input("Please enter monday, tuesday, wedensday, thursday, friday, saterday, sunday or all: ")
        if day not in days:
            continue
        elif day in days:
            break


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour, month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # The most common month
    popular_month = df['month'].mode()[0]

    # The most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # The most common start hour
    popular_hour = df['hour'].mode()[0]
    
    print('Most Popular Start Hour: ', popular_hour)
    print('Most Popular Start Day: ', popular_day)
    print('Most Popular Start Month: ', popular_month)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # Most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # Most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().nlargest(1)

    print('Most Commonly Used Start Station: ', popular_start_station)
    print('Most Commonly Used End Station: ', popular_end_station)
    print('Most Frequent Trip:\n', popular_combination)    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = df['Trip Duration'].sum()

    # Mean travel time
    average_travel_time = df['Trip Duration'].mean()
    
    print('Total Travel Time in Seconds: ', total_travel_time)
    print('Average Travel Time in Seconds: ', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df['User Type'].value_counts()
    
    try:
        # Counts of gender
        user_genders = df['Gender'].value_counts()

        # Earliest, most recent, and most common year of birth\
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        
    except:
        user_genders = "No gender data available"
        earliest_birth_year = "No data on birth year available"
        recent_birth_year = "No data on birth year available"
        common_birth_year = "No data on birth year available"

    
    print('Counts of User Types:\n', user_types)
    print()
    print('Counts of User Genders:\n', user_genders)
    print()
    print('Earliest Birth Year: ', earliest_birth_year)
    print('Most Recent Birth Year: ', recent_birth_year)
    print('Most Common Birth Year: ', common_birth_year)

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
        
        # while loop to view first or additional rows of raw data 
        start_row = 0
        end_row = 4
        while True:
            more_rows = input('\nWould you like to view first (or five additional) rows of raw data? Enter yes or no.\n')
            if more_rows.lower() == 'yes':
                print(df.iloc[start_row:end_row])
                start_row +=5
                end_row +=5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
