import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#
# This is a quick block for git versioning and testing #1
#
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please select city:').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Please select from chicago, new york city, or washington ONLY:').lower()

    #get user input for month (all, january, february, ... , june)
    month = input('Please select a month:').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Please select from these months ONLY: january, february, march, april, may, or june:').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please select a day:').lower()
    while day not in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        day = input('Please choose from sunday, monday, tuesday, wednesday, thursday, friday or saturday ONLY:').lower()

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

    #load the proper csv using the provided key
    df = pd.read_csv(CITY_DATA[city])

    #date/time formatting
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #get month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter to month selection
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter to day selection
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    try:
     month_mode = df['month'].mode()[0]
     print('Most Common Month: ', month_mode)
    except KeyError:
     print('\nData not available for this dataset.')

    #display the most common day of week
    try:
     day_mode = df['day_of_week'].mode()[0]
     print('Most Common Day of the Week: ', day_mode)
    except KeyError:
     print('\nMost Common Day of the Week not available for this dataset.')

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    try:
     hour_mode = df['hour'].mode()[0]
     print('Most Common Hour of the Day: ', hour_mode)
    except KeyError:
     print('\nMost Common Hour not available for this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    try:
     station_mode = df['Start Station'].mode()[0]
     print('Most Common Start Station: ', station_mode)
    except KeyError:
     print('\nMost Common Start Station not available for this dataset.')


    #display most commonly used end station
    try:
     end_station_mode = df['End Station'].mode()[0]
     print('Most Common End Station: ', end_station_mode)
    except KeyError:
     print('\nMost Common End Station not available for this dataset.')

    #display most frequent combination of start station and end station trip
    try:
     trip_mode = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
     print('Most Common Trip:\n', trip_mode.to_string())
    except KeyError:
     print('\nMost Common Trip not available for this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    try:
     duration_hours = df['Trip Duration'].sum() / 3600.0
     print('Total Travel Time (hours): ', duration_hours)
    except KeyError:
     print('\nTotal Travel Time not available for this dataset.')

    #display mean travel time
    try:
     duration_mean = df['Trip Duration'].mean() / 3600.0
     print('Average Travel Time (hours): ', duration_mean)
    except KeyError:
     print('\nAverage Travel Time not available for this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    try:
     user_types = df['User Type'].value_counts()
     print('User Types:\n', user_types.to_string())
    except KeyError:
     print('\nUser Types not available for this dataset.')

    #Display counts of gender
    try:
     gender_count = df['Gender'].value_counts()
     print('\nGender Types: \n', gender_count.to_string())
    except KeyError:
     print('\nGender Types not available for this dataset.')

    #Display earliest, most recent, and most common year of birth
    try:
     earliest_year = df['Birth Year'].min()
     print('\nEarliest Year: ', earliest_year)
    except KeyError:
     print('\nEarliest Year not available for this dataset.')

    try:
     newest_year = df['Birth Year'].max()
     print('Most Recent Year: ', newest_year)
    except KeyError:
     print('\nMost Recent Year not available for this dataset.')

    try:
     year_mode = df['Birth Year'].mode()[0]
     print('Most Common Year: ', year_mode)
    except KeyError:
     print('\nMost Common Year not available for this dataset.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def raw_data(df):
    #display raw data 5 rows at a time
    print('\nRaw Data Sample: ')
    print(df.head())
    x = 0
    while True:
        view_data = input('\nWould you like to see 5 more rows? Enter yes or no.')
        if view_data != 'yes':
            return
        x = x + 5
        print(df.iloc[x:x+5])


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
