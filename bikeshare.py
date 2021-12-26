import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

WEEKDAYS = ['All', 'Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to analyze: Chicago, New York City, or Washington? ')
    city = city.lower()
    while city not in CITY_DATA:
        print('That is not one of the cities in the dataset.')
        city = input('Which city would you like to analyze: Chicago, New York City, or Washington? ')
        city = city.lower()
    # get user input for month (all, january, february, ... , june)
    month = input('Enter the month to filter by (January - June) or enter "all" for data for all months: ')
    month = month.lower()
    while month not in MONTHS:
        print('That is not a valid month.')
        month = input('Enter the month to filter by (January - June) or enter "all" for data for all days: ')
        month = month.lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter the day of the week to filter by or enter "all" to apply no filter: ')
    day = day.title()
    while day not in WEEKDAYS:
        print('That is not a weekday.')
        day = input('Enter the day of the week to filter by or enter "all" to apply no filter: ')
        day = day.title()
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
    # read data from file
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #filter by month
    if month != 'all':
        month = MONTHS.index(month)
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    most_common_month = MONTHS[most_common_month]
    print('The most common month of travel in the data is', most_common_month.title())

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common start hour for travel is', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('The most common starting station is', most_common_start)

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('The most common end station is', most_common_end)

    # display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most common trip from start to end is \n{}'.format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # display shortest travel time
    min_travel_time = df['Trip Duration'].min()
    print('The shortest travel time in the data is {}'.format(str(datetime.timedelta(seconds=int(min_travel_time)))))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time is {}'.format((str(datetime.timedelta(seconds=int(mean_travel_time))))))
    #display longest travel time
    max_travel_time = df['Trip Duration'].max()
    print('The longest travel time in the data is {}'.format(str(datetime.timedelta(seconds=int(max_travel_time)))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_count = df['User Type'].value_counts()
    print('The total amount of "Subscriber" users is', type_count.loc['Subscriber'])
    print('The total amount of "Customer" users is {}\n'.format(type_count.loc['Customer']))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('The number of users with a listed gender of male is', gender_count.loc['Male'])
        print('The number of users with a listed gender of female is {}\n'.format(gender_count.loc['Female']))
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The earliest birth year in the dataset is', int(earliest_birth_year))
        print('The most recent birth year in the dataset is', int(recent_birth_year))
        print('The most common birth year in the dataset is', int(most_common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data from the DataFrame"""
    raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
    index = 0
    pd.set_option('display.max_columns',200)
    while raw_data.lower() == 'yes':
        print(df.iloc[index:index + 5])
        index += 5
        raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
