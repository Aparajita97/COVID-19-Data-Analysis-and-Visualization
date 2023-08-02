import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

VALID_CITIES = ['new york city', 'chicago', 'washington']
VALID_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
VALID_DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']



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

    while True:
        city = input("\nWhich city would you like to filter by? Please choose from New York City, Chicago, or Washington.\n").lower()
        if city not in VALID_CITIES:
            print("Sorry, I didn't understand. Please try again.")
            continue
        else:
            break
 # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        month = input("\nWhich month would you like to filter by? Please choose from January, February, March, April, May, June, or type 'all' if you do not have any preference.\n").lower()
        if month not in VALID_MONTHS:
            print("Sorry, I didn't understand. Please try again.")
            continue
        else:
            break
# TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or type 'all' if you do not have any preference.\n").lower()
        if day not in VALID_DAYS:
            print("Sorry, I didn't understand. Please try again.")
            continue
        else:
            break

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        month = VALID_MONTHS.index(month) 
      
        df = df[df['month'] == month]

    # Filter by day of the week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', VALID_MONTHS[popular_month - 1].title())

    # Display the most common day of the week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', start_station)

    # Display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', end_station)

    # Display most frequent combination of start station and end station trip
    combination_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Commonly Used Combination of Start Station and End Station Trip:', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time // 86400, "Days")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time // 60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    else:
        print('\nGender Types:\nNo data available for this month.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('\nEarliest Year:', int(earliest_year))
        print('Most Recent Year:', int(most_recent_year))
        print('Most Common Year:', int(most_common_year))
    else:
        print('\nYear of Birth:\nNo data available for this month.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    
    currentIndex = 0
    while True:
        option = input("\nDo you want to see 5 lines of data? Please choose from Yes / No.\n").lower()
        if option== "yes":
            start = currentIndex
            end = currentIndex + 5
            print(df.iloc[start:end])
            currentIndex = currentIndex + 5
            continue
        else:
            break    
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()