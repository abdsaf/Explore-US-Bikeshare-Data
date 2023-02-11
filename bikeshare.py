import time
import pandas as pd
import numpy as np

#dictionary to map user input (city) with csv file
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#dictionary to check each user inputs with associated considered valid input
"""
we can make list for each input validator , but I think it is more logical
and clean code to define data structure as dictionary for all valid user input
"""
valid_user_input = { 'city':['chicago','new york city','washington'],
                     'month':['all','january','february','march','april','may','june'],
                     'day':['all', 'monday','tuesday','wednesday','thursday','friday','saturday','sunday']}
#list of month names to be used when need it (Filter , printed)
months = ['january', 'february', 'march', 'april', 'may', 'june']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city,month,day=None,None,None
    try:
        print('Hello! Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        while True:
            print()
            city=input('Enter exactly city from the following [chicago, new york city, washington] :\n').lower()
            if city in valid_user_input['city']:
                break
    
         # get user input for month (all, january, february, ... , june)
        while True:
             print()
             month=input('In which month do you want to analyse data [all, january, february,  march, april ,may, june] :\n').lower()
             if month in valid_user_input['month']:
                 break
    
         # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            print()
            day=input('In which day of week do you want to analyse data [all, monday, tuesday, wednesday,thursday,friday,saturday,sunday]\n').lower()
            if day in valid_user_input['day']:
                break 
        print('-'*40)
    except Exception as e:
        print("Exception occurred: {}".format(e))
        
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
    df=None
    #read csv file 
    try:
        df = pd.read_csv(CITY_DATA[city])
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()
        # extract start hour to be used in other functions like time_state
        df['hour']=df['Start Time'].dt.hour
        if month != 'all':
            print()
            # use the index of the months list to get the corresponding int
            month = months.index(month)+1
            # filter by month to create the new dataframe
            df = df[df['month']==month]
         # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week']==day.title()]
    except Exception as e:
        print("Exception occurred: {}".format(e))
        
    return df

    


def time_stats(df):
    try:
        """Displays statistics on the most frequent times of travel."""

        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        month_name =months[df['month'].mode()[0]-1]
        print("Most trips were happened in month : {}".format(month_name.title()))


        # display the most common day of week
        print("Most trips were happened in day : {}".format(df['day_of_week'].mode()[0].title()))
    
        # display the most common start hour
        print("Most trips started at hour : {}".format(df['hour'].mode()[0]))

    except Exception as e:
        print("Exception occurred: {}".format(e))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    
    try:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        print("Most trips started from station: {}".format(df['Start Station'].mode()[0]))
    
    
        # display most commonly used end station
        print("Most trips ended at station: {}".format(df['End Station'].mode()[0]))


        # display most frequent combination of start station and end station trip
        """
        using the below link for groupby multi columns and count 
        https://sparkbyexamples.com/pandas/pandas-groupby-count-examples/
        actually the easy way is to combine start & end station in new column but I don't want to add ad-hoc data to original dataset if we can find solution by calling built-in functions or mehtods
        """
        df_most_freq=df.groupby(['Start Station','End Station']).size().reset_index(name="counts").sort_values(by=['counts'], ascending=False).head(1).reset_index()
         
        print("Most commonly trips from Start Station : [{}] to End Station [{}]\nIn total there are {} trips from the mentioed stations".format(df_most_freq['Start Station'][0],df_most_freq['End Station'][0],df_most_freq['counts'][0]))
        
    except Exception as e:
        print("Exception occurred: {}".format(e))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def format_duration(total_duration_inseconds):
    """
    this function to get Total number of days, hours, minutes and second
    from given total seconds to display information in more insight

    Parameters
    ----------
    total_duration_inseconds : TYPE
        Total number of second.

    Returns
    -------
    days : TYPE
        Number of days.
    hours : TYPE
        Number of hours.
    minutes : TYPE
        Total minutes.
    seconds : TYPE
        Total seconds.

    """
    days,hours,minutes,seconds=0,0,0,0
    try:
        #get time parts from total seconds
        days=total_duration_inseconds//(24*3600)
        hours=(total_duration_inseconds-(days*24*3600))//3600
        minutes=(total_duration_inseconds-(days*24*3600)-(hours*3600))//60
        seconds=total_duration_inseconds-(days*24*3600)-(hours*3600)-(minutes*60)
        seconds=round(seconds,2)
    except Exception as e:
        print("Exception occurred: {}".format(e))
    return days,hours,minutes,seconds

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    try:
        
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()
    
        # display total travel time
        days,hours,minutes,seconds=format_duration(np.sum(df['Trip Duration']))
        print("Total travle time is {} days, {} hours , {} minutes ,{} seconds".format(days,hours,minutes,seconds))
    
    
        # display mean travel time
        days,hours,minutes,seconds=format_duration(round(np.mean(df['Trip Duration']),2))
        print("Average travle time is {} hours , {} minutes ,{} seconds".format(hours,minutes,seconds))
    except Exception as e:
        print("Exception occurred: {}".format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):   
    """Displays statistics on bikeshare users."""
    
    try:
        
        print('\nCalculating User Stats...\n')
        start_time = time.time()
        user_stat = None
        # Display counts of gender
        print("Analysis users by gender :")
        if 'Gender' in df.columns:
            #Fill missing data 
            df['Gender'].fillna(method='bfill',inplace=True)
            user_stat = df.groupby(['Gender'])['Gender'].count()
            print(user_stat)
        else:
            print('Your dataset does not contain users Gender!!')
            
        # Display earliest, most recent, and most common year of birth
        print("\nAnalysis users by birth year:")
        if 'Birth Year' in df.columns:
            df['Birth Year'].fillna(method='bfill',inplace=True)
            earliest=int(np.min(df['Birth Year']))
            most_recent=int(np.max(df['Birth Year']))
            most_common=int(df['Birth Year'].mode()[0])
            print("The oldest user was boren in :{}\nThe youngest user was born in {},\nMostly users were born in {}".format(earliest,most_recent,most_common))
        else:
            print('Your dataset does not contain users birth date!!')
            
        # Display counts of user types,
        print("\nAnalysis users by type:")
        if 'User Type' in df.columns:
            df['User Type'].fillna(method='bfill',inplace=True)
            user_stat = df.groupby(['User Type'])['User Type'].count()
            print(user_stat)
        else:
            print('Your dataset does not contain users type!!')
        
    except Exception as e:
        print("Exception occurred: {}".format(e))
    
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
        view_details_resultset=True
        while view_details_resultset:
            view_data=input('would you like to view first 5 rows of raw data?')
            if view_data!='yes':
                break   
            else:
                row_index=0
                while True:
                    print(df.iloc[row_index:row_index+5])
                    row_index+=5
                    view_data=input('would you like to view the next 5 rows of raw data?')
                    if view_data!='yes':
                        view_details_resultset=False
                        break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
